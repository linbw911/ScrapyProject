# -*- coding: utf-8 -*-
from __future__ import absolute_import

import re
import time
import json
import scrapy
from urlparse import urljoin
from tc.items import TcItem


class TcSpiderSpider(scrapy.Spider):
    name = 'tc_spider'
    start_urls = ['https://www.sogou.com/sogou?site=news.qq.com&query=%E4%B8%AD%E5%8D%B0%E5%AF%B9%E5%B3%99&pid=sogou-wsse-b58ac8403eb9cf17-0004&duppid=1&idx=f&page=1&ie=utf8',
				  'https://www.sogou.com/sogou?site=news.qq.com&query=%B6%B4%C0%CA%CA%C2%BC%FE&pid=sogou-wsse-b58ac8403eb9cf17-0004&sourceid=&idx=f&idx=f']
    news_website_id = 1
    data_path = './data/tc'
    cache = './cache/tc.cache'
    cache_size = 20
    comparsse_size = 10000

    def parse(self, response):
        for i in response.css('div.vrwrap'):
            url = i.css('a[id*="sogou_snapshot"]::attr(href)').extract_first()
            try:
                time = i.css('p.str_info span.gray-color::text').extract_first().strip(' -')
            except AttributeError:
                print 'no data'
                time = ['2012-00-00']
            year = time[0:4]
            month = time[5:7]
            day = time[8:10]
            if (year == '2017'):
                print 'Match Year 2017'
                if (month == '07'):
                    print 'Match Month 07'
                    if (day in ['29', '30', '31']):
                        print 'Match Day'
                        yield scrapy.Request(url=url, callback=self.parse_snapshot)
                elif (month == '08'):
                    print 'Match Month 08'
                    if (day in [str(j + 1) for j in range(16)]):
                        print 'Match Day'
                        yield scrapy.Request(url=url, callback=self.parse_snapshot)

        nextpage = response.css('a#sogou_next.np::attr(href)').extract()
        if (nextpage):
            nextpage = 'https://www.sogou.com/sogou' + nextpage[0]
            yield scrapy.Request(url=nextpage, callback=self.parse)

    def parse_snapshot(self,response):
        url = response.css('div p a[href*="http://news.qq.com"]::attr(href)').extract_first()
        yield scrapy.Request(url=url, callback=self.parse_news, meta={'data':{}})



    def	parse_news(self,response):
        title =  response.css('div.qq_article div.hd h1::text').extract_first()
        source_url = response.css('div.a_Info span.a_source a::attr(href)').extract_first()
        pub_time = response.css('div.a_Info span.a_time::text').extract_first()
        fbody = response.css('div#Cnt-Main-Article-QQ p[style*="TEXT-INDENT: 2em"]::text').extract()
        body = '\n'.join(fbody)
        response.meta['data'].update({
			'pub_time':pub_time,
            'content': body,
            'source_url': source_url,
            'title': title,
            'response_url': response.url
        })
        yield TcItem(response.meta['data'])


        
