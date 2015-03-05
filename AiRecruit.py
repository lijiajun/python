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
		
class Recruit :
	def __init__(self, userName, userPswd, workDir, loginName, loginPswd, debug=False):
		self.debug = debug
		
		self.workDir = workDir
		
		self.auctionId = 0
		self.serverTime = "00:00:00"
		
		self.endHour = 0
		self.endMinute = 0
		self.endSecond= 0
		
		self.userName = userName
		self.navigator = Navigator("ailk\\" + userName, userPswd)
		
		self.loginName = loginName
		self.loginPswd = loginPswd
		
	def login(self):		
		loginUrl = "http://ailkjobs.asiainfo-linkage.com.cn/admin/login"
		self.navigator.call(loginUrl)
		#pageHtml = self.navigator.read()
		#print "loginInfo_pageHtml:%s" % (pageHtml)
		
		veriCode = ""
		resVal = False
		
		print "++++++++ verify_code_step"
		pageUrl = "http://ailkjobs.asiainfo-linkage.com.cn/img/check.php"
		
		while resVal == False:
			fotoData = self.navigator.obtain(pageUrl)		
			saveFileContent((self.workDir + "/ailkjob_veriCode_%d.jpg" % (1001)), fotoData)
			
			print "please_input_verify_code:"
			veriCode = sys.stdin.readline().rstrip()
			
			print "veriCode_is:'%s'" % (veriCode)
			
			postData = {
					"rhr__email": self.loginName,
					"user_name_addr":"asiainfo-linkage.com",
					"rhr__password":self.loginPswd,
					"identifying_code":veriCode,
					"redirect":"",
					"x":"62",
					"y":"34",
					"hasflash":"1"
			}
			
			self.navigator.call(loginUrl, None, postData)
			
			pageHtml = self.navigator.read()
			print "pageHtml:%s" % (pageHtml)
			resVal = ("/backend.php/hr/myjob/" in pageHtml)
			
		print "login_ailkjobs_successfully"
		
		return True		
	
	def doFillInfo(self, postData) :        
		pageUrl = "http://auction.asiainfo-linkage.com/auction/bidstus.asp"
		
		self.navigator.call(pageUrl, None, postData)
		
		return self.navigator.read()
	
	def isAuctionWinned(self, pageHtml):
		pattern = re.compile(r'bidding price must be')
		
		#print pageHtml
		patternRes = pattern.search(pageHtml)
		
		resVal = (patternRes == None)
		
		if not resVal: print "isAuctionWinned_pageHtml: %s" % (pageHtml)
		
		return resVal
	
	def perform(self):
		self.login()
		
		resVal = True
		return resVal
		
if __name__ == '__main__':
	print "Recruit_process_begin......" 
	
	resVal = False
	
	userName = 'lijj'
	userPswd = os.getenv("aintPswd")
	
	loginName = "lijj"
	loginPswd = "xxxxxx"
	
	debugMode = False
	workDir = "E:/TempFile"
	
	recruit = Recruit(userName, userPswd, workDir, loginName, loginPswd, debugMode)
	
	resVal= recruit.perform()
	
	if resVal: print "congratulations_your_work_is_successful" 
	else:      print ":( unfortunately_your_work_is_failed ):"