'''
Created on 2014-4-22

@author: Sindo
'''
# coding=utf-8

import os
import sys

from ss.util.Toolkit import Toolkit
from ss.util.Navigator import Navigator
from ss.util.HtmlParser import TableParser

class ResumeParser(TableParser):
	def __init__(self, tagId="", tagIdx=0):
		TableParser.__init__(self, tagId, tagIdx)
		
	def handle_starttag(self, tag, attrs):
		TableParser.handle_starttag(self, tag, attrs)
		
		if len(self.tagPath)>=4 and self.tagPath[1]=="tbody" and self.tagPath[2]=="tr" and self.tagPath[3]=="td":
			if self.colIdx==0 and self.curTag=="a":
				self.dataList[self.rowIdx][self.colIdx].append(self.attrDict["href"])
	
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
		self.navigator = Navigator("ai\\" + userName, userPswd)
		
		self.loginName = loginName
		self.loginPswd = loginPswd
		
	def login(self):		
		loginUrl = "http://aijob.asiainfo.com/admin/login"
		self.navigator.call(loginUrl)
		#pageHtml = self.navigator.read()
		#print "loginInfo_pageHtml:%s" % (pageHtml)
		
		veriCode = ""
		resVal = False
		
		print "++++++++ verify_code_step"
		pageUrl = "http://aijob.asiainfo.com/img/check.php"
		
		while resVal == False:
			fotoData = self.navigator.obtain(pageUrl)		
			Toolkit.saveFileContent((self.workDir + "/aijob_veriCode_%d.jpg" % (1001)), fotoData)
			
			print "please_input_verify_code:"
			veriCode = sys.stdin.readline().rstrip()
			
			print "veriCode_is:'%s'" % (veriCode)
			
			postData = {
					"rhr__email": self.loginName,
					"user_name_addr":"asiainfo.com",
					"rhr__password":self.loginPswd,
					"identifying_code":veriCode,
					"redirect":"",
					"x":"62",
					"y":"34",
					"hasflash":"1"
			}
		
			self.navigator.call(loginUrl, None, postData)
			
			pageHtml = self.navigator.read()
			print "pageHtml:%s,%s,%s" % (self.loginName, self.loginPswd, pageHtml)
			resVal = ("/backend.php/hr/myjob/" in pageHtml)
			
		print "login_aijobs_successfully"
		
		return True		
	
	def fetchResume(self) :        
		pageUrl = "http://aijob.asiainfo.com/backend.php/user/talpool/order/1/t/0" 	\
				+ "?tal_type=0&tag_ids=锁定%28无%29%2C已发送Offer%28无%29%2C离职%28无%29&tag_ids_hidden=11-2%2C14-2%2C15-2" \
				+ "&apply_days=&g_diploma_id=70&g_diploma_id_high=1&resume_exp_years=1&job_trade=&job_trade_hidden=&job_type="	\
				+ "&job_type_hidden=&g_area=浙江省&g_area_hidden=86008000&system_user_from_id=不限&keyword=C%2B%2B&code=&name=&order=1"
		
		self.navigator.call(pageUrl, None)
		
		pageHtml = self.navigator.read()
		
		Toolkit.saveFileContent(self.workDir + "/resumeList.htm", pageHtml);
				
		tblParser = TableParser()
		tblParser.feed(pageHtml)
		
		return pageHtml
	
	def perform(self):
		#self.login()
		#self.fetchResume();
		pageHtml = Toolkit.getFileContent(self.workDir + "/resumeList.htm");
		tblParser = TableParser("favoriteList")
		tblParser.feed(pageHtml)
		
		print "dataList result:"
		for cellList in tblParser.dataList:
			for valList in cellList:
				print "{",
				for val in valList:
					if val != valList[0]:
						print ",",
					print val,
				print "}, ",
			print "\n" 
		
		resVal = True
		return resVal
		
if __name__ == '__main__':
	print "Recruit_process_begin......" 
	
	resVal = False
	
	userName = 'lijj'
	userPswd = os.getenv("aintPswd")
	
	loginName = "kangcl"
	loginPswd = os.getenv("kangPswd")
	
	debugMode = False
	workDir = "D:/ZoomZone/AiJobDat"
	
	recruit = Recruit(userName, userPswd, workDir, loginName, loginPswd, debugMode)
	
	resVal= recruit.perform()
	
	if resVal: print "congratulations_your_work_is_successful" 
	else:      print ":( unfortunately_your_work_is_failed ):"