# -*- coding: utf-8 -*-
from __future__ import absolute_import

import re
import time
import json
import scrapy
from urlparse import urljoin
from ifeng.items import IfengItem



class IfengSpiderSpider(scrapy.Spider):
    name = 'ifeng_spider'
    start_urls = ['http://search.ifeng.com/sofeng/search.action?q=%E4%B8%AD%E5%8D%B0%E5%AF%B9%E5%B3%99&c=1']
    news_website_id = 5
    cmt_id = 1
    data_path = './data/ifeng'
    cache = './cache/ifeng.cache'
    cache_size = 20
    comparsse_size = 10000



    def parse(self, response):
        for i in response.css('div.searchResults'):
        	url = i.css('p.fz16.line24 a::attr(href)').extract_first()
        	time = i.css('font[color*="#1a7b2e"]::text').extract_first()[9:]
        	year = time[:4]
        	month = time[5:7]
        	day = time[8:10]
        	if (year == '2017'):
        		if (month == '07'):
        			if (day in ['29','30','31']):
        				yield scrapy.Request(url=url, callback=self.parse_news,meta={
        						'data':{
        							'pub_time':time
        						}
        					})
        		if (month == '08'):
        			if (day in [str(j+1) for j in range(16)]):
        				yield scrapy.Request(url=url, callback=self.parse_news,meta={
        						'data':{
        							'pub_time':time
        						}
        					})
        	#else:
        		

    def parse_news(self,response):
    	title = response.css('div#artical h1#artical_topic::text').extract_first()
    	fbody = response.css('div#main_content.js_selection_area p::text').extract()
    	body = '\n'.join(fbody)
    	source_url = response.css('div#artical_sth.clearfix span.ss03 a::attr(href)').extract_first()
    	response.meta['data'].update({
    			'content':body,
    			'source_url':source_url,
    			'title':title,
    			'response_url':response.url
    		})
    	yield IfengItem(response.meta['data'])








    	

    	

