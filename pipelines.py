# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql



class CropPipeline(object):

	def __init__(self):
		self.conn = pymysql.connect(host='127.0.0.1', port = 3306, user='root', passwd = '123456789.a', db = 'product',charset='utf8mb4') 
		self.cursor = self.conn.cursor()

	def open_spider(self,spider):
		pass

	def process_item(self, item, spider):
		sql = 'insert into crop(`breed`,`id`,`name`) values(%s,%s,%s)'
		self.cursor.execute(sql,(item['breed'],item['num'],item['name'])
			)
		self.conn.commit()
		return item

	def close_spider(self,spider):
		self.cursor.close()
		self.conn.close()