# -*- coding: utf-8 -*-

# Scrapy settings for cmc project

BOT_NAME = 'cmc'

SPIDER_MODULES = ['cmc.spiders']
NEWSPIDER_MODULE = 'cmc.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'cmc crawler'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Disable cookies
COOKIES_ENABLED = False

# Disable Telnet Console
TELNETCONSOLE_ENABLED = False

# Configure item pipelines
ITEM_PIPELINES = {
    'cmc.pipelines.ConvertLastUpdatedPipeline': 300,
    'cmc.pipelines.RemovePercentSignPipeline': 350,
    'cmc.pipelines.RequiredFieldsPipeline': 400,
    'cmc.pipelines.MySQLStorePipeline': 500,
}

# Configure database connection
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'cmcbot'
MYSQL_USER = 'cmcbot'
MYSQL_PASSWD = 'L14bc$$cm0'
