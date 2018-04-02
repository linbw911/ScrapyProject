# -*- coding: utf-8 -*-
from __future__ import absolute_import

import re
import time
import json
import scrapy
from urlparse import urljoin
from bs4 import BeautifulSoup
from wyauto.items import WyautoItem


class WyautoSpiderSpider(scrapy.Spider):
    name = 'wyauto_spider'
    source_id = 4
    data_path = './data/wyauto'
    cache = './cache/wyauto.cache'
    cache_size = 20
    comparsse_size = 10000
    start_urls = ['http://product.auto.163.com/price']

#    def start_requests(self):
#    	start_urls = ['http://product.auto.163.com/price']
#    	for url in start_urls:
#    		yield scrapy.Request(url=url, callback=self.get_price_list)
#    		break

    def parse(self, response):
    	for url in response.css('div.bd li.title a::attr(href)').extract():
    		url = urljoin('http://product.auto.163.com', url)
    		yield scrapy.Request(url=url, callback=self.parse_car_list)

    def parse_car_list(self, response):
    	for url in response.css('h5 a::attr(href)').extract():
    		url = urljoin('http://product.auto.163.com', url)
    		yield scrapy.Request(url=url, callback=self.parse_comment_list)

    def parse_comment_list(self, response):
    	url = response.css('li a[href*="review"]::attr(href)').extract()[1]
    	url = urljoin('http://product.auto.163.com', url)
    	yield scrapy.Request(url=url, callback=self.parse_comment_more)

    def parse_comment_more(self, response):
    	url = response.css('div#wangyoudianping a.more::attr(href)').extract_first()
    	url = urljoin('http://product.auto.163.com',url)
    	yield scrapy.Request(url=url, callback=self.parse_comment, meta={
    			'data':{
    				'request_url': url
    			}
    		})

    def parse_comment(self, response):
    	model = response.css('h1 a::text').extract_first()
    	for i in response.css('div.commentSingle.commentSingle-main'):
            body_more = i.css('a.body-more::attr(href)').extract_first()
            title = i.css('h3 a::text').extract_first()
            author = i.css('span.author::text').extract_first() + i.css('span.author strong::text').extract_first()
            #author = i.css('span.author::text').extract_first() + i.css('span.author strong::text').extract_first()
            time = i.css('span.postTime::text').extract_first()[:-3]
    		#body_more = i.css('a.body-more::attr(href)').extract_first()
            if body_more:
                url = urljoin('http://product.auto.163.com', body_more)
                yield scrapy.Request(url=url, callback=self.parse_body_more, meta={
    					'data':{
    						'model': model,
    						'title': title,
    						'request_url': response.meta['data']['request_url']

    					}
    				})
            else:
    			body = i.css('div.comBody::text').extract_first()
    			response.meta['data'].update({
    					
    				    'model': model,
    					'title': title,
    				    'body': body,
                        'author': author,
                        'time': time,
    				    'response_url': unicode(response.url)
    					
    				})
    			
    			yield WyautoItem(response.meta['data'])

    	if(len(response.css('div.comment-pages a::text').extract()) == 0 or response.css('div.comment-pages a::text').extract()[-1].isnumeric()):
    		nextpage = 0
    	else:
    		nextpage = response.css('div.comment-pages a::attr(href)').extract()[-1]

    	if nextpage:
    		url = urljoin('http://product.auto.163.com',nextpage)
    		yield scrapy.Request(url=url, callback=self.parse_comment, meta={
    				'data':{
    					'request_url': url
    				}
    			})

    def parse_body_more(self, response):
    	body = response.css('div.d3::text').extract()
        author = response.css('span.author::text').extract_first() + response.css('span.author strong::text').extract_first()
        time = response.css('span.time::text').extract_first()[:-3]
    	#body = re.sub('<br>[\w\W]*$', '', body)
    	response.meta['data'].update({
    			'body': body,
    			'response_url': unicode(response.url)
    		})

    	yield WyautoItem(response.meta['data'])




