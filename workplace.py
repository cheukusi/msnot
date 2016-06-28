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


"""
b = ''
with open(".\\sample001.txt", "r+") as aa:
	readlined = aa.readline()
	readlined = True
	while readlined:
		readlined = aa.readline()
		b += readlined

b = str(b)
b = b.decode('utf8')
b = re.sub("\n","",b)
b = b +"★"
b += "\n"
print b

driver = webdriver.Firefox()
driver.get("http://203.250.77.84")

inputBox = driver.find_element_by_id("TextBox1")
inputBox.send_keys(b)
outputBox = driver.find_element_by_id("TextBox2").text
print outputBox

driver.close()

cc = outputBox.split("\n")
for x in cc:
	print x

print cc[50]
"""

aa = "asdg"
if re.search(r"\d+",aa, re.UNICODE):
	print "Match!"
else:
	print "Not match"
	





"""
dd = aa.read()
bb = aa.readline()
#print aa.tell()
aa.seek(3)
cc = aa.readline()
#aa.write("aaaaaaaa")
aa.seek(3)
kk = aa.readlines()
print kk 
aa.close()
print "\n"

pp = open(".\\sample001.txt", "w")
pp.write("I wrote something")
pp.seek(0)

qq = open(".\\sample001.txt", "a")
"""

"""
# setting file directories
direc = ".\\textData\\"

openFileName = "readerFriendly.txt"
saveFileName = "readerFriendly2.txt"

ret = ""
with open(direc + openFileName, "r+") as c: 
	readlined = c.read()
	ret = readlined.replace("====================","====================\n")
	ret = readlined.replace("[[ENTER]]","\n")
with open(direc + saveFileName, "w") as c:
	c.write(ret)
"""
