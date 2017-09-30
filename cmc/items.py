# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CmcItem(scrapy.Item):
    name = scrapy.Field()
    ticker = scrapy.Field()
    pair = scrapy.Field()
    exchange = scrapy.Field()
    price_usd = scrapy.Field()
    price_btc = scrapy.Field()
    volume_usd = scrapy.Field()
    volume_btc = scrapy.Field()
    market_percent = scrapy.Field()
    last_updated = scrapy.Field()