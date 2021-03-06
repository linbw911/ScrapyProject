# -*- coding: utf-8 -*-

import os
import re
import json
import time
import tarfile
#import mysql.connector
from HTMLParser import HTMLParser
from scrapy.exceptions import DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ZcPipeline(object):
    def process_item(self, item, spider):
    	item['source_id'] = spider.source_id
    	item['language'] = spider.language
    	item['title'] = item['title'].strip()
    	item['body'] = self.parse_body(item['body'])
    	item['cole_time'] = time.time()
        return item
    def parse_body(self, body):
		body = re.sub(r'<!--[\w\W]*?-->|<script([^<>]*)>[\w\W]*?</script>', '', body)
		body = re.sub(r'<\/?(p|div|pre|li|ul|br)( [^<>]*?)?>', '\n', body)
		body = re.sub(r'<[^<>]*?>', '', body)
		body = re.sub(r'\s*\n\s*', '\n', body)
		body = re.sub(r'[^\S\n]+', ' ', body).strip()
		return HTMLParser().unescape(body)

class SavePipeline(object):
	def __init__(self):
		self.is_init = False

	def init(self, data_path, _cache, compresse_size):
		if not os.path.isdir(data_path):
			os.makedirs(data_path)
		cache_dir = os.path.dirname(_cache)
		if not os.path.isdir(cache_dir):
			os.makedirs(cache_dir)

		try:
			with open(_cache) as f:
				cache = json.load(f)
			self.count = cache.get('count', 0)
			self.compresse_count = cache.get('compresse_count', 0)
		except Exception, e:
			self.count = 0
			self.compresse_count = 0

		if self.compresse_count % compresse_size > 0:
			start_num = self.compresse_count - self.compresse_count % compresse_size + 1
			end_num = self.compresse_count
			path = os.path.join(data_path, 'data_compresse_%d_%d.tar.gz' % (start_num, end_num))
			with tarfile.open(path, 'r:gz') as f:
				for filename in f.getnames():
					f.extract(filename, data_path)
			os.remove(path)
			self.compresse_count = start_num - 1

		self.data_path = data_path
		self.cache = _cache
		self.items = []		

	def process_item(self, item, spider):
		if self.is_init == False:
			self.init(spider.data_path, spider.cache, spider.comparsse_size)
			self.is_init = True

		self.count += 1
		item['policy_id'] = self.count
		self.items.append(dict(item))

		if len(self.items) >= spider.cache_size:
			self.save()

		if self.count - self.compresse_count > spider.comparsse_size:
			self.compresse()

		return '[+] %d comments compiled: %s' % (item['policy_id'], 'request_url')

	def close_spider(self, spider):
		if self.is_init:
			self.save()
			self.compresse()

	def save(self):
		if len(self.items) == 0:
			return

		start_num = self.count - len(self.items) + 1
		end_num = self.count
		with open('%s/data%d_%d.json' % (self.data_path, start_num, end_num), 'w+') as f:
			json.dump({
				'count': len(self.items),
				'start': start_num,
				'end': end_num,
				'items': self.items
			}, f, indent=4)
		self.items = []
		self.save_cache()

	def compresse(self):
		if self.count - self.compresse_count == 0:
			return

		cur_path = os.getcwd()
		os.chdir(self.data_path)
		start_num = self.compresse_count + 1
		end_num = self.count
		with tarfile.open('data_compresse_%d_%d.tar.gz' % (start_num, end_num), 'w:gz') as f:
			for filename in os.listdir('./'):
				match = re.match(r'data(\d+)_\d+\.json', filename)
				if match and int(match.group(1)) >= start_num:
					f.add(filename)
					os.remove(filename)
		os.chdir(cur_path)
		self.compresse_count = self.count
		self.save_cache()

	def save_cache(self):
		with open(self.cache, 'w+') as f:
			json.dump({
				'count': self.count,
				'compresse_count': self.compresse_count 
			}, f, indent=4)


