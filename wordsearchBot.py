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

# setting file directories
direc = ".\\textData\\"
driver = webdriver.Firefox()
fileName = "ttt2.csv"

searchWord = "국토해양부"
searchWord = unicode(searchWord, errors='replace')
targetURL = "http://terms.naver.com/search.nhn?query=" + searchWord + "&searchType=&dicType=&subject="
#driver.get("http://terms.naver.com/list.nhn?cid=50867&categoryId=50867")
driver.get(targetURL)
# In case where I first tried, they were "mb_id" and "mb_pw". 
#element_id = driver.find_element_by_id("term_query") 


searchResults = driver.find_elements_by_tag_name("a")

cddList = []
for x in searchResults:
	if re.search(searchWord, x.text, re.UNICODE):
		cdd = ""
		for c in x.text:
			if ord(c) in range(32,127):
				cdd += c
		cdd = str(cdd)
		cdd = re.sub(r'\[\W*',r'',cdd)
		cdd = re.sub(r'\W*\]',r'',cdd)
		print cdd

		cddList.append(cdd)
indexAdjust = 0
for x in range(len(cddList)):
	print re.match(r'[a-zA-Z]',cddList[x])

print cddList
#print driver.current_url
#for x in cddList:
	#x = 

driver.close()


