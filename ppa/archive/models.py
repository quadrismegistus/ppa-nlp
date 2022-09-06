import logging
import os.path
import re
import time
from zipfile import ZipFile

import requests
from cached_property import cached_property
from django.conf import settings
from django.conf.urls import url
from django.contrib.admin.models import ADDITION, CHANGE, LogEntry
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from eulxml.xmlmap import load_xmlobject_from_file
from flags import Flags
from intspan import ParseError as IntSpanParseError
from intspan import intspan
from pairtree import pairtree_client, pairtree_path, storage_exceptions
from parasolr.django import SolrQuerySet
from parasolr.django.indexing import ModelIndexable
from parasolr.indexing import Indexable
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.snippets.models import register_snippet

from ppa.archive.gale import GaleAPI, MARCRecordNotFound, get_marc_record
from ppa.archive.hathi import HathiBibliographicAPI, HathiObject, MinimalMETS

logger = logging.getLogger(__name__)


#: label to use for items that are not in a collection
NO_COLLECTION_LABEL = "Uncategorized"


class TrackChangesModel(models.Model):
    """:class:`~django.models.Model` mixin that keeps a copy of initial
    data in order to check if fields have been changed. Change detection
    only works on the current instance of an object."""

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # store a copy of model data to allow for checking if
        # it has changed
        self.__initial = self.__dict__.copy()

    def save(self, *args, **kwargs):
        """Saves data and reset copy of initial data."""
        super().save(*args, **kwargs)
        # update copy of initial data to reflect saved state
        self.__initial = self.__dict__.copy()

    def has_changed(self, field):
        """check if a field has been changed"""
        # Only consider the field changed if the object has been saved
        return self.pk and getattr(self, field) != self.__initial[field]

    def initial_value(self, field):
        """return the initial value for a field"""
        return self.__initial[field]


@register_snippet
class Collection(TrackChangesModel):
    """A collection of :class:`ppa.archive.models.DigitizedWork` instances."""

    #: the name of the collection
    name = models.CharField(max_length=255)
    #: a RichText description of the collection
    description = RichTextField(blank=True)
    #: flag to indicate collections to be excluded by default in
    #: public search
    exclude = models.BooleanField(
        default=False, help_text="Exclude by default on public search."
    )

    # configure for editing in wagtail admin
    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    @property
    def name_changed(self):
        """check if name has been changed (only works on current instance)"""
        return self.has_changed("name")

    @staticmethod
    def stats():
        """Collection counts and date ranges, based on what is in Solr.
        Returns a dictionary where they keys are collection names and
        values are a dictionary with count and dates.
        """

        # NOTE: if we *only* want counts, could just do a regular facet
        sqs = (
            SolrQuerySet()
            .stats("{!tag=piv1 min=true max=true}pub_date")
            .facet(pivot="{!stats=piv1}collections_exact")
        )
        facet_pivot = sqs.get_facets().facet_pivot
        # simplify the pivot stat data for display
        stats = {}
        for collection in facet_pivot.collections_exact:
            pub_date_stats = collection.stats.stats_fields.pub_date
            stats[collection.value] = {
                "count": collection.count,
                "dates": "%(min)d–%(max)d" % pub_date_stats
                if pub_date_stats.max != pub_date_stats.min
                else "%d" % (pub_date_stats.min or 0,),
            }

        return stats


class ProtectedWorkFieldFlags(Flags):
    """:class:`flags.Flags` instance to indicate which :class:`DigitizedWork`
    fields should be protected if edited in the admin."""

    #: title
    title = ()
    #: subtitle
    subtitle = ()
    #: sort title
    sort_title = ()
    #: enumcron
    enumcron = ()
    #: author
    author = ()
    #: place of publication
    pub_place = ()
    #: publisher
    publisher = ()
    #: publication date
    pub_date = ()

    @classmethod
    def deconstruct(cls):
        """Give Django information needed to make
        :class:`ProtectedWorkFieldFlags.no_flags` default in migration."""
        # (import path, [args], kwargs)
        return ("ppa.archive.models.ProtectedWorkFieldFlags", ["no_flags"], {})

    def __str__(self):
        return ", ".join(sorted(self.to_simple_str().split("|")))


class ProtectedWorkField(models.Field):
    """PositiveSmallIntegerField subclass that returns a
    :class:`ProtectedWorkFieldFlags` object and stores as integer."""

    description = (
        "A field that stores an instance of :class:`ProtectedWorkFieldFlags` "
        "as an integer."
    )

    def __init__(self, verbose_name=None, name=None, **kwargs):
        """Make the field unnullable and not allowed to be blank."""
        super().__init__(verbose_name, name, blank=False, null=False, **kwargs)

    def from_db_value(self, value, expression, connection):
        """Always return an instance of :class:`ProtectedWorkFieldFlags`"""
        return ProtectedWorkFieldFlags(value)

    def get_internal_type(self):
        return "PositiveSmallIntegerField"

    def get_prep_value(self, value):
        return int(value)

    def to_python(self, value):
        """Always return an instance of :class:`ProtectedWorkFieldFlags`"""
        return ProtectedWorkFieldFlags(value)


class CollectionSignalHandlers:
    """Signal handlers for indexing :class:`DigitizedWork` records when
    :class:`Collection` records are saved or deleted."""

    @staticmethod
    def save(sender, instance, **kwargs):
        """signal handler for collection save; reindex associated digitized works"""
        # only reindex if collection name has changed
        # and if collection has already been saved
        if instance.pk and instance.name_changed:
            # if the collection has any works associated
            works = instance.digitizedwork_set.all()
            if works.exists():
                logger.debug(
                    "collection save, reindexing %d related works", works.count()
                )
                DigitizedWork.index_items(works)

    @staticmethod
    def delete(sender, instance, **kwargs):
        """signal handler for collection delete; clear associated digitized
        works and reindex"""
        logger.debug("collection delete")
        # get a list of ids for collected works before clearing them
        digwork_ids = instance.digitizedwork_set.values_list("id", flat=True)
        # find the items based on the list of ids to reindex
        digworks = DigitizedWork.objects.filter(id__in=list(digwork_ids))

        # NOTE: this sends pre/post clear signal, but it's not obvious
        # how to take advantage of that
        instance.digitizedwork_set.clear()
        DigitizedWork.index_items(digworks)


def validate_page_range(value):
    """Ensure page range can be parsed as an integer span"""
    try:
        intspan(value)
    except IntSpanParseError as err:
        raise ValidationError(
            "Parse error: %(message)s",
            params={"message": err},
        )


class DigitizedWork(ModelIndexable, TrackChangesModel):
    """
    Record to manage digitized works included in PPA and store their basic
    metadata.
    """

    HATHI = "HT"
    GALE = "G"
    OTHER = "O"
    SOURCE_CHOICES = (
        (HATHI, "HathiTrust"),
        (GALE, "Gale"),
        (OTHER, "Other"),
    )
    #: source of the record, HathiTrust or elsewhere
    source = models.CharField(
        max_length=2,
        choices=SOURCE_CHOICES,
        default=HATHI,
        help_text="Source of the record.",
    )
    #: source identifier; hathi id for HathiTrust materials
    source_id = models.CharField(
        max_length=255,
        verbose_name="Source ID",
        help_text="Source identifier. Must be unique when combined with page range; "
        + "used for site URL. (HT id for HathiTrust materials.)",
    )
    #: source url where the original can be accessed
    source_url = models.URLField(
        max_length=255,
        verbose_name="Source URL",
        blank=True,
        help_text="URL where the source item can be accessed",
    )
    #: record id; for Hathi materials, used for different copies of
    #: the same work or for different editions/volumes of a work
    record_id = models.CharField(
        max_length=255,
        blank=True,
        help_text="For HathiTrust materials, record id (use to aggregate "
        + "copies or volumes); for Gale materials, ESTC id.",
    )
    #: title of the work; using TextField to allow for long titles
    title = models.TextField(help_text="Main title")
    #: subtitle of the work; using TextField to allow for long titles
    subtitle = models.TextField(
        blank=True, default="", help_text="Subtitle, if any (optional)"
    )
    #: sort title: title without leading non-sort characters, from marc
    sort_title = models.TextField(
        default="",
        help_text="Sort title from MARC record or title without leading article",
    )
    #: enumeration/chronology (hathi-specific; contains volume or version)
    enumcron = models.CharField(
        "Enumeration/Chronology/Volume",
        max_length=255,
        blank=True,
        help_text="Enumcron for HathiTrust material; volume for Gale material",
    )
    # NOTE: may eventually to convert to foreign key
    author = models.CharField(
        max_length=255,
        blank=True,
        help_text="Authorized name of the author, last name first.",
    )
    #: place of publication
    pub_place = models.CharField("Place of Publication", max_length=255, blank=True)
    #: publisher
    publisher = models.TextField(blank=True)
    # Needs to be integer to allow aggregating max/min, filtering by date
    pub_date = models.PositiveIntegerField("Publication Date", null=True, blank=True)
    #: number of pages in the work
    page_count = models.PositiveIntegerField(null=True, blank=True)
    #: public notes field for this work
    public_notes = models.TextField(
        blank=True,
        default="",
        help_text="Notes on edition or other details (displayed on public site)",
    )
    #: internal team notes, not displayed on the public facing site
    notes = models.TextField(
        blank=True,
        default="",
        help_text="Internal curation notes (not displayed on public site)",
    )
    #: :class:`ProtectedWorkField` instance to indicate metadata fields
    #: that should be preserved from bulk updates because they have been
    #: modified in Django admin.
    protected_fields = ProtectedWorkField(
        default=ProtectedWorkFieldFlags,
        help_text="Fields protected from HathiTrust bulk "
        "update because they have been manually edited in the "
        "Django admin.",
    )
    #: collections that this work is part of
    collections = models.ManyToManyField(Collection, blank=True)
    #: date added to the archive
    added = models.DateTimeField(auto_now_add=True)
    #: date of last modification of the local record
    updated = models.DateTimeField(auto_now=True)

    PUBLIC = "P"
    SUPPRESSED = "S"
    STATUS_CHOICES = (
        (PUBLIC, "Public"),
        (SUPPRESSED, "Suppressed"),
    )
    #: status of record; currently choices are public or suppressed
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=PUBLIC,
        help_text="Changing status to suppressed will remove rsync data "
        + "for that volume and remove from the public index. This is "
        + "currently not reversible; use with caution.",
    )

    FULL = "F"
    EXCERPT = "E"
    ARTICLE = "A"
    ITEMTYPE_CHOICES = (
        (FULL, "Full work"),
        (EXCERPT, "Excerpt"),
        (ARTICLE, "Article"),
    )
    #: type of record, whether excerpt, article, or full; defaults to full
    item_type = models.CharField(
        max_length=1,
        choices=ITEMTYPE_CHOICES,
        default=FULL,
        help_text="Portion of the work that is included; used to determine icon for public display.",
    )
    #: book or journal title for excerpt or article
    book_journal = models.TextField(
        "Book/Journal title",
        help_text="title of the book or journal that includes this content (excerpt/article only)",
        blank=True,
    )
    pages_orig = models.CharField(
        "Page range (original)",
        max_length=255,
        help_text="Page range in the original work (for display and citation).",
        blank=True,
    )
    pages_digital = models.CharField(
        "Page range (digital edition)",
        max_length=255,
        help_text="Sequence of pages in the digital edition. "
        + "Use full digits for start and end separated by a dash (##-##); "
        + "for multiple sequences, separate ranges by a comma (##-##, ##-##). "
        + "NOTE: removing page range may have unexpected results.",
        blank=True,
        validators=[validate_page_range],
    )

    class Meta:
        ordering = ("sort_title",)
        # require unique combination of source id + page range,
        # since we need to allow multiple excerpts from the same source
        constraints = [
            models.UniqueConstraint(
                fields=["source_id", "pages_digital"], name="unique_sourceid_pagerange"
            )
        ]

    def get_absolute_url(self):
        """
        Return object's url for
        :class:`ppa.archive.views.DigitizedWorkDetailView`
        """
        url_opts = {"source_id": self.source_id}
        # start page must be specified if set but must not be included if empty
        if self.pages_digital:
            url_opts["start_page"] = self.first_page()
        return reverse("archive:detail", kwargs=url_opts)

    def __str__(self):
        """Default string display. Uses :attr:`source_id` and :attr:`pages_digital` if any"""
        if self.pages_digital:
            return "%s (%s)" % (self.source_id, self.pages_digital)
        return self.source_id

    def clean_fields(self, exclude=None):
        if not exclude or "pages_digital" not in exclude:
            # normalize whitespace in pages digital field before applying regex validation
            self.pages_digital = " ".join(self.pages_digital.strip().split())
        super().clean_fields(exclude=exclude)

    @property
    def is_suppressed(self):
        """Item has been suppressed (based on :attr:`status`)."""
        return self.status == self.SUPPRESSED

    def display_title(self):
        """admin display title to allow displaying title but sorting on sort_title"""
        return self.title

    display_title.short_description = "title"
    display_title.admin_order_field = "sort_title"

    def is_public(self):
        """admin display field indicating if record is public or suppressed"""
        return self.status == self.PUBLIC

    is_public.short_description = "Public"
    is_public.boolean = True
    is_public.admin_order_field = "status"

    #: regular expresion for cleaning preliminary text from publisher names
    printed_by_re = (
        r"^(Printed)?( and )?(Pub(.|lished|lisht)?)?( and sold)? (by|for|at)( the)? ?"
    )
    # Printed by/for (the); Printed and sold by; Printed and published by;
    # Pub./Published/Publisht at/by/for the
    pubyear_re = re.compile(r"(?P<year>\d{4})")

    @property
    def has_fulltext(self):
        """Checks if an item has full text (currently only items from
        HathiTrust or Gale)."""
        return self.source in [self.HATHI, self.GALE]

    @cached_property
    def hathi(self):
        """:class:`ppa.archive.hathi.HathiObject` for HathiTrust records,
        for working with data in HathiTrust pairtree data structure."""
        if self.source == self.HATHI:
            return HathiObject(self.source_id)
        return None

    def save(self, *args, **kwargs):
        # if status has changed so that object is now suppressed,
        # do some cleanup
        if self.has_changed("status") and self.status == self.SUPPRESSED:
            # remove indexed page content from Solr
            self.solr.update.delete_by_query('source_id:"%s"' % self.source_id)
            # if this is a HathiTrust item, remove pairtree data
            if self.source == DigitizedWork.HATHI:
                self.hathi.delete_pairtree_data()

        # Solr identifier is based on combination of source id and first page;
        # if either changes, remove the old record from Solr before saving
        # with the new identifier
        if self.has_changed("source_id") or self.has_changed("pages_digital"):
            # store the updated values
            new_source_id = self.source_id
            new_pages_digital = self.pages_digital
            # temporarily revert to previous value to remove from index
            self.source_id = self.initial_value("source_id")
            self.pages_digital = self.initial_value("pages_digital")
            self.remove_from_index()
            # restore new values
            self.source_id = new_source_id
            self.pages_digital = new_pages_digital

        if self.has_changed("pages_digital"):
            # if there is a page range set now, update page count and index
            if self.pages_digital:
                # recalculate page total based on current range
                self.page_count = self.count_pages()
                # update index to remove all pages that are no longer in range
                self.solr.update.delete_by_query(
                    'source_id:"%s" AND item_type:page NOT order:(%s)'
                    % (self.source_id, " OR ".join(str(p) for p in self.page_span))
                )
            # any page range change requires reindexing (potentially slow)
            logger.debug("Reindexing pages for %s after change to page range", self)
            self.index_items(Page.page_index_data(self))
            # NOTE: removing a page range may not work as expected
            # (does not recalculate page count; cannot recalculate for Gale items)

        super().save(*args, **kwargs)

    def clean(self):
        """Add custom validation to trigger a save error in the admin
        if someone tries to unsuppress a record that has been suppressed
        (not yet supported)."""
        if self.has_changed("status") and self.status != self.SUPPRESSED:
            raise ValidationError("Unsuppressing records not yet supported.")

        # should not be editable in admin, but add a validation check
        # just in case
        if self.has_changed("source_id") and self.source == self.HATHI:
            raise ValidationError(
                "Changing source ID for HathiTrust records is not supported"
            )

    def compare_protected_fields(self, db_obj):
        """Compare protected fields in a
        :class:`ppa.archive.models.DigitizedWork` instance and return those
        that are changed.

        :param object db_obj: Database instance of a
            :class:`~ppa.archive.models.DigitizedWork`.
        """
        changed_fields = []
        # if a field has changed, append to changed fields
        for field in ProtectedWorkFieldFlags.all_flags:
            # field is in format of ProtectedWorkFieldFlags.title
            field_name = str(field)
            # if obj has a different value for a protected field
            # than its db counterpart
            if getattr(self, field_name) != getattr(db_obj, field_name):
                # append as a now protected field
                changed_fields.append(field_name)
        return changed_fields

    def populate_fields(self, field_data):
        """Conditionally update fields as protected by flags using Hathi
        bibdata information.

        :param dict field_data: A dictionary of fields updated from a
            :class:`ppa.archive.hathi.HathiBibliographicRecord` instance.
        """
        protected_fields = [str(field) for field in self.protected_fields]
        for field, value in field_data.items():
            if field not in protected_fields:
                setattr(self, field, value)

    def metadata_from_marc(self, marc_record, populate=True):
        """Get metadata from MARC record and return a dictionary
        of the data. When populate is True, calls `populate_fields`
        to set values."""

        # create dictionary to store bibliographic information
        field_data = {}
        # set title and subtitle from marc if possible
        # - clean title: strip trailing space & slash and initial bracket
        field_data["title"] = marc_record["245"]["a"].rstrip(" /").lstrip("[")

        # according to PUL CAMS,
        # 245 subfield contains the subtitle *if* the preceding field
        # ends with a colon. (Otherwise could be a parallel title,
        # e.g. title in another language).
        # HOWEVER: metadata from Hathi doesn't seem to follow this
        # pattern (possibly due to records being older?)

        # subfields is a list of code, value, code, value
        # iterate in paired steps of two starting with first and second
        # for code, value in zip(marc_record['245'].subfields[0::2],
        #                        marc_record['245'].subfields[1::2]):
        #     if code == 'b':
        #         break
        #     preceding_character = value[-1:]

        # if preceding_character == ':':
        #     self.subtitle = marc_record['245']['b'] or ''
        # NOTE: skipping preceding character check for now
        field_data["subtitle"] = marc_record["245"]["b"] or ""
        # strip trailing space & slash from subtitle
        field_data["subtitle"] = field_data["subtitle"].rstrip(" /")
        # indicator 2 provides the number of characters to be
        # skipped when sorting (could be 0)
        try:
            non_sort = int(marc_record["245"].indicators[1])
        except ValueError:
            # at least one record has a space here instead of a number
            # probably a data error, but handle it
            # - assuming no non-sort characters
            non_sort = 0

        # strip whitespace, since a small number of records have a
        # nonsort value that doesn't include a space after a
        # definite article.
        # Also strip punctuation, since MARC only includes it in
        # non-sort count when there is a definite article.
        field_data["sort_title"] = marc_record.title()[non_sort:].strip(' "[')
        field_data["author"] = marc_record.author() or ""
        # remove a note present on some records and strip whitespace
        field_data["author"] = (
            field_data["author"].replace("[from old catalog]", "").strip()
        )
        # removing trailing period, except when it is part of an
        # initial or known abbreviation (i.e, Esq.)
        # Look for single initial, but support initials with no spaces
        if field_data["author"].endswith(".") and not re.search(
            r"( ([A-Z]\.)*[A-Z]| Esq)\.$", field_data["author"]
        ):
            field_data["author"] = field_data["author"].rstrip(".")

        # field 260 includes publication information
        if "260" in marc_record:
            # strip trailing punctuation from publisher and pub place
            # subfield $a is place of publication
            field_data["pub_place"] = marc_record["260"]["a"] or ""
            field_data["pub_place"] = field_data["pub_place"].rstrip(";:,")
            # if place is marked as unknown ("sine loco"), leave empty
            if field_data["pub_place"].lower() == "[s.l.]":
                field_data["pub_place"] = ""
            # subfield $b is name of publisher
            field_data["publisher"] = marc_record["260"]["b"] or ""
            field_data["publisher"] = field_data["publisher"].rstrip(";:,")
            # if publisher is marked as unknown ("sine nomine"), leave empty
            if field_data["publisher"].lower() == "[s.n.]":
                field_data["publisher"] = ""

            # remove printed by statement before publisher name,
            # then strip any remaining whitespace
            field_data["publisher"] = re.sub(
                self.printed_by_re, "", field_data["publisher"], flags=re.IGNORECASE
            ).strip()

        # Gale/ECCO dates may include non-numeric, e.g. MDCCLXXXVIII. [1788]
        # try as numeric first, then extract year with regex
        pubdate = marc_record.pubyear()
        # at least one case returns None here,
        # which results in a TypeError on attemped conversion to integer
        if pubdate:
            try:
                field_data["pub_date"] = int(pubdate)
            except ValueError:
                yearmatch = self.pubyear_re.search(pubdate)
                if yearmatch:
                    field_data["pub_date"] = int(yearmatch.groupdict()["year"])

        # remove brackets around inferred publishers, place of publication
        # *only* if they wrap the whole text
        for field in ["publisher", "pub_place"]:
            if field in field_data:
                field_data[field] = re.sub(
                    r"^\[(.*)\]$", r"\1", field_data[field]
                ).strip()

        if populate:
            # conditionally update fields that are protected (or not)
            self.populate_fields(field_data)

        return field_data

    def populate_from_bibdata(self, bibdata):
        """Update record fields based on Hathi bibdata information.
        Full record is required in order to set all fields

        :param bibdata: bibliographic data returned from HathiTrust
            as instance of :class:`ppa.archive.hathi.HathiBibliographicRecord`

        """
        # create dictionary to store bibliographic information
        field_data = {}
        # store hathi record id
        field_data["record_id"] = bibdata.record_id

        # set fields from marc if available, since it has more details
        if bibdata.marcxml:
            # get metadata from marcxml, but don't save it yet
            field_data.update(self.metadata_from_marc(bibdata.marcxml, populate=False))
        else:
            # fallback behavior, if marc is not availiable
            # use dublin core title
            field_data["title"] = bibdata.title
            # could guess at non-sort, but hopefully unnecessary

        # pub date returned in api JSON is list; use first for now (if available)
        if bibdata.pub_dates:
            field_data["pub_date"] = bibdata.pub_dates[0]
        copy_details = bibdata.copy_details(self.source_id)
        # hathi version/volume information for this specific copy of a work
        field_data["enumcron"] = copy_details["enumcron"] or ""
        # hathi source url can currently be inferred from htid, but is
        # included in the bibdata in case it changes - so let's just store it
        field_data["source_url"] = copy_details["itemURL"]

        # should also consider storing:
        # - last update, rights code / rights string, item url
        # (maybe solr only?)

        # conditionally update fields that are protected (or not)
        self.populate_fields(field_data)

    index_depends_on = {
        "collections": {
            "post_save": CollectionSignalHandlers.save,
            "pre_delete": CollectionSignalHandlers.delete,
        }
    }

    def first_page(self):
        if self.pages_digital:
            return list(self.page_span)[0]

    def index_id(self):
        """use source id + first page in range (if any) as solr identifier"""
        first_page = self.first_page()
        if first_page:
            return "%s-p%d" % (self.source_id, first_page)
        return self.source_id

    @classmethod
    def items_to_index(cls):
        """Queryset of works for indexing everything; excludes
        suppressed works."""
        return DigitizedWork.objects.exclude(status=cls.SUPPRESSED)

    @classmethod
    def index_item_type(cls):
        """override index item type label to just work"""
        return "work"

    def index_data(self):
        """data for indexing in Solr"""

        # When an item has been suppressed, return id only.
        # This will blank out any previously indexed values, and item
        # will not be findable by any public searchable fields.
        if self.status == self.SUPPRESSED:
            return {"id": self.source_id}

        index_id = self.index_id()
        return {
            "id": index_id,
            "source_id": self.source_id,
            "first_page_i": self.first_page(),
            "group_id_s": index_id,  # for grouping pages by work or excerpt
            "source_t": self.get_source_display(),
            "source_url": self.source_url,
            "title": self.title,
            "subtitle": self.subtitle,
            "sort_title": self.sort_title,
            "pub_date": self.pub_date,
            "pub_place": self.pub_place,
            "publisher": self.publisher,
            "enumcron": self.enumcron,
            "author": self.author,
            # set default value to simplify queries to find uncollected items
            # (not set in Solr schema because needs to be works only)
            "collections": [collection.name for collection in self.collections.all()]
            if self.collections.exists()
            else [NO_COLLECTION_LABEL],
            # public notes field for display on site_name
            "notes": self.public_notes,
            # hard-coded to distinguish from & sort with pages
            "item_type": "work",
            "order": "0",
            "work_type_s": self.get_item_type_display()
            .lower()
            .replace(" ", "-"),  # full-work, excerpt, or article
            "book_journal_s": self.book_journal,
        }

    def remove_from_index(self):
        """Remove the current work and associated pages from Solr index"""
        # Default parasolr logic only removes current item record;
        # we need to remove associated pages as well
        logger.debug(
            "Deleting DigitizedWork and associated pages from index with group_id %s",
            self.index_id(),
        )
        self.solr.update.delete_by_query('group_id_s:("%s")' % self.index_id())

    def count_pages(self, ptree_client=None):
        """Count the number of pages for a digitized work. If a pages are specified
        for an excerpt or article, page count is determined based on the number of pages
        in the combined ranges. Otherwise, page count is based on the
        number of files in the zipfile within the pairtree content (Hathi-specific).
        Raises :class:`pairtree.storage_exceptions.ObjectNotFoundException`
        if the data is not found in the pairtree storage. Returns page count
        found; saves the object if the count changes."""

        # if this item has a page span defined, calculate number of pages
        # based on the number of pages across all spans
        if self.page_span:
            return len(self.page_span)

        if not self.source == DigitizedWork.HATHI:
            raise storage_exceptions.ObjectNotFoundException(
                "Using Hathi-specific page count for non-Hathi item"
            )

        if not ptree_client:
            ptree_client = self.hathi.pairtree_client()

        # count the files in the zipfile
        start = time.time()
        # could raise pairtree exception, but allow calling context to catch
        with ZipFile(self.hathi.zipfile_path(ptree_client)) as ht_zip:
            # some aggregate packages retrieved from Data API
            # include jp2 and xml files as well as txt; only count text
            page_count = len(
                [
                    filename
                    for filename in ht_zip.namelist()
                    if filename.endswith(".txt")
                ]
            )
            logger.debug(
                "Counted %d pages in zipfile in %f sec", page_count, time.time() - start
            )
        # NOTE: could also count pages via mets file, but that's slower
        # than counting via zipfile name list

        # store page count in the database if changed
        if self.page_count != page_count:
            self.page_count = page_count
            self.save()

        return page_count

    @property
    def page_span(self):
        # convert the specified page numbers into an intspan
        # if empty, returns an empty set
        return intspan(self.pages_digital)

    def get_metadata(self, metadata_format):
        """Get metadata for this item in the specified format.
        Currently only supports marc."""
        if metadata_format == "marc":
            # get metadata from hathi bib api and serialize
            # as binary marc
            if self.source == DigitizedWork.HATHI:
                bib_api = HathiBibliographicAPI()
                bibdata = bib_api.record("htid", self.source_id)
                return bibdata.marcxml.as_marc()

            if self.source == DigitizedWork.GALE:
                # get record from local marc pairtree storage using ESTC id
                # (stored as record id)
                try:
                    record = get_marc_record(self.record_id)
                    # specify encoding to avoid errors
                    record.force_utf8 = True
                    return record.as_marc()
                except MARCRecordNotFound:
                    logger.warning(
                        "MARC record for %s/%s not found"
                        % (self.source_id, self.record_id)
                    )
                    return ""

            return ""

        # error for unknown
        raise ValueError("Unsupported format %s" % metadata_format)

    def get_source_link_label(self):
        """Source-specific label for link on public item detail view."""
        if self.source == DigitizedWork.GALE:
            return "View on Gale Primary Sources"
        if self.source == DigitizedWork.OTHER:
            return "View external record"
        return "View on %s" % self.get_source_display()

    @staticmethod
    def add_from_hathi(htid, bib_api=None, update=False, log_msg_src=None, user=None):
        """Add or update a HathiTrust work in the database.
        Retrieves bibliographic data from Hathi api, retrieves or creates
        a :class:`DigitizedWork` record, and populates the metadata if
        this is a new record, if the Hathi metadata has changed, or
        if update is requested. Creates admin log entry to document
        record creation or update.

        Raises :class:`ppa.archive.hathi.HathiItemNotFound` for invalid
        id.

        Returns the new or updated  :class:`~ppa.archive.models.DigitizedWork`.

        :param htid: HathiTrust record identifier
        :param bib_api: optional :class:`~ppa.archive.hathi.HathiBibliographicAPI`
            instance, to allow for shared sessions in scripts
        :param update: update bibliographic metadata even if the hathitrust
            record is not newer than the local database record (default: False)
        :param log_msg_src: source of the change to be used included
            in log entry messages (optional). Will be used as "Created/updated
            [log_msg_src]".
        :param user: optional user responsible for the change,
            to be associated with :class:`~django.admin.models.LogEntry`
            record
        """

        # initialize new bibliographic API if none is passed in
        bib_api = bib_api or HathiBibliographicAPI()

        # set a default log message source if not specified
        log_msg_src = log_msg_src or "from HathiTrust bibliographic data"

        # get bibliographic data for this record from Hathi api
        # - needed to check if update is required for existing records,
        #   and to populate metadata for new records

        # could raise HathiItemNotFound for invalid id
        bibdata = bib_api.record("htid", htid)

        # if hathi id is valid and we have bibliographic data, create
        # a new record

        # find existing record or create a new one
        digwork, created = DigitizedWork.objects.get_or_create(source_id=htid)

        # get configured script user for log entries if no user passed in
        if not user:
            user = User.objects.get(username=settings.SCRIPT_USERNAME)

        # if this is an existing record, check if updates are needed
        source_updated = None
        if not created and not update:
            source_updated = bibdata.copy_last_updated(htid)
            if digwork.updated.date() > source_updated:
                # local copy is newer than last source modification date
                # and update is not requested; return un modified
                return digwork

        # populate digitized item in the database
        digwork.populate_from_bibdata(bibdata)
        digwork.save()

        # create a log entry to document record creation or change
        # if created, action is addition and message is creation
        log_change_message = "Created %s" % log_msg_src
        log_action = ADDITION
        # if this was not a new record, log as an update
        if not created:
            # create log entry for updating an existing record
            # include details about why the update happened if possible
            if update:
                msg_detail = " (forced update)"
            else:
                msg_detail = "; source record last updated %s" % source_updated
            log_change_message = "Updated %s%s" % (log_msg_src, msg_detail)
            log_action = CHANGE

        # create log entry for record creation
        LogEntry.objects.log_action(
            user_id=user.id,
            content_type_id=ContentType.objects.get_for_model(digwork).pk,
            object_id=digwork.pk,
            object_repr=str(digwork),
            change_message=log_change_message,
            action_flag=log_action,
        )

        return digwork


class Page(Indexable):
    """Indexable for pages to make page data available for indexing with
    parasolr index manage command."""

    @classmethod
    def items_to_index(cls):
        """Return a generator of page data to be indexed, with data for
        pages for each work returned by :meth:`Page.page_index_data`
        """
        for work in DigitizedWork.items_to_index():
            for page_data in Page.page_index_data(work):
                yield page_data

    @classmethod
    def total_to_index(cls):
        """Calculate the total number of pages to be indexed by
        aggregating page count of items to index in the database."""
        return (
            DigitizedWork.items_to_index().aggregate(
                total_pages=models.Sum("page_count")
            )["total_pages"]
            or 0
        )

    @classmethod
    def index_item_type(cls):
        """index item type for parasolr indexing script"""
        return "page"

    @classmethod
    def page_index_data(cls, digwork):
        """Get page content for the specified digitized work from Hathi
        pairtree and return data to be indexed in solr."""

        # Only index pages fo ritems that are not suppressed
        if not digwork.is_suppressed:
            # get index page data based on the source
            if digwork.source == digwork.HATHI:
                return cls.hathi_page_index_data(digwork)
            if digwork.source == digwork.GALE:
                return cls.gale_page_index_data(digwork)

        # return an empty list for anything else
        return []

    @classmethod
    def hathi_page_index_data(cls, digwork):
        """Get page content for the specified digitized work from Hathi
        pairtree and return data to be indexed in solr."""

        # load mets record to pull metadata about the images
        try:
            mmets = load_xmlobject_from_file(digwork.hathi.metsfile_path(), MinimalMETS)
        except storage_exceptions.ObjectNotFoundException:
            logger.error(
                "Pairtree data for %s not found but status is %s",
                digwork.source_id,
                digwork.get_status_display(),
            )
            return

        # get page span from digitized work
        page_span = digwork.page_span
        digwork_index_id = digwork.index_id()

        # read zipfile contents in place, without unzipping
        with ZipFile(digwork.hathi.zipfile_path()) as ht_zip:

            # yield a generator of index data for each page; iterate
            # over pages in METS structmap
            for i, page in enumerate(mmets.structmap_pages, 1):
                # if the document has a page range defined, skip any pages not in range
                if page_span and i not in page_span:
                    continue
                # zipfile spec uses / for path regardless of OS
                pagefilename = "/".join(
                    [digwork.hathi.content_dir, page.text_file_location]
                )
                with ht_zip.open(pagefilename) as pagefile:
                    try:
                        yield {
                            "id": "%s.%s" % (digwork_index_id, page.text_file.sequence),
                            "source_id": digwork.source_id,
                            "group_id_s": digwork_index_id,  # for grouping with work record
                            "content": pagefile.read().decode("utf-8"),
                            "order": page.order,
                            "label": page.display_label,
                            "tags": page.label.split(", ") if page.label else [],
                            "item_type": "page",
                        }
                    except StopIteration:
                        return

    @classmethod
    def gale_page_index_data(cls, digwork, gale_record=None):
        """Get page content for the specified digitized work from Gale
        API and return data to be indexed in solr. Takes an optional gale_record
        parameter (item record as returned by Gale API), to avoid
        making an extra API call if data is already available."""
        if gale_record is None:
            gale_record = GaleAPI().get_item(digwork.source_id)

        # get page span from digitized work
        page_span = digwork.page_span
        digwork_index_id = digwork.index_id()

        for i, page in enumerate(gale_record["pageResponse"]["pages"], 1):
            page_number = page["pageNumber"]
            # folio number not yet set for all volumes; fallback to page number
            page_label = page.get("folioNumber", int(page_number))
            # if the document has a page range defined, skip any pages not in range
            if page_span and i not in page_span:
                continue
            yield {
                "id": "%s.%s" % (digwork_index_id, page_number),
                "source_id": digwork.source_id,
                "group_id_s": digwork_index_id,  # for grouping with work record
                "content": page.get("ocrText"),  # some pages have no text
                "order": i,
                "label": page_label,
                "item_type": "page",
                # image id needed for thumbnail url; use solr dynamic field
                "image_id_s": page["image"]["id"],
            }
