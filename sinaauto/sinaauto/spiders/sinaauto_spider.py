# -*- coding: utf-8 -*-
from __future__ import absolute_import

import re
import time
import json
import scrapy
from urlparse import urljoin
from bs4 import BeautifulSoup
from sinaauto.items import SinaautoItem


class SinaautoSpiderSpider(scrapy.Spider):
    name = 'sinaauto_spider'
    source_id = 5
    data_path = './data/sinaauto'
    cache = './cache/sinaauto.cache'
    cache_size = 20
    comparsse_size = 10000
    #headers = {"header1":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0"}
    count = True
    start_urls = [
            'http://db.auto.sina.com.cn/list-0-0-0-0-0-0-0-0-9-0-1.html'
    ]

    def parse(self, response):
        yield scrapy.Request(url=response.url, callback=self.parse_car_list)

    def parse_car_list(self, response):
    	for url in response.css('li.fL p.title a::attr(href)').extract():
    		url = urljoin('http:', url)
    		yield scrapy.Request(url=url, callback=self.parse_more_comment)

    	nextpage = response.css('a.next::attr(href)').extract_first()
    	if nextpage:
    		url = urljoin('http:', nextpage)
    		yield scrapy.Request(url=url, callback=self.parse_car_list)

    def parse_more_comment(self, response):
    	self.count = True
    	url = response.css('div.praise_list.lump a.more::attr(href)').extract_first()
    	yield scrapy.Request(url=url, callback=self.parse_comment, meta={
    			'data':{
    				'request_url': url
    			}
    		})

    def parse_comment(self, response):
        brand = response.css('span.fL.dd::text').extract_first()
    	for i in response.css('dl.g.clearfix'):
    		title = i.css('p.ti a::text').extract_first()
    		time = i.css('p.ms span.fL::text').extract_first()
    		body ={
                i.css('p.yo strong::text').extract_first():i.css('p.yo::text').extract_first(),
                i.css('p.qu strong::text').extract_first():i.css('p.qu::text').extract_first(),
                i.css('p.zs strong::text').extract_first():i.css('p.zs::text').extract_first()
            }

    		tag = i.css('p.bj a::text').extract()
    		response.meta['data'].update({
    				'title': title,
    				'time': time,
    				'body': body,
                    'brand':brand,
    				'tag': tag,
    				'response_url':unicode(response.url)
    			})
    		yield SinaautoItem(response.meta['data'])

    	nextpage = response.css('div.morepage a[alt]::attr(href)').extract()[-2]
    	fake = response.css('div.morepage a[alt]::attr(href)').extract_first()
    	if self.count or nextpage!=fake:
    		self.count = False
    		url = nextpage
    		yield scrapy.Request(url=url, callback=self.parse_comment, meta={
    				'data':{
    					'request_url': url
    				}
    			})





