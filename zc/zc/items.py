# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZcItem(scrapy.Item):
	title = scrapy.Field()
	url = scrapy.Field()
	inputtime = scrapy.Field()
	source_id = scrapy.Field()
	response_url = scrapy.Field()
	policy_id = scrapy.Field()
	classifications = scrapy.Field()
	request_url = scrapy.Field()
	html = scrapy.Field()
	body = scrapy.Field()
	out_links = scrapy.Field()
	cole_time = scrapy.Field()
	language = scrapy.Field()
