'''
Created on 2014-4-22

@author: Sindo
'''
# coding=utf-8


import os

from HTMLParser import HTMLParser

class TableParser(HTMLParser):
	def __init__(self, tagId="", tagIdx=0):
		self.mainTag = "table"
		
		self.tagId = tagId
		self.tagIdx = tagIdx
		
		self.curTag = ""
		
		self.enterTag = 0
		self.leaveTag = 0
		
		self.tagPath = []
		self.dataList = []
		
		self.rowIdx = -1;
		self.colIdx = -1;
		
		self.attrDict = {}
		
		HTMLParser.__init__(self)
		
	def get_attrDict(self, attrs) :
		attrDict = {}
		for attr in attrs:
			attrDict[attr[0]] = attr[1]
		return attrDict
		
	def handle_starttag(self, tag, attrs):
		if self.enterTag==0 and not self.leaveTag==1 and tag == self.mainTag:
			if self.tagId:
				for attr in attrs:
					if attr[0] == "id" and attr[1] == self.tagId:          
						self.enterTag = 1
						#print "enterTag"
						break
			else:
				if not(self._tagIdx): 	self._tagIdx = 0
				else:					self._tagIdx = self._tagIdx + 1
				
				if self.tagIdx == self._tagIdx:
					self.enterTag = 1
					#print "enterTag"
		
		if not (self.enterTag == 1 and self.leaveTag == 0):
			return
		
		self.curTag = tag
		self.tagPath.append(tag);
		self.attrDict = self.get_attrDict(attrs)
		#print "curTag{{{:%s" % (tag)
		
		if len(self.tagPath)>=4 and self.tagPath[1]=="tbody" and self.tagPath[2]=="tr" and self.tagPath[3]=="td":
			if self.rowIdx == -1:
				self.cellList = [];
				self.rowIdx = len(self.dataList);
				self.dataList.append([])
				
			if self.colIdx == -1:
				self.valList = [];
				self.colIdx = len(self.dataList[self.rowIdx]);
				self.dataList[self.rowIdx].append([])
				self.dataList[self.rowIdx][self.colIdx] = []
			
			if self.colIdx==0 and self.curTag=="a":
				self.dataList[self.rowIdx][self.colIdx].append(self.attrDict["href"])
	
	def handle_endtag(self, tag):
		if not (self.enterTag == 1 and self.leaveTag == 0):
			return
		
		#print "}}}curTag:%s" % (tag)
		
		while len(self.tagPath)>0:
			popTag = self.tagPath.pop()
			
			if popTag == tag:
				break
			else:
				pass
				#print "Tag_is_not_same: {popTag:%s, tag:%s, self.curTag:%s}" % (popTag, tag, self.curTag)
		
		if len(self.tagPath) == 0:
			self.curTag = ""
		else:
			self.curTag = self.tagPath[-1];
			
		if tag=="tr" and len(self.tagPath)==2:
			if self.tagPath[1]=="tbody":
				self.rowIdx = -1;	#row end
				#print self.dataList[self.rowIdx]
		elif tag=="td" and len(self.tagPath)==3:
			if self.tagPath[1]=="tbody" and self.tagPath[2]=="tr":
				self.colIdx = -1;	#col end			
		elif tag == self.mainTag and self.curTag == "":
			self.leaveTag= 1
			#print "leaveTag"
			
	def handle_data(self, data):
		if not(self.enterTag == 1 and self.leaveTag == 0):
			return
		
		if len(self.tagPath)>=4 and self.tagPath[1]=="tbody" and self.tagPath[2]=="tr" and self.tagPath[3]=="td":
			if len(data.strip()) > 0:
				self.dataList[self.rowIdx][self.colIdx].append(data.strip());
		
class FormParser(HTMLParser):
	def __init__(self, formName):
		self.formName = None
		if formName: 
			self.formName = formName
			
		self.enterTag = 0
		self.leaveTag = 0
		
		self.fieldDict = {}
		HTMLParser.__init__(self)
		
	def getAttrDict(self, attrs) :
		attrDict = {}
		for attr in attrs:
			attrDict[attr[0]] = attr[1]
		return attrDict
		
	def handle_starttag(self, tag, attrs):
		if tag == "form":
			if self.formName:
				for attr in attrs:
					if attr[0] == "name":
						if attr[1] == self.formName:          
							self.enterTag = 1
							#print "enter form"
							break
			else:
				self.enterTag = 1
			
		if self.enterTag == 1 and self.leaveTag == 0:
			if tag == "input":
				attrDict = self.getAttrDict(attrs)
				if attrDict.has_key("type") \
						and attrDict["type"] == "hidden" and attrDict["name"]:
					if attrDict.has_key("value"):
						self.fieldDict[attrDict["name"]] = attrDict["value"]
					else:
						self.fieldDict[attrDict["name"]] = ""

	def handle_endtag(self, tag):
		if tag == "form":           
			if self.enterTag == 1:
				self.leaveTag= 1
				#print "leave form"
			
	def handle_data(self, data):
		pass
				
if __name__ == '__main__':
	print "HtmlParser_process_begin......" 
	
	resVal = False
	
	userName = 'lijj'
	userPswd = os.getenv("aintPswd")
	
	
	if resVal: print "congratulations_your_work_is_successful" 
	else:      print ":( unfortunately_your_work_is_failed ):"