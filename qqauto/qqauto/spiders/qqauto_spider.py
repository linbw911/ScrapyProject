# -*- coding: utf-8 -*-
from __future__ import absolute_import

import re
import time
import json
import scrapy
from urlparse import urljoin
from bs4 import BeautifulSoup
from qqauto.items import QqautoItem


class QqautoSpiderSpider(scrapy.Spider):
    name = 'qqauto_spider'
    source_id = 3
    data_path = './data/qqauto'
    cache = './cache/qqauto.cache'
    cache_size = 20
    comparsse_size = 10000
    start_urls = [
        'http://data.auto.qq.com/car_public/1/serial_style_1.shtml',
        'http://data.auto.qq.com/car_public/1/serial_style_2.shtml',
        'http://data.auto.qq.com/car_public/1/serial_style_3.shtml',
        'http://data.auto.qq.com/car_public/1/serial_style_4.shtml',
        'http://data.auto.qq.com/car_public/1/serial_style_5.shtml',
        'http://data.auto.qq.com/car_public/1/serial_style_6.shtml',
        'http://data.auto.qq.com/car_public/1/serial_style_7.shtml',
        'http://data.auto.qq.com/car_public/1/serial_style_8.shtml',
        'http://data.auto.qq.com/car_public/1/serial_style_9.shtml'

    ]


    def parse(self, response):
        yield scrapy.Request(url=response.url, callback=self.parse_car_list)

    def parse_car_list(self, response):
    	for i in response.css('div[style="display: block;"] a[href*="car_serial"]::attr(href)').extract():
    		url = urljoin('http://data.auto.qq.com', i)
    		yield scrapy.Request(url=url, callback=self.parse_comment_list)

    def parse_comment_list(self,response):
    	url = response.css('div#side_review_list h4 a[href*="serial"]::attr(href)').extract_first()[:-16]
    	yield scrapy.Request(url=url, callback=self.parse_all)

    def parse_all(self, response):
    	lookall = response.css('div.lookall.lan1 a::attr(href)').extract_first()
    	if lookall:
    		url = urljoin('http://cgi.data.auto.qq.com/php/',lookall)
    		yield scrapy.Request(url=url, callback=self.parse_comment,meta={
    				'data':{
    					'request_url': url
    				}
    			})
    	else:
    		url = response.url
    		yield scrapy.Request(url=url, callback=self.parse_comment, meta={
    				'data':{
    					'request_url': url
    				}
    			})

    def parse_comment(self, response):
    	model = response.css('a.nav_two_level_a_b::text').extract_first()
    	if(len(response.css('div#pjxq').extract())):
    		for i in response.css('div.pt-list.cl'):
    			title = i.css('h3 a::text').extract_first()
    			time = i.css('span.date::text').extract_first()
                body = {
                    i.css('dt.yd::text').extract_first(): i.css('dt.yd~dd::text').extract_first(),
                    i.css('dt.qd::text').extract_first(): i.css('dt.qd~dd::text').extract_first(),
                    i.css('dt.zs::text').extract_first(): i.css('dt.zs~dd::text').extract_first()

                }
                body = i.css('dl.yqlist.cl dd::text').extract()
                response.meta['data'].update({
    					
    					'title': title,
    					'time': time,
    					'body': body,
    					'model': model,
    					'response_url': unicode(response.url)
    					
    				})
                yield QqautoItem(response.meta['data'])

    		nextpage = response.css('a#g_auto_next_page::attr(href)').extract_first()
    		if nextpage:
    			url = urljoin('http://cgi.data.auto.qq.com/php/', nextpage)
    			yield scrapy.Request(url=url, callback=self.parse_comment, meta={
                        'data':{
                            'request_url':url
                        }
                    }) 



    	
    		