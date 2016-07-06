# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# Author    : allqoow
# Contact   : allqoow@gmail.com
# Started on: 20160624(yyyymmdd)
# Project   : msnot

# importing required modules
import codecs, csv, re, sys

# especially, the module, selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# resetting the chararcter setting for unicode issue
reload(sys)
sys.setdefaultencoding('utf-8')

#userInput = sys.argv[1]

# 1. sanitiser
b = "미래창조과학부는 과학기술정책과 정보통신기술(ICT)에 관한 사무를 관장하는 중앙행정기관이다."
b = '국토교통부는 국토의 체계적인 개발과 보존, 교통물류체계 구축 등의 사무를 관장하는 중앙행정기관이다.'

b = str(b)
b = b.decode('utf8')
b = re.sub("\n","",b)
b = b +" ★"
b += "\n"
print b

# 2. corpus tagger
driver = webdriver.Firefox()
driver.get('http://203.250.77.84')
inputBox = driver.find_element_by_id('TextBox1')
inputBox.send_keys(b)
outputBox = driver.find_element_by_id('TextBox2').text
outputBox = str(outputBox)
cc = outputBox.split('★')

# 3. filtering some nouns/retagging/mapping of nouns
# 3-1. searchBot/Bot selector
# 3-2. compound noun constructor
aliasMapping = []
aliasCommon = 'mnProper'
aliasId = 0
for x in cc[1].split(' '):
	# 검색대상을 선정하는 기준은?(1)
	# NNG가 한 어절에서 세번 나오면 검색대상이 되어야 할까? 연접빈도를 통해서 예측되지 않는 단어라면 검색대상?
	if len(re.findall('NNG', x)) >= 3:
		#print x
		xDecomposed = re.sub(r'__[0-9]+', '', x).split('+')
		searchWord = ''
		xBacks = ''
		for i in range(len(xDecomposed)):
			#이/VCP+다/EF+./SF
			if re.search(r'/J[A-Z]+|이/VCP|다/EF|\./SF', xDecomposed[i]) != None:
				xBacks += xDecomposed[i]
			elif re.search(r'/S[A-Z]+', xDecomposed[i]) != None:
				pass
			else:
				searchWord += xDecomposed[i].split('/')[0]
		
		# strip! strip!
		searchWord = str(searchWord.strip())
		# 어떤 서치봇을 돌릴까?(2)
		from wordsearchBot import atTermsNaver
		#print 'searching the word form Naver...'
		aa = atTermsNaver(searchWord, driver, re)
		aliasMapping.append([aliasCommon + str(aliasId), aa])
		x = aliasCommon + str(aliasId) + '/SL+' + xBacks + str(aliasMapping[aliasId])#NNG?
		aliasId += 1
		
	print x
print aliasMapping

# 4. real translator
# 4-1. decomposing into a tree
# import treeBuilder
# 4-2. rearranging & substituting to English words
# 4-3. reconstructing a sentence from a tree



#print result