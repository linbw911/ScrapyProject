# -*- coding: utf-8 -*-
from __future__ import absolute_import

import re
import time
import json
import scrapy
from urlparse import urljoin
from ifeng_comment.items import IfengCommentItem
import os
from selenium import webdriver
from scrapy.http import HtmlResponse


class IfengCommentSpiderSpider(scrapy.Spider):
    name = 'ifeng_comment_spider'
    comment_id = 1
    data_path = './data/ifeng_comment'
    cache = './cache/ifeng_comment.cache'
    cache_size = 20
    comparsse_size = 10000

    def start_requests(self):
        urls =[]
        root = '/home/lbw/Documents/ifeng_comment/ifeng_comment/source2/'
        print 'hello'
        for rt, dirs, files in os.walk(root):
            print 'hello'
            for f in files:
                fname = os.path.splitext(f)
                if fname[1] == '.json':
                    with open(root+''.join(fname)) as json_file:
                        data = json.load(json_file)
                        for i in data['items']:
                            demand = {i['cmt_id']: i['response_url']}
                            urls.append(demand)

        for dict in urls:
            for key in dict:
                print 'i am going to yield Request!'
                yield scrapy.Request(url=dict[key], callback=self.get_page_source, meta={
                    'data': {
                        'news_id': key
                    }
                })
#         yield scrapy.Request(url='http://news.ifeng.com/a/20170811/51615331_0.shtml',callback=self.get_comments,meta={
#             'data':{
#                 'news_id':1
#             }
#
#         })

    def get_page_source(self,response):
        docUrl = response.url
        url_1 = 'http://comment.ifeng.com/get.php?callback=newCommentListCallBack&orderby=&docUrl='
        url_2 = '&format=js&job=1&p='
        url_3 = '&pageSize=20&callback=newCommentListCallBack&skey=253757'
        for i in range(60):
            url = url_1 + docUrl + url_2 +str(i+1) +url_3
            yield scrapy.Request(url=url, callback=self.get_comments, meta={
                'data':{
                    'news_id':response.meta['data']['news_id']
                }
            })

    def get_comments(self,response):
        body = response.body
        j = re.findall(r'\(function\(\)\{var commentJsonVarStr___=(.*?);\r\n newCommentListCallBack\(commentJsonVarStr___\);\}\)\(\);',body)
        data = json.loads(j[0])
        if data['comments']:
            for i in data['comments']:
                meta = {
                    'data': {
                        'content': i["comment_contents"],
                        'good_number': i['uptimes'],
                        'user_id': i['user_id'],
                        'comment_time': i['comment_date'],
                        'news_id': response.meta['data']['news_id'],
                        'response_url': response.url
                    }
                }
                yield IfengCommentItem(meta['data'])

        else:
            print 'Out of page!'











