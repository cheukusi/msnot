#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author    : allqoow
# Contact   : allqoow@gmail.com
# Started on: 20160624(yyyymmdd)
# Project   : msnot

# importing required modules
import codecs, csv, re, sys

# resetting the chararcter setting for unicode issue
reload(sys)
sys.setdefaultencoding('utf-8')

#userInput = sys.argv[1]
userInput = str('신청마감시간에 임박하면 온라인접속이 폭주합니다.')
userInput = str('시험이 어려우면 자살율이 증가한다.')

# Stage 1 
# sanitiser
from sanitiser import sanitiser
sanitiser = sanitiser(userInput)
rawSenList = sanitiser.rawSenList
#print rawSenList

# Library based substitution...
# from substitutionLB import substitutionLB

# Stage 2
# corpusTagger
from corpusTagger import corpusTagger
corpusTagger = corpusTagger(rawSenList)
corpusTagger.taggingWithKomoran()
taggedSenList = corpusTagger.taggedSenList
ejlisedSenList = corpusTagger.ejlisedSenList
#
for x in taggedSenList:
	for y in x:
		print y[0] + ' ' + y[1] + '    ',
print '\n'

for x in ejlisedSenList:
	for y in x:
		print y[0] + ' ' + str(y[1]) + '   ',
print '\n'
#

# Stage 3
# filtering some nouns/retagging/mapping of nouns
# from substitutionWSB import substitutionWSB
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Firefox()
#substitutionWSB(driver)
# 3-1. searchBot/Bot selector
# 3-2. compound noun constructor
# substitution library

# Stage 4
# treeGen
from treeGen import treeGen
senInfos = zip(rawSenList, taggedSenList)
treeList = []
for x in senInfos:
	aTree = treeGen(x[0], x[1])
	treeList.append(aTree)

# Stage 5
# senBuilder
from senBuilder import senBuilder
outputList = []
for i in range(len(ejlisedSenList)):
	senBuilder(driver, ejlisedSenList[i], treeList[i].schemeList)
# 구글번역기로 대체할 부분
# 4-2. rearranging & substituting to English words
# 4-3. reconstructing a sentence from a tree

print '\n'
print 'Successfully translated!'
#print result
