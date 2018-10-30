from unittest.mock import patch, Mock

from django.contrib.admin.sites import AdminSite
from django.http import HttpResponseRedirect
from django.test import TestCase, override_settings, RequestFactory
from django.urls import reverse

from ppa.archive.admin import DigitizedWorkAdmin
from ppa.archive.models import DigitizedWork, Collection

TEST_SOLR_CONNECTIONS = {
    'default': {
        'COLLECTION': 'testppa',
        'URL': 'http://localhost:191918984/solr/',
        'ADMIN_URL': 'http://localhost:191918984/solr/admin/cores'
    }
}


class TestDigitizedWorkAdmin(TestCase):

    fixtures = ['sample_digitized_works']

    def setUp(self):
        self.factory = RequestFactory()

    def test_list_collections(self):
        # set up preliminary objects needed to test an admin site object
        site = AdminSite()
        digadmin = DigitizedWorkAdmin(DigitizedWork, site)

        # no collections should return an empty string
        digwork = DigitizedWork.objects.create(source_id='njp.32101013082597')
        coll_list = digadmin.list_collections(digwork)
        assert coll_list == ''

        # create two collections and set them on digwork
        Z = Collection.objects.create(name='Z Collection')
        A = Collection.objects.create(name='A Collection')
        C = Collection.objects.create(name='C Collection')

        digwork.collections.set([Z, A, C])

        # should now return an alphabetized, comma separated list
        coll_list = digadmin.list_collections(digwork)
        assert coll_list == 'A Collection, C Collection, Z Collection'

    def test_source_link(self):
        # set up preliminary objects needed to test an admin site object
        site = AdminSite()
        digadmin = DigitizedWorkAdmin(DigitizedWork, site)
        # create digitalwork with a source_id and source_url
        # test and method assume that we can always count on these
        fake_url='http://obviouslywrongurl.org/njp.32101013082597'
        digwork = DigitizedWork.objects.create(
            source_id='njp.32101013082597',
            source_url=fake_url
        )
        snippet = digadmin.source_link(digwork)
        assert snippet == \
            '<a href="%s" target="_blank">njp.32101013082597</a>' % fake_url


    @override_settings(SOLR_CONNECTIONS=TEST_SOLR_CONNECTIONS)
    @patch('ppa.archive.solr.get_solr_connection')
    @patch('ppa.archive.models.DigitizedWork.index')
    def test_save_related(self, mockindex, mock_get_solr_connection):
        '''Test that override of save_related calls index'''
        # fake request
        request = self.factory.get('/madeup/url')
        # fake adminsite
        site = AdminSite()
        # make a digital work to get in overridden method
        digwork = DigitizedWork.objects.create(source_id='njp.32101013082597')
        # mocked form
        form = Mock()
        form.instance.pk = digwork.pk
        form.save_m2m = Mock()
        digadmin = DigitizedWorkAdmin(DigitizedWork, site)
        # call save_related using mocks for most params we don't use or need
        digadmin.save_related(request, form, [], False)
        # mocked index method of the digwork object should have been called
        digwork.index.assert_called_with(params={'commitWithin': 10000})

    def test_bulk_add_collection(self):
        # create a DigitizedWorkAdmin object
        digworkadmin = DigitizedWorkAdmin(DigitizedWork, AdminSite())
        fakerequest = Mock()
        fakerequest.session = {}
        # set some arbitary querystring filters
        fakerequest.GET = {'q': 1, 'foo': 'bar'}
        queryset = DigitizedWork.objects.all()
        redirect = digworkadmin.bulk_add_collection(fakerequest, queryset)
        # should return a redirect
        assert isinstance(redirect, HttpResponseRedirect)
        # url should reverse the appropriate route
        assert redirect.url == reverse('archive:add-to-collection')
        # session on request should be set with a key called collection-add-ids
        # that is not empty
        assert fakerequest.session['collection-add-ids']
        # the key should have the ids of the three fixtures
        assert set(fakerequest.session['collection-add-ids']) == \
            set(queryset.values_list('id', flat=True))
        # the querystring should have been faithfully copied to session as well
        assert fakerequest.session['collection-add-filters'] == fakerequest.GET
        redirect = digworkadmin.bulk_add_collection(fakerequest, queryset)
        # test against an empty queryset just in case
        DigitizedWork.objects.all().delete()
        queryset = DigitizedWork.objects.all()
        redirect = digworkadmin.bulk_add_collection(fakerequest, queryset)
        # session variable should be set to an empty list
        assert fakerequest.session['collection-add-ids'] == []
