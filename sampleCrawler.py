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

# importing custom modules
# import sanitiser(?)

# resetting the chararcter setting for unicode issue
reload(sys)
sys.setdefaultencoding('utf-8')

# setting file directories
direc = ".\\textData\\"
driver = webdriver.Firefox()
saveFileNameEn = "sampleEn.csv"
saveFileNameKo = "sampleKo.csv"

driver.get("http://www.nrf.re.kr/")

def write_unicode(text, charset='utf-8'):
    return text.encode(charset)

baseURL = "http://www.nrf.re.kr/nrf_tot_cms/board/biz_notice/view.jsp?show_no=170&check_no=169&c_relation=biz&c_relation2=0&c_no=99&c_now_tab=1&BBS_LLF_CD=biznot&BBS_SLF_CD=99&NTS_NO="

# the Range of indices to crawl
si = int(raw_input("Enter Starting index: "))
ei = int(raw_input("Enter Ending index: "))
theRange = range(si,ei)

retKo = ""
retEn = ""
recordCountKo = 0
recordCountEn = 0
for index in theRange:
	indexedURL = baseURL + str(index)
	driver.get(indexedURL)
	wrContents = driver.find_elements_by_class_name("left")
	dept = wrContents[1].text

	if dept:
		date = wrContents[3].text

		# less easier to comprehend, but we have to go through too many articles
		title = driver.find_element_by_class_name("td_title").text
		title = str(title)
		title = re.sub(r" +"," ",title)
		title = title.replace("\n","[[ENTER]]")

		content = driver.find_element_by_class_name("bd_view_txt").text
		content = str(content)
		content = re.sub(r" +"," ",content)
		content = content.replace("\n","[[ENTER]]")

		if re.search(r'([^a-zA-Z0-9]){10}',title) != None:
			retKo += title
			retKo += "|"
			retKo += dept
			retKo += "|"
			retKo += date
			retKo += "|"
			retKo += content
			retKo += "\n"
			retKo = write_unicode(retKo)

			recordCountKo += 1
			print "done with " + str(index) + "[KO]"
		else:				
			retEn += title
			retEn += "|"
			retEn += dept
			retEn += "|"
			retEn += date
			retEn += "|"
			retEn += content
			retEn += "\n"
			retEn = write_unicode(retEn)

			recordCountEn += 1
			print "done with " + str(index) + "[EN]"

# close the browser so that your desktop would look nice.
driver.close()

with open(direc + saveFileNameKo, "w") as saveFileKo:
	saveFileKo.write(codecs.BOM_UTF8)
	saveFileKo.write(retKo)

with open(direc + saveFileNameEn, "w") as saveFileEn:
	saveFileEn.write(codecs.BOM_UTF8)
	saveFileEn.write(retEn)

print "Successfully crawled!"
print "record recordCountKo: " + str(recordCountKo)
print "record recordCountEn: " + str(recordCountEn)
raw_input("Press any key to dismiss")