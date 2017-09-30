# -*- coding: utf-8 -*-

# CMCBot Pipelines

from scrapy.exceptions import DropItem
from time import time, gmtime, strftime
from datetime import datetime
from hashlib import md5
from scrapy import log
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
import logging

class ConvertLastUpdatedPipeline(object):
    """ Converts the cmc n hours ago to n hours before the item was scraped in mysql datetime format """
    
    def process_item(self, item, spider):
            
        if item['last_updated']:
            updated = item['last_updated'][0]
            seconds = 0
            if updated != 'Recently':
                print("Exchange " + item['exchange'][0] + " for pair " + item['pair'][0] + " was updated " + updated);
                seconds = int(updated.replace(' hours ago', '').replace(' hour ago', '')) * 3600
            last_updated = time() - seconds
            item['last_updated'] = strftime('%Y-%m-%d %H:%M:%S', gmtime(last_updated))
            return item
        else:
            raise DropItem("Missing last_updated in %s" % item)
     
class RemovePercentSignPipeline(object):
    """ Removes % from percentage """
    
    def process_item(self, item, spider):    
        if item['market_percent']:
            item['market_percent'] = item['market_percent'][0].replace('%', '')
            return item
        else:
            raise DropItem("Missing last_updated in %s" % item)
            
class RequiredFieldsPipeline(object):
    """Ensures the item have the required fields."""

    required_fields = ('ticker', 'pair', 'exchange', 'price_usd', 'price_btc', 'volume_usd', 'volume_btc', 'market_percent', 'last_updated')

    def process_item(self, item, spider):
        for field in self.required_fields:
            if not item.get(field):
                raise DropItem("Field '%s' missing: %r" % (field, item))
        return item
        
class MySQLStorePipeline(object):
    """A pipeline to store the item in a MySQL database.
    This implementation uses Twisted's asynchronous database API.
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        # run db query in the thread pool
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d

    def _do_upsert(self, conn, item, spider):
        """Perform an insert or update."""
        guid = self._get_guid(item)
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')

        conn.execute("""SELECT EXISTS(
            SELECT 1 FROM markets WHERE guid = %s
        )""", (guid, ))
        ret = conn.fetchone()[0]

        if ret:
            conn.execute("""
                UPDATE markets
                SET name=%s, ticker=%s, pair=%s, exchange=%s, price_usd=%s, price_btc=%s, 
                    volume_usd=%s, volume_btc=%s, market_percent=%s, last_updated=%s, updated=%s
                WHERE guid=%s
            """, (item['name'], item['ticker'], item['pair'], item['exchange'], item['price_usd'], 
            item['price_btc'], item['volume_usd'], item['volume_btc'], 
            item['market_percent'], item['last_updated'], now, guid))
            logging.log(logging.INFO, "Item updated in db: %s %r", guid, item)
        else:
            conn.execute("""
                INSERT INTO markets (guid, name, ticker, pair, exchange, price_usd, price_btc,
                    volume_usd, volume_btc, market_percent, last_updated, updated)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (guid, item['name'], item['ticker'], item['pair'], item['exchange'], item['price_usd'], 
            item['price_btc'], item['volume_usd'], item['volume_btc'], 
            item['market_percent'], item['last_updated'], now))
            logging.log(logging.INFO, "Item stored in db: %s %r", guid, item)

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        logging.log(logging.ERROR, failure)

    def _get_guid(self, item):
        """Generates an unique identifier for a given item."""
        # hash based in pair, exchange and ticker fields
        return md5((item['pair'][0] + item['exchange'][0] + item['ticker'][0]).encode('utf-8')).hexdigest()
