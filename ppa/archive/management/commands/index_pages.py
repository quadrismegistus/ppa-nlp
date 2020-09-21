'''
Custom multiprocessing Solr index script for page index data.
'''

import queue
from multiprocessing import Process, Queue, cpu_count
from time import sleep

from django.core.management.base import BaseCommand
from parasolr.django import SolrClient, SolrQuerySet
import progressbar

from ppa.archive.models import DigitizedWork, Page


def page_index_data(work_q, page_data_q):
    '''Function to generate page index data and add it to
    a queue. Takes a queue with digitized works to generate pages
    for and a queue where page data will be added.'''
    while True:
        try:
            digwork = work_q.get(True, 1)
            # convert to the generator to a list
            # — might be nice to chunk, but most books are small
            # enough it doesn't matter that much
            page_data_q.put(list(Page.page_index_data(digwork)))
        except queue.Empty:
            # worker is done when the work queue is empty
            return


def process_index_queue(index_data_q, total_to_index, work_q):
    '''Function to send index data to Solr. Takes a
    queue to poll for index data, a total of the items
    to be indexed (for use with progess bar), and a work queue
    as a way of checking that all indexing is complete.'''

    solr = SolrClient()
    progbar = progressbar.ProgressBar(redirect_stdout=True,
                                      max_value=total_to_index)
    count = 0
    while True:
        try:
            # get data from the queue and put it into Solr
            # block with a timeout
            index_data = index_data_q.get(timeout=5)
            solr.update.index(index_data)
            # increase count based on the number of items in the list
            count += len(index_data)
            progbar.update(count)
        except queue.Empty:
            # only end if work q is also empty; otherwise, loop again
            # indexer has just gotten ahead of page index data
            if work_q.empty():
                progbar.finish()

                # print a summary of solr totals by item type
                facets = SolrQuerySet().all().facet('item_type').get_facets()
                item_totals = []
                for item_type, total in facets.facet_fields.item_type.items():
                    item_totals.append('%d %s%s' % (
                        total, item_type, '' if total == 1 else 's'))
                print('\nItems in Solr by item type: %s' %
                      (', '.join(item_totals)))

                # finish indexing process
                return


class Command(BaseCommand):
    '''Index page data in Solr (multiprocessor implementation)'''
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument(
            '--cpus', default=cpu_count(), type=int,
            help='Number of CPUs to use (cpu_count by default: %(default)s)')

    def handle(self, *args, **kwargs):
        work_q = Queue()
        page_data_q = Queue()

        # populate the work queue with digitized works that have
        # page content to be indexed
        for digwork in DigitizedWork.items_to_index():
            work_q.put(digwork)

        # start multiple processes to populate the page index data queue
        for i in range(kwargs['cpus'] - 1):
            Process(
                target=page_index_data, args=(work_q, page_data_q)).start()

        # give the page data a head start, since indexing is faster
        sleep(10)
        # start a single indexing process
        Process(target=process_index_queue,
                args=(page_data_q, Page.total_to_index(), work_q)).start()
