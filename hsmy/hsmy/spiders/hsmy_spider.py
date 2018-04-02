# -*- coding: utf-8 -*-
from __future__ import absolute_import

import re
import time
import json
import scrapy
from urlparse import urljoin
from hsmy.items import HsmyItem


class HsmySpiderSpider(scrapy.Spider):
    name = 'hsmy_spider'
    start_urls = ['http://www.msri.cn/xyReportView']
    source_id = 1
    report_id = 0
    data_path = './data/hsmy'
    cache = './cache/hsmy.cache'
    cache_size = 20
    comparsse_size = 10000

    def parse(self, response):
        for i in response.css('ul#stiReportList li'):
        	url = i.css('a::attr(href)').extract_first()[29:-4]
        	pub_time = i.css('span::text').extract_first()
        	title = i.css('p::text').extract_first()
        	yield scrapy.Request(url=url, callback=self.parse_data, meta={
        			'data':{
        				'request_url':url,
        				'pub_time':pub_time,
        				'title':title
        			}
        		})
        #nextpage = 
        #if nextpage:

    def parse_data(self, response):
    	text = response.text
    	data_list = re.findall(u'\u62a5\u6536\u4e8e(\d+\.\d+)\u70b9',text)
    	response.meta['data'].update({
    			'STI':data_list[0:3],
    			'Southeast_Asia':data_list[3:6],
    			'South_Asia':data_list[6:9],
    			'Middle_East':data_list[9:12],
    			'Red_Sea':data_list[12:15],
    			'Central_Eastern_Europe':data_list[15:18],
    			'STI_Container':data_list[18:21],
    			'STI_Bulk':data_list[21:24],
    			'STI_Liquid':data_list[24:27],
    			'response_url':unicode(response.url)
    		})
    	yield HsmyItem(response.meta['data'])

