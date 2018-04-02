# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QqautoItem(scrapy.Item):
    comments_id = scrapy.Field()
    source_id = scrapy.Field()
    title = scrapy.Field()
    model = scrapy.Field()
    body = scrapy.Field()
    time = scrapy.Field()
    request_url = scrapy.Field()
    response_url = scrapy.Field()
    
