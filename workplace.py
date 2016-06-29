#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author    : allqoow
# Contact   : allqoow@gmail.com
# Started on: 20160624(yyyymmdd)
# Project	: msnot

# importing required modules
import codecs, csv, re, sys

# especially, the module, selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

reload(sys)
sys.setdefaultencoding('utf-8')


"""
b = ''
with open(".\\sample001.txt", "r+") as aa:
	readlined = aa.readline()
	readlined = True
	while readlined:
		readlined = aa.readline()
		b += readlined
"""
b = "사람은 안경을 바꿔야 함."
b = str(b)
b = b.decode('utf8')
b = re.sub("\n","",b)


b = b +" ★"
b += "\n"
print b

driver = webdriver.Firefox()
driver.get("http://203.250.77.84")
inputBox = driver.find_element_by_id("TextBox1")
inputBox.send_keys(b)
outputBox = driver.find_element_by_id("TextBox2").text

#driver.get("https://translate.google.co.kr/")
#driver.close()

cc = outputBox.split("★")
for x in cc[1].split(" "):
	print x
