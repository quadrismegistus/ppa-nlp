import csv
import logging
from collections import Counter

from django.conf import settings
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError

from ppa.archive.models import DigitizedWork, Page

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Import Group IDs for records already in the system"""

    help = __doc__

    stats = None
    #: normal verbosity level
    v_normal = 1
    verbosity = v_normal

    required_fields = [
        "Source ID",
        "UNIQUE ID",
        "Pages (digital)",
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            "csv",
            help="CSV file with records and group ids for import",
        )

    def handle(self, *args, **kwargs):
        data = self.load_csv(kwargs["csv"])

        self.verbosity = kwargs.get("verbosity", self.v_normal)
        self.script_user = User.objects.get(username=settings.SCRIPT_USERNAME)
        self.digwork_contentype = ContentType.objects.get_for_model(DigitizedWork)

        for row in data:
            # - find the correct record
            # use an unsaved digitized work to parse the page range for search filter
            dw_pages = DigitizedWork(
                pages_digital=row["Pages (digital)"].replace(";", ",")
            )
            try:
                digwork = DigitizedWork.objects.get(
                    source_id=row["Source ID"], pages_digital=dw_pages.pages_digital
                )
                if self.verbosity > self.v_normal:
                    print(digwork)
            except DigitizedWork.DoesNotExist:
                # TODO: count missing and report
                self.stdout.write(
                    self.style.WARNING(
                        "%s%s not found"
                        % (
                            row["Source ID"],
                            " (%s)" % dw_pages.pages_digital
                            if dw_pages.pages_digital
                            else "",
                        )
                    )
                )
                # skip to next row
                continue

            # set the group id
            digwork.group_id = row["UNIQUE ID"]
            # save if changed
            if digwork.has_changed("group_id"):
                digwork.save()

                # create a log entry
                LogEntry.objects.log_action(
                    user_id=self.script_user.pk,
                    content_type_id=self.digwork_contentype.pk,
                    object_id=digwork.pk,
                    object_repr=str(digwork),
                    change_message="Set group ID via CSV",
                    action_flag=CHANGE,
                )

            # reindex pages to ensure they have the new group id
            # TODO: maybe optional?
            digwork.index_items(Page.page_index_data(digwork))

    # NOTE: adapted from gale_import script
    def load_csv(self, path):
        """Load a CSV file with items to be imported."""
        try:
            with open(path, encoding="utf-8-sig") as csvfile:
                csvreader = csv.DictReader(csvfile)
                data = [row for row in csvreader]
        except FileNotFoundError:
            raise CommandError("Error loading the specified CSV file: %s" % path)

        header_row = data[0].keys()
        for field in self.required_fields:
            if field not in header_row:
                raise CommandError("%s column is required in CSV file" % field)
        return data
