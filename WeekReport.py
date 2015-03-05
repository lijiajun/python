'''
Created on 2014-4-22

@author: Sindo
'''

import os,sys,locale
import re
import xlrd
from datetime import date
from datetime import datetime
from datetime import timedelta

from Navigator import Navigator

def printSecSepor(seporName="========") :
	print ""
	print "========================================================================"
	print "=========================== %s ===================================" % (seporName)
	print "========================================================================"
	print ""
		
def saveFileContent(fileName, fileData):
	fileObj = open(fileName, "wb") 
	
	fileObj.write(fileData)
	fileObj.close()
	
class WeekReport :
	def __init__(self, userName, userPswd, workDir, debug=False):
		self.debug = debug
		
		self.userName = userName
		self.userPswd = userPswd
		
		self.workDir = workDir
		self.teamMemberTuple = (u"茅晓萍", u"程雷", u"朱孝明", u"陈宏梅", u"郑杭", u"陈强", u"苏志锦", u"柴增琪", u"汪闻鹏", u"张绪昌")
		
		#self.navigator = Navigator("ailk\\" + userName, userPswd)
	
	def openExcel(self, excelFile):
		try:
			data = xlrd.open_workbook(excelFile)
			return data
		except Exception,e:
			print str(e)
			return None
		
	def parseReqInfo(self, excelSheet, bgnIdx):
		rowNum = excelSheet.nrows    	#####行数

		infoList =[]		
		infoColDict = {
				"ReqId" : 0,
				"Content": 1, 
				"Percent": 2,
				"Workload":3,
				"WorkedDays": 4,
				"WorkingDays": 5,
				"WorkDate":6,
				"UrgentReq":7
		}
		
		for rowId in range(bgnIdx,rowNum):
			row = excelSheet.row_values(rowId)
			
			if not row or not row[0]:
				continue
			elif row[0] == u"系统BUG解决：本周处理的BUG":
				break

			info = {}
			
			colName = "ReqId"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			colName = "Content"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			colName = "Percent"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			colName = "WorkingDays"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			colName = "WorkDate"
			cellIdx = infoColDict[colName]
			try:
				dateTuple = xlrd.xldate_as_tuple(excelSheet.cell(rowId,cellIdx).value,0)
				dateStr = "%4d-%02d-%02d" % (dateTuple[0],dateTuple[1],dateTuple[2])
			except Exception,e:
				print "pasring_date_format_error:%s" % str(e)
				dateStr = row[cellIdx]
			info[colName] = dateStr
			
			colName = "UrgentReq"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			infoList.append(info)
			
		print "reqInfo_end_at_rowId:%d" % (rowId)
		
		return (infoList, rowId)
	
	def parseBugInfo(self, excelSheet, bgnIdx):
		rowNum = excelSheet.nrows    	#####行数
		
		infoList = []
		infoColDict = {
				"BugId": 0,
				"Content": 1, 
				"Percent": 2,
				"Workload":3,
				"WorkedDays": 4,
				"WorkingDays": 5,
				"WorkDate":6,
				"Remark":7
		}
		
		rowId = bgnIdx
		for rowId in range(bgnIdx,rowNum):
			row = excelSheet.row_values(rowId)
			
			if not row or not row[0]:
				continue
			elif row[0] == u"回退：各个现场提出的相关回退":
				break

			info = {}
			
			colName = "BugId"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			colName = "Content"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			colName = "Percent"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			colName = "WorkingDays"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			colName = "WorkDate"
			cellIdx = infoColDict[colName]
			try:
				dateTuple = xlrd.xldate_as_tuple(excelSheet.cell(rowId,cellIdx).value,0)
				dateStr = "%4d-%02d-%02d" % (dateTuple[0],dateTuple[1],dateTuple[2])
			except Exception,e:
				print "pasring_date_format_error:%s" % str(e)
				dateStr = row[cellIdx]
			info[colName] = dateStr
			
			infoList.append(info)
			
		print "bugInfo_end_at_rowId:%d" % (rowId)
		
		return infoList, rowId
	
	def parseHtdInfo(self, excelSheet, bgnIdx):
		rowNum = excelSheet.nrows    	#####行数
		
		infoList = []
		infoColDict = {
				"HtdId": 0,
				"Content": 1, 
				"Percent": 2,
				"Workload":3,
				"WorkedDays": 4,
				"WorkingDays": 5,
				"WorkDate":6,
				"Remark":7
		}
		
		rowId = bgnIdx
		for rowId in range(bgnIdx,rowNum):
			row = excelSheet.row_values(rowId)
			
			if not row or not row[0]:
				continue
			elif row[0] == u"各省现场问题处理：各个现场出现的问题以及解决方法":
				break

			info = {}
			
			colName = "HtdId"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			colName = "Content"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			colName = "Percent"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			infoList.append(info)
			
		print "bugInfo_end_at_rowId:%d" % (rowId)
		
		return infoList, rowId
	
	def parseCopeInfo(self, excelSheet, bgnIdx):
		rowNum = excelSheet.nrows    	#####行数
		
		infoList = []
		infoColDict = {
				"Prov": 0,
				"Problem":1,
				"Content": 2,
				"Workload":5,
				"WorkDate":6,
				"Resolved":7
		}
		
		rowId = bgnIdx
		for rowId in range(bgnIdx,rowNum):
			row = excelSheet.row_values(rowId)
			
			if not row or not row[0]:
				continue
			elif row[0] == u"学习、研究和其他：本周学习或者研究的相关内容":
				break

			info = {}
			
			colName = "Prov"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			colName = "Problem"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			colName = "Content"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			colName = "Workload"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			colName = "WorkDate"
			cellIdx = infoColDict[colName]
			try:
				dateTuple = xlrd.xldate_as_tuple(excelSheet.cell(rowId,cellIdx).value,0)
				dateStr = "%4d-%02d-%02d" % (dateTuple[0],dateTuple[1],dateTuple[2])
			except Exception,e:
				print "copeInfo_pasring_date_format_error:%s" % str(e)
				dateStr = row[cellIdx]
			info[colName] = dateStr
			
			colName = "Resolved"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			infoList.append(info)
			
		print "copeInfo_end_at_rowId:%d" % rowId
		
		return infoList, rowId
	
	def parseStudyInfo(self, excelSheet, bgnIdx):
		rowNum = excelSheet.nrows    	#####行数
		
		infoList = []
		infoColDict = {
				"ProcDesc":1,
				"ResultDesc": 2,
				"Workload":5,
				"WorkDate":6,
				"Remart":7
		}
		
		rowId = bgnIdx
		for rowId in range(bgnIdx,rowNum):
			row = excelSheet.row_values(rowId)
			
			if not row or not row[0]:
				continue
			elif row[0] == u"各省上线支持：各个省份上线支持记录和内容。上线期间，7X24小时支持记录和内容。":
				break
			elif row[0] == u"序号":
				break

			print "rowId:%d, row0:%s" % (rowId, row[0])
			
			info = {}
			
			colName = "ProcDesc"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			colName = "ResultDesc"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			colName = "Workload"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			colName = "WorkDate"
			cellIdx = infoColDict[colName]
			try:
				dateTuple = xlrd.xldate_as_tuple(excelSheet.cell(rowId,cellIdx).value,0)
				dateStr = "%4d-%02d-%02d" % (dateTuple[0],dateTuple[1],dateTuple[2])
			except Exception,e:
				print "pasring_date_format_error:%s" % str(e)
				dateStr = row[cellIdx]
			info[colName] = dateStr
			
			colName = "Remart"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			infoList.append(info)
			
		print "studyInfo_end_at_rowId:%d" % rowId
		
		return infoList, rowId
	
	def parseLiveInfo(self, excelSheet, bgnIdx): 	#上线支持
		rowNum = excelSheet.nrows    	#####行数
		
		infoList = []
		infoColDict = {
				"ProcDesc":1,
				"ResultDesc": 2,
				"Remart":7
		}
		
		rowId = bgnIdx
		for rowId in range(bgnIdx,rowNum):
			row = excelSheet.row_values(rowId)
			
			if not row or not row[0]:
				continue
			elif row[0] == u"下周工作内容：记录下周准备处理的内容":
				break
			elif row[0] == u"序号":
				break

			print "rowId:%d, row0:%s" % (rowId, row[0])
			
			info = {}
			
			colName = "ProcDesc"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			colName = "ResultDesc"
			cellIdx = infoColDict[colName]
			info[colName] = row[cellIdx]
			
			infoList.append(info)
			
		print "liveInfo_end_at_rowId:%d" % rowId
		
		return infoList, rowId
		
	def parseTable(self, excelFile):
		excelData = self.openExcel(excelFile)
		excelSheet = excelData.sheets()[0]
		
		rowNum = excelSheet.nrows    	#行数
		colNum = excelSheet.ncols  		#列数
		
		print "total_rowNum:%d, total_colNum:%d" % (rowNum, colNum)
		
		reqBgnIdx = 3
		reqList, rowId = self.parseReqInfo(excelSheet, reqBgnIdx)
		
		bugBgnIdx = rowId + 2
		bugList, rowId = self.parseBugInfo(excelSheet, bugBgnIdx)
		
		htdBgnIdx = rowId + 2	#htd=回退单
		htdList, rowId = self.parseHtdInfo(excelSheet, htdBgnIdx)
		
		copeBgnIdx = rowId + 2	#cope=各省现场问题处理
		copeList, rowId = self.parseCopeInfo(excelSheet, copeBgnIdx)
		
		studyBgnIdx = rowId + 2	#学习研究等其他内容
		studyList, rowId = self.parseStudyInfo(excelSheet, studyBgnIdx)
		
		liveBgnIdx = rowId + 2	#各省上线支持情况
		liveList, rowId = self.parseLiveInfo(excelSheet, liveBgnIdx)
			
		return (reqList, bugList, htdList, copeList, studyList, liveList)
		
	def perform(self, reportDate):
		resVal = False
		fileData = ""
		lineData = ""
		
		reportDateStr = "%4d-%02d-%02d" % (reportDate/10000, (reportDate%10000/100), (reportDate%10000%100))
		
		for memberName in self.teamMemberTuple:
			excelFile = u"%s/%d/综合账务处理周报_%d(%s).xls" % (self.workDir, reportDate, reportDate, memberName)
			
			if not os.path.isfile(excelFile):
				print "no_excel_file_name: %s" % excelFile
				excelFile = u"%s/%d/综合账务处理周报_%d（%s).xls" % (self.workDir, reportDate, reportDate, memberName)
			
			if not os.path.isfile(excelFile):
				print "no_excel_file_name: %s" % excelFile
				excelFile = u"%s/%d/综合账务处理周报_%d(%s）.xls" % (self.workDir, reportDate, reportDate, memberName)
			
			if not os.path.isfile(excelFile):
				print "no_excel_file_name: %s" % excelFile
				excelFile = u"%s/%d/综合账务处理周报_%d（%s）.xls" % (self.workDir, reportDate, reportDate, memberName)
				
			if not os.path.isfile(excelFile):	
				print "the_member_s_weekReport_not_found: %s" % (memberName)
				#return False
				continue
			
			print "current_excel_file_name: %s" % excelFile
			printSecSepor(">" + memberName + "<")
			
			reqList, bugList, htdList, copeList, studyList, liveList = self.parseTable(excelFile)
			
			printSecSepor("ReqList")
			for reqInfo in reqList:
				lineData = u"\"%s:%s\"\t\"%s\"\t\"%s\"\t\"%s\"\t\"%s\"" % (reqInfo["ReqId"], reqInfo["Content"], "", memberName, reportDateStr, reqInfo["Percent"])
				fileData = u"%s\n%s" % (fileData, lineData)
				print "reqInfo:%s" % lineData
				
			printSecSepor("BugList")
			for bugInfo in bugList:
				lineData = u"\"%s:%s\"\t\"%s\"\t\"%s\"\t\"%s\"\t\"%s\"" % (bugInfo["BugId"], bugInfo["Content"], "", memberName, reportDateStr, bugInfo["Percent"])
				fileData = u"%s\n%s" % (fileData, lineData)
				print "bugInfo: %s" % lineData

			printSecSepor("HtdList")
			for htdInfo in htdList:
				lineData = u"\"%s:%s\"\t\"%s\"\t\"%s\"\t\"%s\"\t\"%s\"" % (htdInfo["HtdId"], htdInfo["Content"], "", memberName, reportDateStr, htdInfo["Percent"])
				fileData = u"%s\n%s" % (fileData, lineData)
				print "htdInfo: %s" % lineData

			printSecSepor("CopeList")
			for copeInfo in copeList:
				lineData = u"\"%s:%s\"\t\"%s\"\t\"%s\"\t\"%s\"\t\"%s\"" % (copeInfo["Problem"], copeInfo["Content"], copeInfo["Prov"], memberName, reportDateStr, "100%")
				fileData = u"%s\n%s" % (fileData, lineData)
				print "copeInfo: %s" % lineData

			printSecSepor("StudyList")
			for studyInfo in studyList:
				lineData = u"\"%s:%s\"\t\"%s\"\t\"%s\"\t\"%s\"\t\"%s\"" % (studyInfo["ProcDesc"], studyInfo["ResultDesc"], "", memberName, reportDateStr, "100%")
				fileData = u"%s\n%s" % (fileData, lineData)
				print "studyInfo: %s" % lineData
				
			printSecSepor("LiveList")
			for liveInfo in liveList:
				lineData = u"\"%s:%s\"\t\"%s\"\t\"%s\"\t\"%s\"\t\"%s\"" % (liveInfo["ProcDesc"], liveInfo["ResultDesc"], "", memberName, reportDateStr, "100%")
				fileData = u"%s\n%s" % (fileData, lineData)
				print "liveInfo: %s" % lineData

		printSecSepor("fileData")
		print fileData
		outputFile = u"%s/%d/综合账务处理周报_%d(Team).xls" % (self.workDir, reportDate, reportDate)
		saveFileContent(outputFile, fileData.lstrip())

		resVal = True
		
		return resVal

def getReportDate():
	wrDateObj = date.today()
	weekDay = wrDateObj.weekday()+1
	
	while not weekDay == 5:	
		wrDateObj = wrDateObj + timedelta(days = -1)
		weekDay = wrDateObj.weekday()+1
		
	#reportDate = "%d%02d%02d" % (wrDateObj.year, wrDateObj.month, wrDateObj.day)
	reportDate = wrDateObj.year * 10000 + wrDateObj.month*100 + wrDateObj.day
	
	return reportDate

if __name__ == '__main__':	# sys.argv[0], sys.argv[1]
	reload(sys)
	sys.setdefaultencoding("utf-8")
	
	print "WeekReport_process_begin...... %d,%s"  % (len(sys.argv), sys.argv[0])
	
	resVal = False
	debugMode = False
	
	userName = 'lijj'
	userPswd = os.getenv("aintPswd")
	
	reportDate = getReportDate()
	if len(sys.argv) >=2:
		"WeekReport_process_arg 1"  + sys.argv[1]
		reportDate = int(sys.argv[1])
		
	workDir = "D:/LiatAilk/WeekRept"
	
	weekReport = WeekReport(userName, userPswd, workDir, debugMode)
	
	resVal= weekReport.perform(reportDate)
	
	printSecSepor()
	
	#python cp , rename Team周报-帐务处理维护团队* Team周报-帐务处理维护团队(2014xx).doc
	
	if resVal: print "congratulations_your_work_is_done_successfully" 
	else:      print "unfortunately_your_work_is_failed"