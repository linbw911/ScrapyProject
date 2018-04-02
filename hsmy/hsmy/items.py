# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HsmyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    request_url = scrapy.Field()
    pub_time = scrapy.Field()
    title = scrapy.Field()
    response_url = scrapy.Field()
    STI = scrapy.Field()
    Southeast_Asia = scrapy.Field()
    South_Asia = scrapy.Field()
    Middle_East = scrapy.Field()
    Red_Sea = scrapy.Field()
    Central_Eastern_Europe = scrapy.Field()
    STI_Container = scrapy.Field()
    STI_Bulk = scrapy.Field()
    STI_Liquid = scrapy.Field()
    report_id = scrapy.Field()
    source_id = scrapy.Field()
