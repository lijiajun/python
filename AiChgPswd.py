'''
Created on 2014-4-22

@author: Sindo
'''
# coding=utf-8

import os
import re

from Navigator import Navigator

def printSecSepor() :
	print ""
	print "========================================================================"
	print "========================================================================"
	print "========================================================================"
	print ""
		
def saveFileContent(fileName, fileData):
	fileObj = open(fileName, "wb") 
	
	fileObj.write(fileData)
	fileObj.close()
		
class AiChgPswd :
	def __init__(self, userName, userPswd, debug=False):
		self.debug = debug
		
		self.userName = userName
		self.userPswd = userPswd
		self.navigator = Navigator("ai\\" + userName, userPswd)
		
	def doVisitPage(self):  
		pageUrl = "http://chgpass.asiainfo.com/"
		self.navigator.call(pageUrl)
		
		return self.navigator.read()
		
	def doPostChg(self, postData):        
		pageUrl = "http://chgpass.asiainfo.com/"
		
		#<span id="labelMessage" style="color:Red;">
		self.navigator.call(pageUrl, None, postData)
		
		return self.navigator.read()
	
	def getPageInfo(self, pageHtml):
		viewState = ""
		eventValid = ""
		
		#id="__VIEWSTATE" value=""
		#id="__EVENTVALIDATION" value=""
		pattern = re.compile('id="__VIEWSTATE"\svalue="([\S]+)"')
		iterator = pattern.finditer(pageHtml)
		
		if not iterator:
			print "viewState_not_found, html: %s" % (pageHtml)
			return None
		else:
			iIdx = 0;
			for match in iterator:
				viewState = match.group(1)
				iIdx = iIdx + 1
				
		pattern = re.compile('id="__EVENTVALIDATION"\svalue="([\S]+)"')
		iterator = pattern.finditer(pageHtml)
		
		if not iterator:
			print "eventValid_not_found, html: %s" % (pageHtml)
			return None
		else:
			iIdx = 0;
			for match in iterator:
				eventValid = match.group(1)
				iIdx = iIdx + 1
				
		return (viewState, eventValid)
	
	def isPostSuccess(self, pageHtml):
		pattern = re.compile(r'Password changed successfully')
		iterator = pattern.finditer(pageHtml)
		
		if not iterator:
			print "viewState_not_found, html: %s" % (pageHtml)
			return None
		else:
			iIdx = 0;
			for match in iterator:
				return True
				iIdx = iIdx + 1
		
		return None
	
	def perform(self):
		resVal = False
		
		pageHtml = self.doVisitPage();
		pageInfo = self.getPageInfo(pageHtml)		
		postData = {
				"dropdownListDomainName": "AI",
				"textBoxAccountName":self.userName,
				"textBoxOldPassword":self.userPswd,
				"textBoxNewPassword":self.userPswd + "111",
				"textBoxNewPasswordAgain":self.userPswd + "111",
				"buttonChangePassword": "Submit",
				"__VIEWSTATE": pageInfo[0],
				"__EVENTVALIDATION": pageInfo[1]
		}
		printSecSepor()
		pageHtml = self.doPostChg(postData)
		if not self.isPostSuccess(pageHtml):
			print "post_html_No01:%s" % pageHtml
		else:
			print "chg_pswd_succ_No01"
		
		pageHtml = self.doVisitPage();
		pageInfo = self.getPageInfo(pageHtml)
		postData["textBoxOldPassword"] = self.userPswd + "111"
		postData["textBoxNewPassword"] = self.userPswd + "222"
		postData["textBoxNewPasswordAgain"] = self.userPswd + "222"
		postData["__VIEWSTATE"] = pageInfo[0]
		postData["__EVENTVALIDATION"] = pageInfo[1]
		printSecSepor()
		pageHtml = self.doPostChg(postData)
		if not self.isPostSuccess(pageHtml):
			print "post_html_No02:%s" % pageHtml
		else:
			print "chg_pswd_succ_No02"
		
		pageHtml = self.doVisitPage();
		pageInfo = self.getPageInfo(pageHtml)
		postData["textBoxOldPassword"] = self.userPswd + "222"
		postData["textBoxNewPassword"] = self.userPswd + "333"
		postData["textBoxNewPasswordAgain"] = self.userPswd + "333"
		postData["__VIEWSTATE"] = pageInfo[0]
		postData["__EVENTVALIDATION"] = pageInfo[1]
		printSecSepor()
		pageHtml = self.doPostChg(postData)
		if not self.isPostSuccess(pageHtml):
			print "post_html_No03:%s" % pageHtml
		else:
			print "chg_pswd_succ_No03"
		
		pageHtml = self.doVisitPage();
		pageInfo = self.getPageInfo(pageHtml)
		postData["textBoxOldPassword"] = self.userPswd + "333"
		postData["textBoxNewPassword"] = self.userPswd
		postData["textBoxNewPasswordAgain"] = self.userPswd
		postData["__VIEWSTATE"] = pageInfo[0]
		postData["__EVENTVALIDATION"] = pageInfo[1]
		printSecSepor()
		pageHtml = self.doPostChg(postData)
		if not self.isPostSuccess(pageHtml):
			print "post_html_No04:%s" % pageHtml
		else:
			print "chg_pswd_succ_No04"
		
		resVal = True
		
		return resVal
		
if __name__ == '__main__':
	print "begin......"
	
	resVal = False
	debugMode = False
	
	userName = 'lijj'
	userPswd = os.getenv("aintPswd")
	chgPswd = AiChgPswd(userName, userPswd, debugMode)
	
	resVal= chgPswd.perform()
	
	printSecSepor() 
	if resVal: print "congratulations_your_password_is_changed_successfully" 
	else:      print "unfortunately_your_password_is_changed_failed"