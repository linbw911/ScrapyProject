# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WyautoItem(scrapy.Item):
    comments_id = scrapy.Field()
    source_id = scrapy.Field()
    model = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
    request_url = scrapy.Field()
    response_url = scrapy.Field()