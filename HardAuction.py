'''
Created on 2014-4-22

@author: Sindo
'''
# coding=utf-8

import os
import re
import sys
import time
import locale
from Navigator import Navigator

def printSecSepor(self) :
	print ""
	print "========================================================================"
	print "========================================================================"
	print "========================================================================"
	print ""
		
def saveFileContent(fileName, fileData):
	fileObj = open(fileName, "wb") 
	
	fileObj.write(fileData)
	fileObj.close()
		
class HardAuction :
	def __init__(self, userName, userPswd, workDir, debug=False):
		self.debug = debug
		
		self.workDir = workDir
		
		self.auctionId = 0
		self.serverTime = "00:00:00"
		
		self.endHour = 0
		self.endMinute = 0
		self.endSecond= 0
		
		self.userName = userName
		self.navigator = Navigator("ai\\" + userName, userPswd)           
		
	def fetchVeriCode(self):        
		pageUrl = "http://auction.asiainfo.com/auction/getcode.asp"
		
		fotoData = self.navigator.obtain(pageUrl)
		
		saveFileContent((self.workDir + "/no%d_veriCode.jpg" % (self.auctionId)), fotoData)
		
		return True		
	
	def doFillInfo(self, postData) :        
		pageUrl = "http://auction.asiainfo.com/auction/bidstus.asp"
		
		self.navigator.call(pageUrl, None, postData)
		
		return self.navigator.read()
	
	def isVeriCodeRight(self, veriCode):
		"Please enter the correct Valify Code"
		"bidding price must be&nbsp;at least 10.00 more than current Price"
		pattern = re.compile(r'bidding price must be')
		
		postData = {
				"id":self.auctionId,
				"bid1":"1",
				"vcode": veriCode
		}
		
		pageHtml = self.doFillInfo(postData)
		
		#print pageHtml
		patternRes = pattern.search(pageHtml)
		
		resVal = (patternRes != None)
		
		if not resVal: print pageHtml
		
		return resVal
	
	def doVisitItemDtl(self):
		pageUrl = "http://auction.asiainfo.com/auction/itemdtl.asp"
		qryData = {
				"ID":self.auctionId
		}
		self.navigator.call(pageUrl, qryData)
		pageHtml = self.navigator.read()
		
		fileName = "no%s_item_dtl_%s.html" % (self.auctionId, self.serverTime.replace(":", ""))
		saveFileContent(self.workDir + "/html/" + fileName, pageHtml)
		
		return pageHtml
		
	def getAuctionInfo(self, pageHtml):
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
				
		return (currWinner, currPrice, currDate, currTime)
	
	def isAuctionWinned(self, pageHtml):
		pattern = re.compile(r'bidding price must be')
		
		#print pageHtml
		patternRes = pattern.search(pageHtml)
		
		resVal = (patternRes == None)
		
		if not resVal: print "isAuctionWinned_pageHtml: %s" % (pageHtml)
		
		return resVal
	
	def perform(self, auctionId, endTime, maxPrice, addPrice, preSec):
		self.auctionId = auctionId
		timeTuple = endTime.split(":")
		self.endHour = locale.atoi(timeTuple[0])
		self.endMinute = locale.atoi(timeTuple[1])
		self.endSecond = locale.atoi(timeTuple[2])
		
		print "auction_info:{auctionId:%d, endTime: %02d:%02d:%02d}" % (auctionId, self.endHour,self.endMinute,self.endSecond)
		
		veriCode = ""
		resVal = False
		
		print "++++++++ verify_code_step"
		while resVal == False:
			self.fetchVeriCode()
			
			print "please_input_verify_code:"
			veriCode = sys.stdin.readline().rstrip()
			
			print "veriCode_is:'%s'" % (veriCode)
			
			resVal = self.isVeriCodeRight(veriCode);
			
			print "resVal:%d" % (resVal)
			
		print "the_correct_veriCode:%s" % (veriCode)
		
		loopTimes = 0
		winPrice = 0
		winnerName = ""
		
		while True:			
			print "++++++++ parsing_price_step: No%2d, %s" % (loopTimes, self.serverTime)
			pageHtml = self.doVisitItemDtl();
			auctionInfo = self.getAuctionInfo(pageHtml)
			
			if not auctionInfo:
				print "current_auctionInfo_not_found"
				return False
			
			winnerName, strPrice, serverDate, self.serverTime = auctionInfo
			
			winPrice = locale.atoi(strPrice.split(".")[0])
			
			timeTuple = self.serverTime.split(":")
			serverHour = locale.atoi(timeTuple[0])
			serverMin = locale.atoi(timeTuple[1])
			serverSec = locale.atoi(timeTuple[2])
			
			secondMinus =  (self.endHour-serverHour)*60*60 	\
					+ (self.endMinute-serverMin)*60 + (self.endSecond - serverSec)
			
			print "current_auctionInfo1: {No%02d, minus:%d, '%d', '%s', '%s', '%s'}."  %	\
					(loopTimes, secondMinus, winPrice, winnerName, serverDate, self.serverTime)
					
			if secondMinus - 30 > (3*60):
				print "sleeping %d second ......" % (3*60)
				time.sleep(3*60)
			else:
				print "sleeping %d second ......" % (secondMinus-preSec)
				time.sleep(secondMinus-preSec)
				break
					
			loopTimes = loopTimes+1
		
		print "++++++++ fill_bid_info_step"
		
		loopTimes = 0
		resVal = False
		
		while True:
			print "###################### try_no:%d ######################" % (loopTimes+1)
			
			if winnerName != self.userName:
				bidPrice = winPrice + addPrice
				if bidPrice > maxPrice:
					print "maxPrice_is_reached"
					bidPrice = maxPrice
				postData = {
						"id":self.auctionId,
						"bid1": "%d" % (bidPrice),
						"vcode": veriCode
				}
				
				print "winner_price:%d, begin_bid_price:%d" % (winPrice, bidPrice)
				pageHtml = self.doFillInfo(postData)
				
				fileName = "no%s_bid_res_%s_%02d.html" % (self.auctionId, self.serverTime.replace(":", ""), loopTimes)
				saveFileContent(self.workDir + "/html/" + fileName, pageHtml)
			
			pageHtml = self.doVisitItemDtl();
			auctionInfo = self.getAuctionInfo(pageHtml)
			winnerName, strPrice, serverDate, self.serverTime = auctionInfo		
			
			winPrice = locale.atoi(strPrice.split(".")[0])
			
			timeTuple = self.serverTime.split(":")
			serverHour = locale.atoi(timeTuple[0])
			serverMin = locale.atoi(timeTuple[1])
			serverSec = locale.atoi(timeTuple[2])
			
			if serverHour == self.endHour and serverMin>self.endMinute:
				print "endTime_is_reached_1:%s" % self.serverTime
				break
			elif serverHour == self.endHour 	\
					and serverMin == self.endMinute and serverSec>= self.endSecond:
				print "endTime_is_reached_2:%s" % self.serverTime
				break
			else:
				print "current_auctionInfo1: {No%02d, winner:%s, winPrice:%d, serverTime:'%02d:%02d:%02d'}."  %	\
					(loopTimes, winnerName, winPrice, serverHour, serverMin, serverSec)

			
			loopTimes = loopTimes+1
		
		return (winnerName == self.userName)
		
if __name__ == '__main__':
	print "begin......"
	
	resVal = False
	
	userName = 'lijj'
	userPswd = os.getenv("aintPswd")
	
	debugMode = False
	workDir = "E:/Learning/Auction"
	
	auctionId = 61			#auction_id
	maxPrice = 100			#max_price
	addPrice = 10			#add_price
	preSecond = 10 			#seconds_reserve
	endTime = "13:00:00"	#terminate_time
	
	hardAuction = HardAuction(userName, userPswd, workDir, debugMode)
	
	resVal= hardAuction.perform(auctionId, endTime, maxPrice, addPrice, preSecond)
	
	if resVal: print "auction_success" 
	else:      print "auction_failed"