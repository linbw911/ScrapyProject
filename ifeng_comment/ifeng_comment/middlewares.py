# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from __future__ import absolute_import

import time
from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
from scrapy import signals
from ifeng_comment.settings import USER_AGENT_LIST

import random
from scrapy import log



class IfengCommentSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class RandomUserAgentMiddleware(object):
    """docstring for RandomUserAgentMiddleware"""

    def process_request(self, request, spider):
        ua = random.choice(USER_AGENT_LIST)
        if ua:
            request.headers.setdefault("User-Agent", ua)

# class ActionMiddleware(object):
#     # use selenium
#     def process_request(self, request, spider):
#         if 'https://news.qq.com' in request.url:
#             print "Firefox is starting..."
#             driver = webdriver.Firefox()
#             driver.get(request.url)
#             driver.implicitly_wait(5)
#             #driver.find_element_by_class_name('js_cmtUrl.js_commentNumber').click()
#             url = driver.find_element_by_class_name('js_cmtUrl.js_commentNumber').get_attribute('href')
#             driver.get(url)
#             driver.implicitly_wait(5)
#             print driver.page_source
#             body = driver.page_source
#             driver.close()
#             driver.find_elements_by_class_name()
#             return HtmlResponse(url=url, body=body, encoding='utf-8',request=request)
#         else:
#             return None