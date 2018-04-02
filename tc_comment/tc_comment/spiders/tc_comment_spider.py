# -*- coding: utf-8 -*-
from __future__ import absolute_import

import re
import time
import json
import scrapy
from urlparse import urljoin
from tc_comment.items import TcCommentItem
import os




class TcCommentSpiderSpider(scrapy.Spider):
    name = 'tc_comment_spider'
    comment_id = 1
    data_path = './data/tc_comment'
    cache = './cache/tc_comment.cache'
    cache_size = 20
    comparsse_size = 10000

    def start_requests(self):
        urls = []
        root = '/home/lbw/Documents/tc_comment/tc_comment/source/'
        print 'hello'
        for rt, dirs, files in os.walk(root):
            print 'hello'
            for f in files:
                fname = os.path.splitext(f)
                if fname[1] == '.json':
                    with open(root + ''.join(fname)) as json_file:
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

    def get_url(self,response):
        text = response.body
        cmt_id = re.findall(r'cmt_id = (\d*?);', text)[0]
        url_1 = 'http://coral.qq.com/'
        url = url_1 + cmt_id
        print url
        yield scrapy.Request(url=url, callback=self.get_page_source, meta={
            'data':{
                'news_id':response.meta['news_id']
            }
        })


    def get_page_source(self, response):
        print 'gogogo'
        text = response.body
        cmt_id = re.findall(r'cmt_id = (\d*?);',text)[0]
        last = '0'
        url_1 = 'http://coral.qq.com/article/'
        url_2 = '/comment/v2?callback=jQuery112405815446422842271_1511179797655&orinum=10&oriorder=o&pageflag=1&cursor='
        url_3 = '&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=1&_=1511179797656'
        url = url_1 + cmt_id + url_2 + last +url_3
        yield scrapy.Request(url=url, callback=self.get_comments,meta={
            'data':{
                'news_id':response.meta['data']['news_id']
            }
        })

    def get_comments(self,response):
        url_1 = 'http://coral.qq.com/article/'
        url_2 = '/comment/v2?callback=jQuery112405815446422842271_1511179797655&orinum=10&oriorder=o&pageflag=1&cursor='
        url_3 = '&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=1&_=1511179797656'
        content = response.body
        content  =content.strip('\n')
        tmp = re.findall(r'jQuery\d*?_\d*?\((.*?)\}\)',content)[0]+'}'
        data = json.loads(tmp)
        cmt_id = data['data']['targetid']
        last = data['data']['last']
        for i in data['data']['oriCommList']:
            meta={
                'data':{
                    'content': i['content'],
                    'good_number': i['up'],
                    'user_id': i['userid'],
                    'comment_time': time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(i['time']))),
                    'news_id':response.meta['data']['news_id'],
                    'response_url':response.url
                }
            }
            yield TcCommentItem(meta['data'])
        repCommList = data['data']['repCommList']
        if repCommList:
            for i in repCommList:
                meta = {
                    'data': {
                        'content': repCommList[i][0]['content'],
                        'good_number': repCommList[i][0]['up'],
                        'user_id': repCommList[i][0]['userid'],
                        'comment_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(repCommList[i][0]['time']))),
                        'news_id': response.meta['data']['news_id'],
                        'response_url': response.url
                    }
                }
                yield TcCommentItem(meta['data'])


        if last:
            url = url_1 + str(cmt_id) + url_2 + last +url_3
            yield scrapy.Request(url=url, callback=self.get_comments, meta={
                'data': {
                    'news_id': response.meta['data']['news_id']
                }
            })





