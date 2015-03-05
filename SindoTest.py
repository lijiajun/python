'''
Created on 2014-3-20

@author: Sindo
'''
# coding=UTF-8

import re
import locale
import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from HTMLParser import HTMLParser
		
class ConfirmResultParser(HTMLParser):
	def __init__(self):
		self.tagId = "divSuccess"
		
		self.curTag = ""
			
		self.enterTag = 0
		self.leaveTag = 0
		
		self.enterTable = 0
		self.leaveTable = 0
		
		self.enterTr = 0
		self.enterTd = 0
		
		self.fieldDict = {
				"sucess": False
		}
		
		HTMLParser.__init__(self)
		
	def getAttrDict(self, attrs) :
		attrDict = {}
		for attr in attrs:
			attrDict[attr[0]] = attr[1]
		return attrDict
		
	def handle_starttag(self, tag, attrs):
		self.curTag = tag
		
		if tag == "div":
			if self.tagId:
				for attr in attrs:
					if attr[0] == "id":
						if attr[1] == self.tagId:          
							self.enterTag = 1
							break
			else:
				self.enterTag = 1
			
		if self.enterTag == 1 and self.leaveTag == 0:
			if tag == "table":
				self.enterTable=1
			if self.enterTable == 1 and self.leaveTable == 0:
				if tag == "tr":
					self.enterTr = self.enterTr + 1
				if self.enterTr == 2:
					if tag == "td":
						self.enterTd = self.enterTd + 1
  
	def handle_endtag(self, tag):
		if self.enterTag == 1:
			if tag == "div":           
				self.leaveTag= 1
			if self.leaveTag < 1 and tag == "table":
				self.leaveTable = 1
			
	def handle_data(self, data):
		if self.enterTd == 2:
			if self.curTag == "td":
				if "预定成功！资源预定成功Email已经发送到您的Email信箱。" in data:
					self.fieldDict["success"] = True

class OrderResultParser(HTMLParser):
	def __init__(self):
		self.mainTag = "span"
		self.tagId = "labelInfo"
		
		self.curTag = ""
		
		self.enterTag = 0
		self.leaveTag = 0
		
		self.fieldDict = {
				"success": True,
				"ordered": False,
				"overtime": False
		}
		
		HTMLParser.__init__(self)
		
	def getAttrDict(self, attrs) :
		attrDict = {}
		for attr in attrs:
			attrDict[attr[0]] = attr[1]
		return attrDict
		
	def handle_starttag(self, tag, attrs):
		self.curTag = tag
		
		if tag == self.mainTag:
			if self.tagId:
				for attr in attrs:
					if attr[0] == "id":
						if attr[1] == self.tagId:          
							self.enterTag = 1
							#print "enterTag"
							break
			else:
				self.enterTag = 1
	
	def handle_endtag(self, tag):
		if self.enterTag == 1 and self.leaveTag == 0:
			if tag == self.mainTag:           
				self.leaveTag= 1
				#print "leaveTag"
			
	def handle_data(self, data):
		if self.enterTag == 1 and self.leaveTag == 0:
			#print self.curTag + ":" + data + "."
			if self.curTag == "img":
				if "该时段已经被其它人预定" in data:
					self.fieldDict["success"] = False
					self.fieldDict["ordered"] = True
				if "预定日期超出限定日期" in data:
					self.fieldDict["success"] = False
					self.fieldDict["overtime"] = True
		
		
def saveFileContent(fileName, fileData):
	fileObj = open(fileName, "wb") 
	
	fileObj.write(fileData)
	fileObj.close()
	
def getFileContent(fileName):
	fileObj = open(fileName, "rt") 
	
	fileContent = ""
	strLine = fileObj.readline()
	
	while strLine:
		fileContent = fileContent + strLine
		strLine = fileObj.readline()
	
	return fileContent

def doTestConfirmResultParser():
	fileName = "E:/Learning/ReserveMeeting/ConfirmResult.html"
	
	pageHtml = getFileContent(fileName)
	
	#print pageHtml
	
	resParser = ConfirmResultParser()
	resParser.feed(pageHtml)
	
	if resParser.fieldDict["success"] == True:
		print "success"
	else:
		print "failed"
	
def doTestOrderResultParser():
	fileName = "E:/Learning/ReserveMeeting/OrderResultDateExceed.html"
	
	pageHtml = getFileContent(fileName)
	
	#print pageHtml
	
	resParser = OrderResultParser()
	resParser.feed(pageHtml)
		
	print "success:%d, orderd:%d, overtime:%d" %    \
			(resParser.fieldDict["success"], resParser.fieldDict["ordered"], resParser.fieldDict["overtime"])
	
	
def doTestDate():    
	testDate = date.today()
	
	weekDay = testDate.weekday()+1
	
	print "date:%d-%d-%d, weekDay:%d" % (testDate.year, testDate.month, testDate.day, weekDay)
	
	testDate = testDate + timedelta(days = 14 )
	weekDay = testDate.weekday()+1
	
	print "date:%d-%d-%d, weekDay:%d" % (testDate.year, testDate.month, testDate.day, weekDay)
	
	#time.sleep(seconds)
	testTime = datetime.now()
	print "time:%d:%d:%d, ms:%d" % (testTime.hour, testTime.minute, testTime.second, testTime.microsecond)
	
	testTime = "12:30"
	testTuple = testTime.rpartition(":")
	
	print "testTime:%d:%d" % (locale.atoi(testTuple[0]), locale.atoi(testTuple[2]))
	
	bgnMinMinus=100
	hourMinus = bgnMinMinus/60
	minuteMinus = bgnMinMinus%60
	print "testMinus:%d:%d" % (hourMinus, minuteMinus)
	
	
def doTestRe():
	fileName = "E:/Learning/BookHtml/AuctionDetail.html"
	pageHtml = getFileContent(fileName)
	
	print "pageHtml:{{{"
	print pageHtml
	print "}}}"
	
		
	currPrice = ""
	currWinner = ""
	currDate = ""
	currTime = ""
	
	#print "getAuctionPrice_html: %s" % (pageHtml)

	#<font face="Verdana, Arial, Helvetica, sans-serif" size="2">
	pattern = re.compile('\<font\sface="Verdana,\sArial,\sHelvetica,\ssans-serif"\ssize="2"\>([\S]+)\</font\>')
	iterator = pattern.finditer(pageHtml)
	
	if not iterator:
		print "price_not_found, getAuctionPrice_html: %s" % (pageHtml)
		return None
	else:
		#print "'%s'" % (match)
		iIdx = 0;
		for match in iterator:
			iIdx = iIdx + 1
			if(iIdx == 2):
				currPrice = match.group(1)[2:]
				
	pattern = re.compile('High bids\</font\>\</td\>[\s]+\<td\swidth="87%"\scolspan="4"\>\<font\ssize="2"\>([\S]+)\</font\>\</td\>')
	iterator = pattern.finditer(pageHtml)
	
	if not iterator:
		print "winner_not_found, getAuctionPrice_html: %s" % (pageHtml)
		return None
	else:
		for match in iterator:
			currWinner = match.group(1)
	
	pattern = re.compile('\<b\>Now:([\S]+)\s([\S]+)\<br\>')
	iterator = pattern.finditer(pageHtml)
	
	if not iterator:
		print "dateTime_not_found, getAuctionPrice_html: %s" % (pageHtml)
		return None
	else:
		for match in iterator:
			currDate = match.group(1)
			currTime = match.group(2)
				
	print (currWinner, currPrice, currDate, currTime)
	
def doTestTime():
	resVal = "12:58:30" < "12:53:01"
	
	print "resVal: %d" % (resVal)
	
	
	timeTuple = "12:53:01".split(":")
	
	serverHour = locale.atoi(timeTuple[0])
	serverMin = locale.atoi(timeTuple[1])
	serverSec = locale.atoi(timeTuple[2])
	
	print "hour:%d, min:%d, sec:%d." % (serverHour, serverMin, serverSec)
	winPrice = 80
	addPrice = 5
	print "testInt:%d" % (winPrice + addPrice),\
	
def doTestSaveFile():
	fileName = "E:/Learning/BookHtml/AuctionDetail.html"
	
	pageHtml = getFileContent(fileName)
	
	saveFileContent("E:/TestSaveFile.py", pageHtml)
def doTestStr():
	
	print "testTime:%s" % "19:01:22".replace(":", "")
	
if __name__ == '__main__':
	#doTestDate()
	#doTestOrderResultParser()
	doTestTime()