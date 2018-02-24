# -*- coding: utf-8 -*-
import scrapy
from crop.items import CropItem
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



class SeedSpider(scrapy.Spider):
    name = 'seed'

    def start_requests(self):
    	url_list = []
    	browser = webdriver.Chrome()
    	try:
    		browser.get("http://www.cgris.net/query/croplist.php#")
    		#time.sleep(2)
    		WebDriverWait(browser,5).until(
    			EC.presence_of_element_located((By.XPATH,'//div[@id="content"]//a'))
    			)
    		tag = browser.find_elements_by_xpath('//div[@id="content"]//a')
    		pattern = re.compile(r"window.open \(\'(.*?)\', ")
    		for element in tag:
    			#获取查询链接
    			cont = element.get_attribute("onclick")
    			href = re.findall(pattern,str(cont))
    			url = "http://www.cgris.net/query/"+href[0]
    			print(url)
    			#获取种子品种
    			breed = element.text
    			meta = {'breed':breed}
    			yield scrapy.Request(url,callback = self.parse , meta =meta)
    	finally:
    		browser.close()	

    def parse(self, response):     	
    	browser = webdriver.Chrome()
    	print(response.url)
    	try:
    		browser.get(response.url)
    		#time.sleep(2)
    		WebDriverWait(browser,5).until(
    			EC.presence_of_element_located((By.XPATH,'//div[@onclick="showR();"]'))
    			)
    		button = browser.find_element_by_xpath('//div[@onclick="showR();"]')
    		button.click()
    		#不断循环查询
    		#页码判断
    		#由于页面未加载完全时，也会有div id ="r1"，所以要选择合适的等待条件
    		time.sleep(1.5)

    		#find_element_locator发挥应该是个locator对象(element)，不能是str
    		#同时如果对返回的element提取内容(text),结果中也会显示后代标签中的内容。但是提取attribute则不会显示

    		#总页码查询
    		page_info = browser.find_element_by_xpath('//div[@id="r1"]')
    		pattern = re.compile(r'共找到(\d*?)个结果')
    		total_page = re.findall(pattern,page_info.text)
    		total_page = int(total_page[0])
    		print(total_page)
    		#设置现页码变量
    		current_page = 1

    		#while ((current_page<total_page) & (i<5)):
    		for i in range(0,5):
    			#提取数据
    			Item = CropItem()
    			print("现页码为:"+str(current_page))
    			Item["breed"] = response.meta["breed"]
    			#由于browser.find_element_by_xpath('//table[@id="undefined"]/tbody[1]/tr[@class="c2"][1]/td[6]')在xpath中可以提取到两个，在尝试后提取式如下
    			Item["name"] = browser.find_elements_by_xpath('//table[@id="undefined"]/tbody[1]/tr[@class="c2"][1]/td[6]')[1].text
    			print(Item["name"])
    			Item["num"] = browser.find_elements_by_xpath('//table[@id="undefined"]/tbody[1]/tr[@class="c2"][1]/td[4]')[1].text
    			print(Item["num"])
    			#点击下一页
    			next_page = browser.find_element_by_xpath('//span[@id="hehe"]/a[3]')
    			next_page.click()
    			time.sleep(2)
    			current_page = int(browser.find_element_by_xpath('//div[@id="r1"]/span[1]/span').text)
    			#i = i + 1
    			yield Item
    	finally:
    		browser.close()