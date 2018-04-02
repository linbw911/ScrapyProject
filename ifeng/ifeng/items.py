# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IfengItem(scrapy.Item):
    news_website_id = scrapy.Field()
    cmt_id = scrapy.Field()
    pub_time = scrapy.Field()
    content = scrapy.Field()
    title = scrapy.Field()
    response_url = scrapy.Field()
    source_url = scrapy.Field()