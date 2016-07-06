#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author    : allqoow
# Contact   : allqoow@gmail.com
# Started on: 20160624(yyyymmdd)
# Project	: msnot
#
# Step 4-1

# importing required modules
import codecs, csv, re, sys

reload(sys)
sys.setdefaultencoding('utf-8')

#'본'
input1 = str('신청마감시간에 임박해 가면 온라인접속이 폭주합니다.')
input2 = str('이 법에 적용되는 연구과제는 기관생명윤리위원회(IRB)의 심의를 받도록 의무화되었습니다.')
input3 = str('연구사업통합지원시스템을 망가뜨리기 위한 2가지 방법을 설명하려고 합니다.')
input4 = str('나는 어제 친구랑 너가 소개시켜준 식당에서 밥을 먹다가 체했다.')
input5 = str('미래창조과학부는 과학기술정책과 정보통신기술(ICT)에 관한 사무를 관장하는 중앙행정기관을 말한다.')
input6 = str('국토교통부는 국토의 체계적인 개발과 보존, 교통물류체계 구축 등의 사무를 관장하는 중앙행정기관을 말한다.')

# 전처리가 끝났으니까 여기서부터 진짜 번역(3)
from konlpy.tag import Kkma, Komoran
#Kkma = Kkma()
Komoran = Komoran()
taggedList1 = Komoran.pos(input1)
taggedList2 = Komoran.pos(input2)
taggedList3 = Komoran.pos(input3)
taggedList4 = Komoran.pos(input4)
taggedList5 = Komoran.pos(input5)
taggedList6 = Komoran.pos(input6)
aa = [taggedList1, taggedList2, taggedList3, taggedList4, taggedList5, taggedList6]

# 지정사 EF랑 조합될때만 유효하도록?
verblikes = ['XSV', 'XSA', 'VV', 'VA', 'VX']#, 'VCP', 'VCN']
endinglikes = ['EP', 'EF', 'EC', 'ETN', 'ETM']

for taggedList in aa:
	tagSeq = []
	counter = 0
	indexList = []
	for x in taggedList:
		print x[0]+'  ',

	for x in taggedList:
		tagSeq.append(str(x[1]))

	tt = zip(tagSeq, tagSeq[1:])
	for x in range(len(tt)):
		if tt[x][0] in verblikes and tt[x][1] in endinglikes:
			indexList.append(x)
			counter += 1

	realIndexList = []
	for x in zip(indexList,indexList[1:]+[999]):
		if (x[1] - x[0]) != 2:
			realIndexList.append(x[0]+1)
	print realIndexList
	print len(realIndexList)

	mainPointer = realIndexList[0]
	subPointer0 = 0
	subPointer1 = 0
	memory0 = 0
	tree = []
	count = 0
	adjust = 0

	# classifying the cases will be a work.
	caseSpecificTagSet = ['JX']

	for i in realIndexList:
		mainPointer = i - adjust
		print tagSeq
		#print mainPointer
		while True:
			# breakout from the loop if some conditions are satified
			# OR when mainPointer reaches the beginning of the list
			if tagSeq[mainPointer-1] in caseSpecificTagSet or mainPointer == 0:
				if tagSeq[i-adjust] == 'ETM':
					tree.append([mainPointer, i-adjust, 'MM'])
					tagSeq[mainPointer:i-adjust+1] = ['MM']
				elif tagSeq[i-adjust] == 'EC':
					tree.append([mainPointer, i-adjust, 'MAG'])
					tagSeq[mainPointer:i-adjust+1] = ['MAG']
				elif tagSeq[i-adjust] == 'EF':
					tree.append([mainPointer, i-adjust, 'Matrix Clause'])
				adjust = i - mainPointer
				break			
			else:
				mainPointer -= 1
		#print adjust
		print tree
	print '\n'