# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IfengCommentItem(scrapy.Item):
    news_id = scrapy.Field()
    content = scrapy.Field()
    good_number = scrapy.Field()
    user_id = scrapy.Field()
    location = scrapy.Field()
    comment_time  = scrapy.Field()
    comment_id = scrapy.Field()
    response_url = scrapy.Field()
