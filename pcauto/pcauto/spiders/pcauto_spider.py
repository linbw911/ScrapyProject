# -*- coding: utf-8 -*-
from __future__ import absolute_import

import re
import time
import json
import scrapy
from urlparse import urljoin
from bs4 import BeautifulSoup
from pcauto.items import PcautoItem

class PcautoSpiderSpider(scrapy.Spider):
    start_urls = ['http://price.pcauto.com.cn/price/q-k9999.html']
    name = 'pcauto_spider'
    source_id = 2
    data_path = './data/pcauto'
    cache = './cache/pcauto.cache'
    cache_size = 20
    comparsse_size = 10000
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'
    }

#    def parse(self, response):
#        yield scrapy.Request(url=response.url, callback=self.parse_list, headers=self.headers)


    def parse(self, response):
        for i in response.css('div.tit.blue a[href*="comment"]::attr(href)').extract():
            url = urljoin('http://price.pcauto.com.cn', i)
            yield scrapy.Request(url=url, callback=self.parse_comment, headers=self.headers, meta={
                    'data':{
                        'classification':'car comment',
                        'request_url': url
                    }
                })

        nextpage = response.css('div.pcauto_page a.next::attr(href)').extract_first()
        if nextpage:
            url = urljoin('http://price.pcauto.com.cn', nextpage)
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse_comment(self, response):
        cars = response.css('div.title h1::text').extract_first()
    	for i in response.css('div.litDy.clearfix'):
            dealer = None
            if len(i.css('div.line::text').extract()[2])>2:
                dealer = i.css('div.line::text').extract()[2]
    		model = i.css('div.line a::text').extract_first()
    		time = i.css('div.line::text')[0].extract()
    		price = i.css('div.line i::text')[0].extract()
    		site = i.css('div.line::text')[1].extract()
    		comment_title = i.css('div.dianPing.clearfix b::text').extract()
    		comment_body = i.css('div.dianPing.clearfix span::text').extract()
    		try:
    			comment = {   			
    		    	comment_title[0]:comment_body[0],
    				comment_title[1]:comment_body[1],
    				comment_title[2]:comment_body[2],
    				comment_title[3]:comment_body[3],
    				comment_title[4]:comment_body[4],
    				comment_title[5]:comment_body[5],
    				comment_title[6]:comment_body[6],
    				comment_title[7]:comment_body[7],
    				comment_title[8]:comment_body[8],
    				comment_title[9]:comment_body[9]

            	}
    		except IndexError as e:
    			print e
    		
    		response.meta['data'].update({
                    'cars': cars,
                    'dealer': dealer,
    				'model': model,
    			    'time': time,
    			    'price': price,
    			    'site': site,
    			    'comment': [comment,],
    			    'response_url': unicode(response.url)

    			})
    		yield PcautoItem(response.meta['data'])

    	nextpage = response.css('a.next::attr(href)').extract_first()
    	if nextpage:
    		yield scrapy.Request(url=nextpage, callback=self.parse_comment, headers=self.headers, meta={
                    'data':{
                        'classification':'car comment',
                        'request_url': nextpage
                    }
                })

