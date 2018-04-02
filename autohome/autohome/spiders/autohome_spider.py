# -*- coding: utf-8 -*-
import scrapy


class AutohomeSpiderSpider(scrapy.Spider):
    name = 'autohome_spider'
    start_urls = ['http://http://www.autohome.com.cn/']

    def start_requests(self):
    	start_urls = [
    		'http://www.autohome.com.cn/grade/carhtml/A.html',
    		'http://www.autohome.com.cn/grade/carhtml/B.html',
    		'http://www.autohome.com.cn/grade/carhtml/C.html',
    		'http://www.autohome.com.cn/grade/carhtml/D.html',
    		'http://www.autohome.com.cn/grade/carhtml/F.html',
    		'http://www.autohome.com.cn/grade/carhtml/G.html',
    		'http://www.autohome.com.cn/grade/carhtml/H.html',
    		'http://www.autohome.com.cn/grade/carhtml/I.html',
    		'http://www.autohome.com.cn/grade/carhtml/J.html',
    		'http://www.autohome.com.cn/grade/carhtml/K.html',
    		'http://www.autohome.com.cn/grade/carhtml/L.html',
    		'http://www.autohome.com.cn/grade/carhtml/M.html',
    		'http://www.autohome.com.cn/grade/carhtml/N.html',
    		'http://www.autohome.com.cn/grade/carhtml/O.html',
    		'http://www.autohome.com.cn/grade/carhtml/P.html',
    		'http://www.autohome.com.cn/grade/carhtml/Q.html',
    		'http://www.autohome.com.cn/grade/carhtml/R.html',
    		'http://www.autohome.com.cn/grade/carhtml/S.html',
    		'http://www.autohome.com.cn/grade/carhtml/T.html',
    		'http://www.autohome.com.cn/grade/carhtml/V.html',
    		'http://www.autohome.com.cn/grade/carhtml/W.html',
    		'http://www.autohome.com.cn/grade/carhtml/X.html',
    		'http://www.autohome.com.cn/grade/carhtml/Y.html',
    		'http://www.autohome.com.cn/grade/carhtml/Z.html'
    	]
    	for url in start_urls:
    		yield scrapy.Request(url=url, callback=self.get_car_list)

    def get_car_list(self, response):
    	for i in response.css('li[id]'):
    		model_front = i.css('h4 a::text').extract_first()
    		url = i.css('a[href*="http://k"]::attr(href)')
    		yield scrapy.Request(url=url, callback=self.get_comment, meta={
    				'data':{
    					'model':[model_front,]
    				}
    			})

    def get_comment(self, response):
    	for i in response.css('div.mouthcon'):
    		model_back = i.css('dl.choose-dl dd a span::text').extract_first()
    		time = i.css('dl.choose-dl dd.font-arial.bg-blue::text').extract()[0].split()[0]
    		price = i.css('dl.choose-dl dd.font-arial.bg-blue::text').extract()[1].split()[0]
    		place = i.css('dl.choose-dl dd.c333::text').extract_first().split()[0]
    		content = response.css('div[id*="divfeeling"]::text').extract()
    		count = 0
    		while count<len(content):
    			body.update({
    					content[count][1:-1]:content[count+1]
    				})
    			count = count+2



    		

        
