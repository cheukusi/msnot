# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# Author    : allqoow
# Contact   : allqoow@gmail.com
# Started on: 20160624(yyyymmdd)
# Project   : msnot

# importing required modules
import codecs, csv, re, sys

class sanitiser:
	"""
	=== Module for Stage 1 ===
	"""
	def __init__(self, userInput):
		self.rawSenList = []
		self.refineSen(userInput)
	def refineSen(self, userInput):
		"""
		It is recommended to have all sentences separated by periods,
		AND periods are used only for separation of sentences - it is more important!,
		although the reison-d'etre of this module is to deal with cases
		where senetences are not well-separated.
		"""
		userInput = str(userInput)
		userInput = userInput.decode('utf8')
		userInput = userInput.strip()
		# in case the sentences are separated only by period(.)s
		if True:
			sens = userInput.split('.')
			for x in sens[0:len(sens)-1]:
				x += '.'
				x = str(x)
				self.rawSenList.append(x)
		# in case the input cannot be refined
		else:
			print 'Invalid input!'