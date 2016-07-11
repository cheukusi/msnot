#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author    : allqoow
# Contact   : allqoow@gmail.com
# Started on: 20160624(yyyymmdd)
# Project   : msnot
###################################################################


###################################################################
# Stage 0
###################################################################
# 프로그램의 초기설정부분입니다.
# 1. 필요한 모듈을 불러옵니다.
# (Importing required modules)
# 2. encoding설정을 변경합니다.
# (Resetting the chararcter setting for unicode issue)
# 3. 웹에서 들어오는 요청(시스템인자, sys.argv)을 python프로그램에서 받습니다. 
#    (지금은 주석이 달려있고 아래 코드로 대체)
import re, sys
reload(sys)
sys.setdefaultencoding('utf-8')
#userInput = sys.argv[1]
userInput = str('신청마감시간에 임박하면 온라인접속이 폭주합니다.') 
#userInput = str('시험이 어려우면 자살율이 증가한다.')
###################################################################



###################################################################
# Stage 1 : sanitiser
###################################################################
# 사용자가 입력하는 문장을 기계친화적인 형태로 "세척"하는 동작입니다.
# - unicode를 string으로 바꾸기 
# - 앞뒤로 띄어쓰기를 제거하기
# - 문장단위로 나누기
# 등의 작업을 포함한니다.
#
# === IMPORTANT! ===
# rawSenList:
# 		Stage 2에서 문장별로 corpus태깅을 할 때 필요합니다.
from sanitiser import sanitiser
sanitiser = sanitiser(userInput)
rawSenList = sanitiser.rawSenList
###################################################################
print rawSenList



###################################################################
# Stage 2 : corpusTagger
###################################################################
# 자세한 설명은 corpusTagger/__init__.py 참조
#
# === IMPORTANT! ===
# taggedSenList:
#		Stage 3에서 "특별한명사"들의 태깅을 수정할 때 필요합니다.
#		Stage 4에서 목표언어(현재로서는 영어)재구성 계획(scheme)을 만드는 데 필요합니다.
# ejlisedSenList:
#		Stage 5에서 목표언어로 재구성 할 때 필요합니다.
from corpusTagger import corpusTagger
corpusTagger = corpusTagger(rawSenList)
corpusTagger.taggingWithKomoran()
taggedSenList = corpusTagger.taggedSenList
ejlisedSenList = corpusTagger.ejlisedSenList
###################################################################
for x in taggedSenList:
	for y in x:
		print y[0] + ' ' + y[1] + '    ',
print '\n'
for x in ejlisedSenList:
	for y in x:
		print y[0] + ' ' + str(y[1]) + '   ',
print '\n'



###################################################################
# Stage 3 :
###################################################################
# 자세한 설명은 ...subsLibBased/__init__.py, subsWebBased/__init__.py 참조
#
# 고유명사 또는 신경써서 번역할 단어들에 대한 alias붙이기 및 태그 재구성입니다.
# 1. DB/웹검색 친화적인 형태로 corpus들을 재조합합니다.
# 2. 우선 자체DB에서 검색하고 치환합니다.
# 3. 그 다음 웹에서 검색하고 치환합니다.
# 지속적인 개선이 필요한 1번째 부분입니다.
# 웹검색이 필요하므로 selenium의 driver객체를 여기서 호출합니다.
#
# 아직 이거에 대한 확신이 없네요.
from subsLibBased import subsLibBased
subsLibBased()
partialTransListExt = []


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#driver = webdriver.Firefox()
driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
driver = webdriver.PhantomJS()  
#driver.implicitly_wait(10)
from subsWebBased import subsWebBased
subsWebBased(driver)
partialTransListExt = []
###################################################################



###################################################################
# Stage 4 : treeGen
###################################################################
# 자세한 설명은 treeGen/__init__.py 참조
#
# 문장의 "deep structure"를 분석하여 기계친화적인 형태로 저장합니다.
# 지속적인 개선이 필요한 2번째 부분입니다.
#
# treeGen객체는 하나의 문장에 대해서 treeGen인스턴스를 생성합니다. 
# 따라서 문장이 여러개인 경우에는 for문의 루프가 돌아서 각 문장에 대응하는 여러개의 
# treeGen인스턴스의 리스트(treeList)가 만들어집니다.
#
# === IMPORTANT! ===
# (treeList각 원소의) schemeList:
#		Stage 5에서 목표언어로 재구성 할 때 필요합니다.
from treeGen import treeGen
senInfos = zip(rawSenList, taggedSenList)
treeList = []
for x in senInfos:
	aTree = treeGen(x[0], x[1])
	treeList.append(aTree)
###################################################################



###################################################################
# Stage 5 : senBuilder
###################################################################
#
# === IMPORTANT! ===
# outputList:
#		설명이 필요한가...
from senBuilder import senBuilder
outputList = []
for i in range(len(ejlisedSenList)):
	senBuilt = senBuilder(driver, ejlisedSenList[i], treeList[i].schemeList, partialTransListExt)
	outputList.append(senBuilt.finalOutput)
###################################################################



# Wrap-up
driver.close()
for x in outputList:
	print x
print '\n'
print 'Successfully translated!'
#print result