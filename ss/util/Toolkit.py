'''
Created on 2014-4-22

@author: Sindo
'''
# coding=utf-8

import os

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE,formatdate
from email.mime.multipart import MIMEMultipart

class Toolkit(object):
		@staticmethod
		def printSecSepor():
			print ""
			print "========================================================================"
			print "========================================================================"
			print "========================================================================"
			print ""
		
		@staticmethod
		def saveFileContent(fileName, fileData):
			fileObj = open(fileName, "wb") 
			
			fileObj.write(fileData)
			fileObj.close()
		
		@staticmethod
		def getFileContent(fileName):
			fileObj = open(fileName, "rt") 
			
			fileContent = ""
			strLine = fileObj.readline()
			
			while strLine:
				fileContent = fileContent + strLine
				strLine = fileObj.readline()
			
			return fileContent
		
		@staticmethod
		def sendMail(cfgDict, mailFrom, mailToList, subject, content, fileList=[]): 
			assert type(cfgDict) == dict 
			assert type(mailToList) == list 
			assert type(fileList) == list 
			
			mimeMsg = MIMEMultipart() 
			mimeMsg['From'] = mailFrom 
			mimeMsg['Subject'] = subject 
			mimeMsg['To'] = COMMASPACE.join(mailToList)     #COMMASPACE==', ' 
			mimeMsg['Date'] = formatdate(localtime=True) 
			mimeMsg.attach(MIMEText(content, "html", "UTF-8")) 
			
			for fileName in fileList: 
				part = MIMEBase('application', 'octet-stream') #'octet-stream': binary data 
				part.set_payload(open(file, 'rb'.read())) 
				encoders.encode_base64(part) 
				part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(fileName)) 
				mimeMsg.attach(part) 
			
			import smtplib 
			smtp = smtplib.SMTP(cfgDict['host']) 
			smtp.login(cfgDict['user'], cfgDict['pswd']) 
			smtp.sendmail(mailFrom, mailToList, mimeMsg.as_string()) 
			smtp.close()
			
			return True
			
if __name__ == '__main__':
	print "Toolkit_process_begin......" 
	
	resVal = False
	
	userName = 'lijj'
	userPswd = os.getenv("aintPswd")
	
	if resVal: print "congratulations_your_work_is_successful" 
	else:      print ":( unfortunately_your_work_is_failed ):"