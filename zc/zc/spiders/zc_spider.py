# -*- coding: utf-8 -*-
from __future__ import absolute_import

import re
import time
import json
import scrapy
from urlparse import urljoin
#from bs4 import BeautifulSoup
from zc.items import ZcItem

class ZcSpiderSpider(scrapy.Spider):
    name = 'zc_spider'
    start_urls = ['http://www.bigdataobor.com/index.php/policy/policylist/57/',
    'http://www.bigdataobor.com/index.php/policy/policylist/58/']
    source_id = 2
    data_path = './data/zc'
    language = 'chi'
    cache = './cache/zc.cache'
    cache_size = 20
    comparsse_size = 10000

    def parse(self, response):
        for i in response.css('div.news_rebox_fr.fl ul li'):
        	title = i.css('a::text').extract()[1].strip(' ,\r,\n')
        	url = i.css('a::attr(href)').extract_first()
        	inputtime = i.css('span.inputtime::text').extract_first()
        	if(response.url == self.start_urls[0]):
        		classifications = 'dt'
        	else:
        		classifications = 'jd'

        	yield scrapy.Request(url=url, callback=self.parse_content, meta={
        			'data':{
        				'request_url':url,
        				'inputtime':inputtime,
        				'classifications':classifications,
        				'title':title

        			}
        		})

        nextpage = response.css('a.pg_next::attr(href)').extract_first()
        if nextpage:
        	yield scrapy.Request(url=nextpage, callback=self.parse)

    def parse_content(solf, response):
    	body = response.css('div.rebox_fr_content').extract_first()
    	body = re.sub('<b>[\w\W]*$', '', body)
    	response.meta['data'].update({
    			'body': re.sub('<p class="mt10">[\w\W]*$', '', body),
    			'response_url':unicode(response.url),
    			'out_links': response.css('a::attr(href)').extract(),
    			'html':response.body_as_unicode()
    		})

    	yield ZcItem(response.meta['data'])




    	

