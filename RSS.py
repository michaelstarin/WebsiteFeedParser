__author__ = 'michaelstarin'

import feedparser
import time
import pickle
import logging


class RSSReader():
    def __init__(self, feed_url, output_file_name, refresh_rate=1200):
        self.url = feed_url
        self.file_name = output_file_name
        self.refresh_rate = refresh_rate
        self._running = True
        self._feed_data = []
        self._etag = None
        self._last_fetch = None
        #writes logging info to a file
        #logging.basicConfig(filename='rss_logging_file', filemode='w', level=logging.INFO)
        #prints logging info on the screen
        logging.basicConfig(level=logging.INFO)

    def _request_data(self):
        if self._etag:
            logging.info("\tLooking for updated feed using 'eTag': %s" % self._etag)
            return feedparser.parse(self.url, etag=self._etag)
        elif self._last_fetch:
            logging.info("\tLooking for updated feed using 'modified': %s" % self._last_fetch)
            return feedparser.parse(self.url, modified=self._last_fetch)
        else:
            logging.info("\tLooking for updated feed without eTag/modified")
            return feedparser.parse(self.url)

    def _update_feed(self, feed):
        if (feed.has_key('modified') and self._last_fetch != feed.modified) or \
            (feed.has_key('etag') and self._etag != feed.etag):
            #The feed has been updated!

            logging.info("\tNew data was fetched")
            if feed.has_key('etag'):
                self._etag = feed.etag
                logging.info("\tEtag: %s" % self._etag)
            if feed.has_key('modified'):
                self._last_fetch = feed.modified
                logging.info("\tLast Fetch: %s" % self._last_fetch)
            self._feed_data.append(feed)
            logging.info("\tProcessing: " + self.url)
            return True
        return False

    def store(self):
        if not self._feed_data:
            return False
        write_file = open(self.file_name, 'ab')
        pickle.dump(self._feed_data, write_file)
        write_file.close()
        self._feed_data = []
        return True

    def fetch_from_store(self):
        read_file = open(self.file_name, 'rb')
        self._feed_data += pickle.load(read_file)
        read_file.close()

    def fetch(self):
        feed = self._request_data()
        self._update_feed(feed)

    def terminate(self):
        self._running = False

    def running(self):
        return self._running

    def run_it(self):
        print('started new rss feed on ', self.url)
        while True:
            newest_feed = self._request_data()
            if not self._update_feed(newest_feed):
                n = 0
                while self._running and n < self.refresh_rate:
                    time.sleep(1)
                    n += 1
            else:
                self.store()






