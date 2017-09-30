# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from cmc.items import CmcItem

class MarketsSpider(scrapy.Spider):
    name = 'markets'
    start_urls = ['http://coinmarketcap.com/']

    def parse(self, response):
        urls = response.xpath('//table[@id="currencies"]//td[@class="no-wrap currency-name"]/a/@href').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_markets);
        
 #       try:
 #           next_page_index = response.css('div.pull-right > ul > li > a::text').extract().index('Next 100  ' + unichr(0x2192))
 #           pagination_urls = response.css('div.pull-right > ul > li > a::attr(href)').extract()
 #           next_page_url = pagination_urls[next_page_index]            
 #           if next_page_url:
 #               next_page_url = response.urljoin(next_page_url)
 #               yield scrapy.Request(url=next_page_url, callback=self.parse)
 #       except:
 #           print("No more pages");
    
    def parse_markets(self, response):
        markets = response.xpath('//table[@id="markets-table"]/tbody/tr')
        name = response.css('h1.text-large > img::attr(alt)').extract_first()
        ticker = response.css('h1.text-large > small::text').extract_first().replace('(', '').replace(')','')
        
        for market in markets:     
            l = ItemLoader(item=CmcItem(), selector=market)
            l.add_value('name', name)
            l.add_value('ticker', ticker)
            l.add_xpath('pair', './/td[3]/a/text()')
            l.add_xpath('exchange', './/td[2]/a/text()')
            l.add_xpath('price_btc', './/td/span[@class="price"]/@data-btc')
            l.add_xpath('price_usd', './/td/span[@class="price"]/@data-usd')
            l.add_xpath('volume_btc', './/td/span[@class="volume"]/@data-btc')
            l.add_xpath('volume_usd', './/td/span[@class="volume"]/@data-usd')
            l.add_xpath('market_percent', './/td[6]/text()')
            l.add_xpath('last_updated', './/td[7]/text()')
            yield l.load_item()
