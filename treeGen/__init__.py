#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author    : allqoow
# Contact   : allqoow@gmail.com
# Started on: 20160624(yyyymmdd)
# Project	: msnot

class treeGen():
	def __init__(self, rawSen, taggedSen):
		self.case = 0
		self.rawSen = rawSen
		self.taggedSen = taggedSen

		self.treekeyList = [len(taggedSen)]
		self.schemeList = [0, len(taggedSen), 'MatrixClause']
		
		#self.ngramSeq = self.ngramSeqGen(1)
		#self.tagSeq

		self.tagSeqGen()
		self.treekeyListGen()
		self.schemeListGen()

	def tagSeqGen(self):
		self.tagSeq = []
		args = []
		for x in self.taggedSen:
			self.tagSeq.append(str(x[1]))
	
	# n: integer
	def ngramSeqGen(self, n):
		args = []
		for i in range(n):
			args.append(self.tagSeq[i:])
		self.ngramSeq = zip(*args)

	#def determineCase(self, taggedSen):
	def treekeyListGen(self):
		# Case 0
		# No superordinate level component is found prior to the subordinate clauses.
		if self.case == 0:
			verblikes = ['XSV', 'XSA', 'VV', 'VA', 'VX', 'VCP', 'VCN']
			endinglikes = ['EP', 'EF', 'EC', 'ETN', 'ETM']
			indexList = []

			#
			for x in self.taggedSen:
				print x[0]+' ',
			print '\n'
			#
			self.ngramSeqGen(2)
			tt = self.ngramSeq
			for i in range(len(tt)):
				if tt[i][0] in verblikes and tt[i][1] in endinglikes:
					indexList.append(i+2)

			#realIndexList = []
			#'VV', 'EC', 'VV', 'EP'는 두가지 경우가 있다.
			# THIS BLOCK IS DESIGNED SPECIFIC TO NGRAM=2
			#for x in zip(indexList,indexList[1:]+[999]):
			#	if (x[1] - x[0]) != 2:
			#		realIndexList.append(x[0]+1)
			realIndexList = indexList
			self.treekeyList = realIndexList
			# matrix clause는 SF를 포함하도록 했으면 좋겠는데...
			self.treekeyList[-1] = len(self.taggedSen)
			print self.treekeyList


	def schemeListGen(self):
		self.schemeList = []
		
		# just for inspiration, no practical use for now
		#subPointer0 = 0
		#subPointer1 = 0
		#memory0 = 0
		caseSpecificTagSet = ['JX']

		# Case 0
		# No superordinate level component is found prior to the subordinate clauses.
		if self.case == 0:
			adjust = 0
			for i in self.treekeyList:
				localTagSeq = self.tagSeq
				mainPointer = (i-1)-adjust
				print localTagSeq
				print mainPointer

				while True:
					# breakout from the loop if some conditions are satified
					# OR when mainPointer reaches the beginning of the list
					if localTagSeq[mainPointer-1] in caseSpecificTagSet or mainPointer == 0:
						if localTagSeq[i-1-adjust] == 'ETM':
							#self.schemeList.append([mainPointer, i-adjust, 'MM'])
							self.schemeList.append([mainPointer, i, 'MM'])
							localTagSeq[mainPointer:i-adjust] = ['MM']
						elif localTagSeq[i-1-adjust] == 'EC':
							#self.schemeList.append([mainPointer, i-adjust, 'MAG'])
							self.schemeList.append([mainPointer, i, 'MAG'])
							localTagSeq[mainPointer:i-adjust] = ['MAG']
						#elif localTagSeq[i-adjust] == 'EP':
						#	self.schemeList.append([mainPointer, i-adjust, 'MAG'])
						#	localTagSeq[mainPointer:i-adjust+1] = ['MAG']
						elif localTagSeq[i-1-adjust] == 'SF':
							#self.schemeList.append([mainPointer, i-adjust, 'MatrixClause'])
							self.schemeList.append([mainPointer, i, 'MatrixClause'])
						adjust = i-1-mainPointer
						break			
					else:
						mainPointer -= 1
		
		print self.schemeList
		print '\n'
			

	#def locateKeys(self, )
