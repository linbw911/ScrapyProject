# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PcautoItem(scrapy.Item):
	comments_id = scrapy.Field()
	source_id = scrapy.Field()
	classification = scrapy.Field()
	cars = scrapy.Field()
	dealer = scrapy.Field()
	model = scrapy.Field()
	time = scrapy.Field()
	price = scrapy.Field()
	site = scrapy.Field()
	score = scrapy.Field()
	ownner_impression = scrapy.Field()
	comment = scrapy.Field()
	request_url = scrapy.Field()
	response_url = scrapy.Field()

