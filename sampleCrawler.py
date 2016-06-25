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

# resetting the chararcter setting for unicode issue
reload(sys)
sys.setdefaultencoding('utf-8')

# setting file directories
direc = ".\\textData\\"
driver = webdriver.Firefox()
fileName = "ttt2.csv"

driver.get("http://www.nrf.re.kr/")

# defining some functions
def write_unicode(text, charset='utf-8'):
    return text.encode(charset)

baseURL = "http://www.nrf.re.kr/nrf_tot_cms/board/biz_notice/view.jsp?show_no=170&check_no=169&c_relation=biz&c_relation2=0&c_no=99&c_now_tab=1&BBS_LLF_CD=biznot&BBS_SLF_CD=99&NTS_NO="

# the Range of indices to crawl
theRange = range(78000,79005)

ret = ""
recordCount = 0
for index in theRange:
	indexedURL = baseURL + str(index)
	driver.get(indexedURL)
	
	title = driver.find_element_by_class_name("td_title").text
	content = driver.find_element_by_class_name("bd_view_txt").text

	#converting the datatype from unicode to string
	title = str(title)
	title = re.sub(r" +"," ",title)
	title = title.replace("\n","[[ENTER]]")

	content = str(content)
	content = re.sub(r" +"," ",content)
	content = content.replace("\n","[[ENTER]]")
	
	#htmlContent = write_unicode(driver.page_source)
	wrContents = driver.find_elements_by_class_name("left")
	dept = wrContents[1].text
	if dept:
		date = wrContents[3].text

		ret += title
		ret += "|"
		ret += dept
		ret += "|"
		ret += date
		ret += "|"
		ret += content
		ret += "\n"

		ret = write_unicode(ret)

		recordCount += 1
		print "done with " + str(index)
	else:
		pass


saveFile = open(direc + fileName, "a")
saveFile.write(codecs.BOM_UTF8)
saveFile.write(ret)
# close the file
saveFile.close()
# close the browser so that your desktop would look nice.
driver.close()
print recordCount

raw_input("Successfully crawled! (Press any key to dismiss")