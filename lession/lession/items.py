# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class LessionItem(scrapy.Item):
    news_id = scrapy.Field()
    source_id = scrapy.Field()
    language = scrapy.Field()
    request_url = scrapy.Field()
    response_url = scrapy.Field()
    title = scrapy.Field()
    classification = scrapy.Field()
    abstract = scrapy.Field()
    body = scrapy.Field()
    pub_time = scrapy.Field()
    cole_time = scrapy.Field()
    out_links = scrapy.Field()
    images = scrapy.Field()
    html = scrapy.Field()