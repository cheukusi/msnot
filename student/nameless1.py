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
direc = "..\\textData\\"
sfnSampleKoToEn = "sampleKoToEn.csv"
sfnDictKoToEn = "dictKoToEn.csv"

# input??
b = '신경망'
b = str(b)
b = b.decode('utf8')
b = re.sub('\n',"",b)
b += '\n'

driver = webdriver.Firefox()
driver.get("http://kiss.kstudy.com/journal/thesis_name.asp?tname=kiss2002&key=20000")

searchList = []
recordCountSample = 0
recordCountDict = 0
# critValue determines how much too crawl
critValue = 10
pagePointer = 0

# since it is much more difficult to find a proper sample
#while recordCountSample < critValue:
"""
inputBox = driver.find_element_by_id("query")
inputBox.send_keys(b)
if pagePointer > 0:
	buttons = driver.find_element_by_class_name('paginate_complex')
	#if pagePointer == 1:
	#	buttons.find_elements_by_tag_name('a')[0].click()
	#else:
	buttons.find_elements_by_tag_name('a')[pagePointer-1].click()

refs = driver.find_elements_by_class_name("title")
for x in refs:
	targetURL = x.find_element_by_tag_name("a").get_attribute("href");
	searchList.append(targetURL)
"""
#for x in searchList:
for i in range(3200000,3210000):
	# move to pages of articles
	x = 'http://kiss.kstudy.com/journal/thesis_name.asp?tname=kiss2002&key=' + str(i)
	driver.get(x)
	print driver.current_url
		
	# processing data from "Keyword"
	# I don't understand why I need this procedure, but without it, it doesn't work.
	targetElements = driver.find_elements_by_class_name("detail")
	targetTexts = []
	for x in targetElements:
		targetTexts.append(x.text)
	artKeywords = targetTexts[2]
	#print len(artKeywords)
	# (until here... all are necessary)

	artKeywords = artKeywords.split("키워드",1)[1].strip()
	artKeywords = str(artKeywords)
	
	inputDict = ''	
	# skip this when artKeywords is empty or mapping is improper	
	if len(artKeywords) > 0 and re.search(r'[ㄱ-ㅣ가-힣]+',artKeywords) != None and re.search(r'[a-z]+',artKeywords) != None:
		kwList = artKeywords.split(', ')
		if len(kwList) % 2 == 0:
			# judge the kind of mapping (from 4 cases) 
			# test whether the phrases are Korean
			resultSet = []
			for x in kwList[0:2]+kwList[-2:]:
				resultSet.append(re.search(r'[ㄱ-ㅣ가-힣]+',x) != None)
			print resultSet
			print kwList
			# case1: Ko, Ko, En, En
			if resultSet == [True, True, False, False]:
				aa = zip(kwList[:len(kwList)/2], kwList[len(kwList)/2:])
				for x in aa:
					inputDict = inputDict + x[0] + '|' + x[1] + '\n'

			# case2: Ko, En, Ko, En
			if resultSet == [True, False, True, False]:
				for i in range(0, len(kwList), 2):
					inputDict = inputDict + kwList[i] + '|' + kwList[i+1] + '\n'

			# case3: En, En, Ko, Ko
			if resultSet == [False, False, True, True]:
				aa = zip(kwList[len(kwList)/2:], kwList[:len(kwList)/2])
				for x in aa:
					inputDict = inputDict + x[0] + '|' + x[1] + '\n'
			# case4: En, Ko, En, Ko
			if resultSet == [False, True, False, True]:
				for i in range(0, len(kwList), 2):
					inputDict = inputDict + kwList[i+1] + '|' + kwList[i] + '\n'

			print inputDict
			recordCountDict += 1

	# processing data from "Abstract"
	# possible to improve this part using regex
	abst = str(targetTexts[3])
	abst = abst.split("<영어 초록>")
	abstKo = abst[0].split("<한국어 초록>")[1].strip()
	abstKoSens = abstKo.split('. ')
	abstEn = abst[1].strip()
	abstEnSens = abstEn.split('. ')

	inputSample = ''
	# skip this when either abstKo or abstEn is (almost) empty
	# and when the mapping is improper
	if len(abstKoSens) == len(abstEnSens) > 0 and len(abstKoSens) > 1 and len(abstEnSens) > 1:
		for i in range(len(abstKoSens)):
			print abstKoSens[i] 
			print abstEnSens[i]
			inputSample = inputSample + abstKoSens[i] + '|' + abstEnSens[i] + '\n'

		inputSample = inputSample + '[문서구분]|[Document Separation]\n'
		recordCountSample += 1

	# this structure is not optimal, but robust to internet disconnection
	with open(direc + sfnDictKoToEn, "a") as saveFileDictKoToEn:
		saveFileDictKoToEn.write(codecs.BOM_UTF8)
		saveFileDictKoToEn.write(inputDict)

	with open(direc + sfnSampleKoToEn, "a") as saveFileSampleKoToEn:
		saveFileSampleKoToEn.write(codecs.BOM_UTF8)
		saveFileSampleKoToEn.write(inputSample)

pagePointer += 1

driver.close()
print "Successfully crawled!"
print "record recordCountSample: " + str(recordCountSample)
print "record recordCountDict: " + str(recordCountDict)