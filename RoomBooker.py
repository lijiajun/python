'''
Created on 2014-3-20
@author: Sindo
'''
# coding=utf-8

import os,sys
import time
import locale

from datetime import date
from datetime import datetime
from datetime import timedelta

from HTMLParser import HTMLParser

from ss.util.Navigator import Navigator
from ss.util.HtmlParser import FormParser

from ss.util.Toolkit import Toolkit

class OrderResultParser(HTMLParser):
	def __init__(self):
		self.mainTag = "span"
		self.tagId = "labelInfo"
		
		self.curTag = ""
		
		self.enterTag = 0
		self.leaveTag = 0
		
		self.fieldDict = {
				"success": True,
				"occupied": False,
				"overtime": False
		}
		
		HTMLParser.__init__(self)
		
	def get_attrDict(self, attrs) :
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
					self.fieldDict["occupied"] = True
				if "预定日期超出限定日期" in data:
					self.fieldDict["success"] = False
					self.fieldDict["overtime"] = True
		
class ConfirmResultParser(HTMLParser):
	def __init__(self):
		self.mainTag = "div"
		self.tagId = "divSuccess"
		
		self.curTag = ""
			
		self.enterTag = 0
		self.leaveTag = 0
		
		self.enterTable = 0
		self.leaveTable = 0
		
		self.enterTr = 0
		self.enterTd = 0
		
		self.fieldDict = {
				"success": False
		}
		
		HTMLParser.__init__(self)
		
	def get_attrDict(self, attrs) :
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
			if tag == self.mainTag:           
				self.leaveTag= 1
			if self.leaveTag < 1 and tag == "table":
				self.leaveTable = 1
			
	def handle_data(self, data):
		if self.enterTd == 2:
			if self.curTag == "td":
				if "预定成功！资源预定成功Email已经发送到您的Email信箱。" in data:
					self.fieldDict["success"] = True
	
class RoomBooker :
	def __init__(self, userName, userPswd, debug=False):
		self.debug = debug
		
		self.meetingRoom = ""
		self.bookDate = "2000-01-01"
		self.bgnTime = "00:00"
		self.endTime = "24:00"
				
		#small: 小会议室,  big: 大会议室,  rec: 接待室
		self.meetingDict = {
			"10_small":    "120f3362-d88d-4926-99e7-24cd37cf5697",
			"11_big_1":    "9322803d-9860-4499-af0e-b954dc00a64f",
			"11_big_2":    "a0d3eb4b-6026-450b-b9f0-65adf4ea5a53",
			"12_big_3":    "ef7ca566-34c6-447a-b16a-9d3e16a889fe",
			"12_big_4":    "965322e7-5758-4fbb-908d-a1fb9e5a6a9d",
			"11_rec_2":    "5e2bb8aa-e8f7-4591-905f-912dc6533a6e",
			"11_rec_3":    "c09e7450-6c85-4b58-a858-862335181755",
			"12_rec_4":    "21d4bcd0-2736-42de-ae6c-fbb6c7cca660",
			"10_rec_5":    "779326f4-5bd9-4adb-b8f6-2f9dd74878be",
			"10层小会议室":      "120f3362-d88d-4926-99e7-24cd37cf5697",
			"11层大会议室一":    "9322803d-9860-4499-af0e-b954dc00a64f",
			"11层大会议室二":    "a0d3eb4b-6026-450b-b9f0-65adf4ea5a53",
			"12层大会议室三":    "ef7ca566-34c6-447a-b16a-9d3e16a889fe",
			"12层大会议室四":    "965322e7-5758-4fbb-908d-a1fb9e5a6a9d",
			"11层第二接待室":    "5e2bb8aa-e8f7-4591-905f-912dc6533a6e",
			"11层第三接待室":    "c09e7450-6c85-4b58-a858-862335181755",
			"12层第四接待室":    "21d4bcd0-2736-42de-ae6c-fbb6c7cca660",
			"10层第五接待室":    "779326f4-5bd9-4adb-b8f6-2f9dd74878be"
		}
		
		self.occupied = False
		self.overtime = False
		
		self.navigator = Navigator(userName, userPswd)           
		
	def queryInfo(self, qryPara):        
		pageUrl = "http://home.asiainfo.com/AIAIR/Reservation/FillInReservationInfo.aspx"
		
		self.navigator.call(pageUrl, qryPara)
		
		return self.navigator.read()
	
	def doFillInfo(self, postData) :        
		pageUrl = "http://home.asiainfo.com/AIAIR/Reservation/FillInReservationInfo.aspx"
		
		self.navigator.call(pageUrl, None, postData)
		
		return self.navigator.read()
	
	def doConfirm(self, postData) :
		pageUrl = "http://home.asiainfo.com/AIAIR/Reservation/ConfirmReserve.aspx"
		self.navigator.call(pageUrl, None, postData)
		
		return self.navigator.read()
	
	def perform(self, meetingRoom, bookDate, bgnTime, endTime, overTimeWait=False):
		self.meetingRoom = meetingRoom
		self.bookDate = bookDate
		self.bgnTime = bgnTime
		self.endTime = endTime
		
		#step_no_1: query_reserve_info
		qryPara = {
			"ID": self.meetingDict[meetingRoom],
			"BT": bookDate + " " + bgnTime + ":00",
			"ET": bookDate + " " + endTime + ":00",
		}
		 
		pageHtml = self.queryInfo(qryPara)
		if self.debug: 
			print "queryHtml:" + pageHtml
			Toolkit.printSecSepor()
		 
		formParser = FormParser("Form1")
		formParser.feed(pageHtml)
		fieldDict = formParser.fieldDict
		if not fieldDict.has_key("__VIEWSTATE"):
			fieldDict["__VIEWSTATE"]=""
		
		#step_no_2: fill_book_info
		postData = {
			"__EVENTTARGET":"linkButtonNext2:LinkButtonAction",
			"__EVENTARGUMENT":"",
			"__VIEWSTATE": fieldDict["__VIEWSTATE"],
			"datePickerBegin:textBoxDate": bookDate,
			"datePickerEnd:textBoxDate": bookDate,
			"dropDownListTimeBegin": bgnTime + ":00",
			"dropDownListTimeEnd":  endTime + ":00",
			"textBoxDescription": "biz_billing_cmc_aps_team_meeting"
		}
		
		while True:
			pageHtml = self.doFillInfo(postData)
			
			if self.debug: 
				print "doOrderHtml:" + pageHtml
				Toolkit.printSecSepor()
			
			bookResParser = OrderResultParser()
			bookResParser.feed(pageHtml)
			
			if bookResParser.fieldDict["success"]:
				self.occupied = False
				self.overtime = False
				break;
			else:
				self.occupied = bookResParser.fieldDict["occupied"]
				self.overtime = bookResParser.fieldDict["overtime"]
				
				if self.occupied: return False
				if self.overtime and not overTimeWait: return False
				
			time.sleep(1)
		
		formParser = FormParser("Form1")
		formParser.feed(pageHtml)
		fieldDict = formParser.fieldDict
		if not fieldDict.has_key("__VIEWSTATE"):
			fieldDict["__VIEWSTATE"]=""
		
		#step_no_3: confirm_book_info
		postData = {
			"__EVENTTARGET":"linkButtonNext2:LinkButtonAction",
			"__EVENTARGUMENT":"",
			"__VIEWSTATE": fieldDict["__VIEWSTATE"],
			"Navigation1:HiddenHelpType":"false"
		}
		pageHtml = self.doConfirm(postData)
		
		if self.debug: 
			print "doConfirm:" + pageHtml
			Toolkit.printSecSepor()
		
		confirmResParser = ConfirmResultParser()
		confirmResParser.feed(pageHtml)
		
		if self.debug: 
			print "################################# DONE #################################"
		
		return confirmResParser.fieldDict["success"]
	
	def doBookPartly(self, meetingRoom, bookDate, bgnTime, endTime):         #碎片化预定每半小时一次        
		print "doBookPartly:{bgnTime:%s, endTime:%s} {{{" % (bgnTime, endTime)
			
		bookRes = True
		
		sleepTime = 0
		
		while True:
			nowTime = datetime.now()
			nowHour = nowTime.hour
			nowMinute = nowTime.minute
			nowSecond = nowTime.second
			
			bgnTimeTuple = bgnTime.rpartition(":")
			bgnHour = locale.atoi(bgnTimeTuple[0])
			bgnMinute = locale.atoi(bgnTimeTuple[2])
			
			endTimeTuple = endTime.rpartition(":")
			endHour = locale.atoi(endTimeTuple[0])
			endMinute = locale.atoi(endTimeTuple[2])
			
			bgnSecMinus = (nowHour-bgnHour)*60*60 + (nowMinute-bgnMinute)*60 + nowSecond
			endSecMinus = (nowHour-endHour)*60*60 + (nowMinute-endMinute)*60 + nowSecond
			bookSecMinus = (endHour-bgnHour)*60*60 + (endMinute-bgnMinute)*60
			
			print "minute_vars:{bgnSecMinus:%d, endSecMinus:%d, bookSecMinus:%d}"   \
					% (bgnSecMinus, endSecMinus, bookSecMinus)\
						
			if bgnSecMinus < (30*60):   #开始时间未到
				sleepTime = 30*60 - bgnSecMinus
				print "bgnTime_sleeping_seconds:%d" % (sleepTime)
				time.sleep(sleepTime)
				continue
			elif endSecMinus < 0:   	#结束时间未到		
				if bgnSecMinus>=(30*60):
					hourMinus = bgnSecMinus/60/60
					minuteMinus = bgnSecMinus/60-hourMinus*60
					
					newBgnHour = bgnHour+hourMinus
					newBgnMinute = bgnMinute+minuteMinus
					if newBgnMinute >=60:
						newBgnHour = newBgnHour+1
						newBgnMinute = newBgnMinute-60
					
					modNewMinute = (newBgnMinute%30)
					newBgnMinute = newBgnMinute - modNewMinute
						
					midTime = "%02d:%02d" % (newBgnHour, newBgnMinute)
					
					print "clastic_midTime:%s" % (midTime)
					
					bookRes = self.doBookPartly(meetingRoom, bookDate, bgnTime, midTime)
					
					if bookRes == True:
						print "midTime_sleeping_minutes:%d" % (29-modNewMinute)
						time.sleep((29-modNewMinute)*60)
						bgnTime = midTime   #更新bgnTime
						continue
					else:
						print "recursive_doClasticOrder_failed"
						break
				else:
					print "else_sleeping_minutes:%d" % (1)
					time.sleep(1)
					continue
			else:
				pass
				
			print "booking:{room:%s, date:%s, time:{%s-%s}" % (meetingRoom, bookDate, bgnTime, endTime)
				
			bookRes = self.perform(meetingRoom, bookDate, bgnTime, endTime, True)
			
			if bookRes == True:
				print "meetingRoom_bookSuccess"
				break
			elif self.overtime == True:
				print "overtime_sleeping_minutes:%d" % (1)
				time.sleep(1)
				continue
			elif self.occupied == True: 
				print "meetingRoom_is_occupied"
				break
			else:
				print "doClasticOrder_unknown_error" 
				break

		print "doBookPartly:{bgnTime:%s, endTime:%s} }}}" % (bgnTime, endTime)
		
		return bookRes
	
def doBookInTurn(booker):         #自动按顺序预定会议室
	bookRes = False
	
	bookInfo = ("2014-04-30", "14:00", "16:00")
	listMeetingRoom  = ("11_big_2", "12_big_4", "12_big_3", "10_small", "10_rec_5")
	
	for meetingRoom in listMeetingRoom:
		bookRes = booker.perform(meetingRoom, bookInfo[0], bookInfo[1], bookInfo[1])
		if bookRes["success"] == True: break
		if bookRes["occupied"] != True: break
			
	return bookRes
	
def doBookDaemon(booker):         #守护进程预定入口
	# 只能按半小时预定会议室
	meetingRoom = "11_big_1"

	entireBgnTime = "09:00"
	entireEndTime = "21:00"
	
	todayDateObj = date.today()
	weekDay = todayDateObj.weekday()+1
	
	if weekDay == 1:        #星期一
		entireBgnTime = "09:00"
		entireEndTime = "21:00"
	elif weekDay == 2:      #星期二
		entireBgnTime = "09:00"
		entireEndTime = "21:00"
	elif weekDay == 3:      #星期三
		entireBgnTime = "09:00"
		entireEndTime = "21:00"    
	elif weekDay == 4:      #星期四
		entireBgnTime = "09:00"
		entireEndTime = "21:00"
	elif weekDay == 5:      #星期五
		entireBgnTime = "09:00"
		entireEndTime = "21:00"
	else:
		print "there_is_no_need_to_reserve"
		return False
	
	bookDateObj = todayDateObj + timedelta(days = 14 )
	
	# value_format: "2014-4-29"
	bookDate = "%d-%02d-%02d" % (bookDateObj.year, bookDateObj.month, bookDateObj.day)
	print "daemon_bookDate:%s" %(bookDate)
	
	loopBgnTime = entireBgnTime
	
	resVal = True
	
	while True:
		resVal = booker.doBookPartly(meetingRoom, bookDate, loopBgnTime, entireEndTime)
		if not resVal and not booker.occupied:
			#未知原因导致的预订失败，再重订一次
			resVal = booker.doBookPartly(meetingRoom, bookDate, loopBgnTime, entireEndTime)
	
		mailRes = doSendMail(userName, userPswd, booker, resVal, entireBgnTime, entireEndTime)
		if mailRes: 	print "send_mail_success" 
		else:      	print "send_mail_failed"
		
		loopBgnTime = booker.endTime
		
		if resVal:
			break
		elif loopBgnTime >= entireEndTime:
			break;
	
	return resVal

def doSendMail(userName, userPswd, booker, resVal, entireBgnTime, entireEndTime):
	mailCfgDict = {
			"host": "mail.asiainfo.com",
			"user": userName, "pswd": userPswd
	}
	mailFrom = userName + "@asiainfo.com"
	mailToList = [userName +"@asiainfo.com"]
	mailSubject = "会议室预定成功通知"
	
	if not resVal:
		mailSubject = "会议室预定失败通知"
	
	mailContent = "管理员, 你好:" +  "<br/><br/>"
	mailContent = mailContent + "　　会_议_室: " + booker.meetingRoom + "<br/>"
	mailContent = mailContent + "　　预定日期: " + booker.bookDate + "<br/>"
	
	if not resVal:
		mailContent = mailContent + "　　失败时间: " + booker.bgnTime + " - " + booker.endTime + "<br/>"
		
	mailContent = mailContent + "　　整体时间: " + entireBgnTime + " - " + entireEndTime + "<br/>"
	
	if not resVal:
		if booker.occupied == True:
			mailContent = mailContent + "　　失败原因: 会议室已被别人抢到" + "<br/>"
		else:
			mailContent = mailContent + "　　失败原因: 未知原因,请参考日志" + "<br/>"
		
	todayDateObj = date.today()
	todayDate = "%4d年%02d月%02d日" % (todayDateObj.year, todayDateObj.month, todayDateObj.day)
	mailContent = mailContent + "<br/><br/><br/><br/><br/>"                             \
			+ "　　　　　　　　　　　　　　　　　　　　　　　　　　　　会议室预定机<br/><br/>"  \
			+ "　　　　　　　　　　　　　　　　　　　　　　　　　　　　" + todayDate + "<br/>"
	
	resVal = Toolkit.sendMail(mailCfgDict, mailFrom, mailToList, mailSubject, mailContent)
	
	return resVal

if __name__ == '__main__':
	print "会议室预定机开始预订会议室......"
	resVal = False
	debugMode = False
	
	Toolkit.printSecSepor()
	
	userName = 'lijj'
	userPswd = os.getenv("aintPswd")
	
	if len(sys.argv)>1:
		userName = sys.argv[1]
	if len(sys.argv)>2:
		userPswd = sys.argv[2]
	
	if userPswd =="console":
		print "please_input_password: ",
		userPswd = sys.stdin.readline().rstrip()
	elif userPswd[0:8] == "AsiaINFO-":
		encryptPswd=userPswd[8:]
		userPswd = Toolkit.decrypt(32, encryptPswd)
	
	booker = RoomBooker("ai\\" + userName, userPswd, debugMode)
	#resVal = doBookInTurn(booker)
	resVal = doBookDaemon(booker)

	if resVal: print "book_meeting_room_success"
	else:      print "book_meeting_room_failed."  