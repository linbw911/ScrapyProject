# -*- coding: utf-8 -*-

from __future__ import absolute_import

import re
import time
import json
import scrapy
from urlparse import urljoin
#from bs4 import BeautifulSoup
from lession.items import LessionItem

class LessionSpider(scrapy.Spider):
	name = 'lession'
	source_id = 1
	language = 'ind'
	data_path = './data/antaranews'
	cache = './cache/antaranews.cache'
	cache_size = 20
	comparsse_size = 10000

	def start_requests(self):
		classifications = {
			'ekonomi': 'http://www.antaranews.com/ekonomi'
		}

		for classification, url in classifications.items():
			yield scrapy.Request(url=url, callback=self.get_news_list, meta={
					'data': {
						'classification': classification
					}
				})
			break

	def get_news_list(self, response):
		for i in response.css('.ul_rubrik li'):
			url = i.css('a::attr(href)').extract_first()
			url = urljoin(response.url, url)
			yield scrapy.Request(url=url, callback=self.get_news, meta={
					'data': {
						'classification': response.meta['data']['classification'],
						'request_url': url,
						'title': i.css('a.box_link2::text').extract_first(),
						'pub_time': i.css('div.date time::attr(datetime)').extract_first(),
						'abstract': i.css('div.indes::text').extract_first()
					}
				})
#			return
		nextpage = response.css('#container .pagination a').re('<a href="(.*?)">Next</a>')
		if nextpage:
			url = urljoin(response.url, nextpage[0])
			yield scrapy.Request(url = url, callback = self.get_news_list, meta={
					'data':response.meta['data']
				})

	def get_news(self, response):
		body = response.css('div#content_news').extract_first()
		body = re.sub('<b>[\w\W]*$', '', body)
		image = response.css('div#image_news')
		response.meta['data'].update({
				'body': re.sub('<p class="mt10">[\w\W]*$', '', body),
				'response_url': unicode(response.url),
				'out_links': response.css('a::attr(href)').extract(),
				'images': [{
					'src': image.css('img::attr(src)').extract_first(),
					'description': image.css('div#caption_news::text').extract_first()
				}] if image else [],
				'html': response.body_as_unicode()
			})
		yield LessionItem(response.meta['data'])