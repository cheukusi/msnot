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

# user interface
si = int(raw_input("Enter Starting index: "))
ei = int(raw_input("Enter Ending index: "))

# setting file directories
direc = "..\\textData\\"
driver = webdriver.Firefox()
saveFileNameKoToEnNl = "sampleKoToEnNl.csv"
saveFileNameKoToEnSl = "sampleKoToEnSl.csv"

driver.get('http://elaw.klri.re.kr/kor_service/lawView.do')


recordCountNl = 0
recordCountSl = 0
#theRange = range(35763,35764)
theRange = range(si, ei)
for index in theRange:
	retNl = ''
	retSl = ''
	indexedURL = 'http://elaw.klri.re.kr/kor_service/lawViewMultiContent.do?hseq=' + str(index)
	driver.get(indexedURL)

	# mapping of nounlike phrases
	
	weList = driver.find_elements_by_class_name('articletitle')
	for i in range(0, len(weList), 2):
		#splitList = re.split(r'(\(|\))', x.text)
		splitList0 = weList[i].text.split('(')
		splitList1 = weList[i + 1].text.split('(')
		if len(splitList1) > 1 and len(splitList0) == len(splitList1):
			retNl = retNl + splitList1[1].replace(')','') + '|' + splitList0[1].replace(')','') + '\n'
			recordCountNl += 1
			print splitList1[1].replace(')','')
	
	# mapping of sentencelike phrases

	# case1: 'none'
	# initialise
	switch1 = False
	countKo = 0
	countEn = 0
	memory = []
	weList = driver.find_elements_by_class_name('none')
	for i in range(len(weList)):
		aa = weList[i].text
		print aa
		y = str(aa)
		# skipping article (or similar) numbers
		if len(y) < 10:
			pass
		else:
			memory.append(y)
			if re.search(r'[ㄱ-ㅣ가-힣]+', y) != None:
				switch1 = True
				countKo += 1
				if countEn < countKo:
					countKo = 0
					memory.pop()
			else:
				countEn += 1
		if switch1 == True and countKo == countEn:
			for z in zip(memory[:len(memory)/2], memory[len(memory)/2:]):
				retSl = retSl + z[0] + '|' + z[1] + '\n'
			recordCountSl += countKo
			# reinitialise
			switch1 = False
			countKo = 0
			countEn = 0
			memory = []
		print i

	# case2: other classes than 'none'
	targetClassList = ['hang', 'ho', 'mok']
	for targetClass in targetClassList:
		weList = driver.find_elements_by_class_name(targetClass)

		# initialise
		switch0 = False
		switch1 = False
		countKo = 0
		countEn = 0
		memory = []
		for i in range(len(weList)):
			aa = weList[i].find_elements_by_tag_name('td')

			for y in aa:
				y = str(y.text)
				# skipping article (or similar) numbers
				if len(y) < 10:
					pass
				else:
					memory.append(y)
					if re.search(r'[ㄱ-ㅣ가-힣]+', y) != None:
						switch1 = True
						countKo += 1
						if countEn < countKo:
							countKo = 0
							memory.pop()
					else:
						countEn += 1
					#print y
					#print str(countEn) + '  ' + str(countKo)
				if switch1 == True and countKo == countEn:
					for z in zip(memory[:len(memory)/2], memory[len(memory)/2:]):
						retSl = retSl + z[0] + '|' + z[1] + '\n'
					recordCountSl += countKo
					# reinitialise
					switch1 = False
					countKo = 0
					countEn = 0
					memory = []
			print i
	retNl = retNl + '[[document separation]]|[[문서 구분]]\n'
	retSl = retSl + '[[document separation]]|[[문서 구분]]\n'

	with open(direc + saveFileNameKoToEnNl, "a") as saveFileNl:
		saveFileNl.write(codecs.BOM_UTF8)
		saveFileNl.write(retNl)

	with open(direc + saveFileNameKoToEnSl, "a") as saveFileSl:
		saveFileSl.write(codecs.BOM_UTF8)
		saveFileSl.write(retSl)

driver.close()



print "Successfully crawled!"
print "record recordCountNl: " + str(recordCountNl)
print "record recordCountSl: " + str(recordCountSl)
raw_input("Press any key to dismiss")