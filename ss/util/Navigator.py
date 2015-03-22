#!user/bin/env python
#-*- coding:utf-8 -*-
'''
对urllib和urllib2的简单封装，方便使用。
提供header伪装、历史记录、gzip解码功能。
'''

import base64 
import urllib,urllib2,cookielib
import gzip,zlib,StringIO
import re,sys

class Navigator(object):
    # 默认的进度显示函数
    @staticmethod
    def Percent(a,b,c):
        i=float(a*b*100)/c
        if i>100.0:i=100.0
        x=int(i/2)
        sys.stderr.write('|')
        for j in xrange(x):sys.stderr.write('=')
        for j in xrange(50-x):sys.stderr.write('-')
        sys.stderr.write('|%6.2f%%\r'%(i))
        
    # 创建一个opener，伪装成浏览器
    def __init__(self, userName, userPswd,proxy=None):
        self.trace=[]
        
        self.header= {
            'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Accept-Encoding':'gzip,deflate',
            'Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.7',
            'Connection':'Keep-Alive'
        }
        if userName:
            auth = base64.b64encode(userName+ ':'+ userPswd)
            self.header["Authorization"] = "Basic "+ auth
        
        self.timeout=5
        self.proxy=proxy
        self.resp=None
        self.page=None
        self.cookie=urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        if proxy:
            self.opener=urllib2.build_opener(self.cookie,urllib2.ProxyHandler(proxy),urllib2.HTTPHandler)
        else:
            self.opener=urllib2.build_opener(self.cookie,urllib2.HTTPHandler)
    # 关闭opener
    def __del__(self):
        self.opener.close()
        
    # 建立网页连接
    def call(self, url, query=None, data=None):
        if query:
            url='%s?%s'%(url,urllib.urlencode(query))
        if self.trace:
            ref=self.trace[-1]
            if 'Host' in self.header and ref.split('/')[1]==self.header['Host']:
                self.header['Referer']=ref
            else:
                if 'Host' in self.header:del self.header['Host']
                if 'Referer' in self.header:del self.header['Referer']
        req=urllib2.Request(url,headers=self.header)
        req.timeout=self.timeout
        if data:
            self.resp=self.opener.open(req,urllib.urlencode(data))
        else:
            self.resp=self.opener.open(req)
        self.header['Host']=url.split('://')[1].split('/')[0]
        self.trace.append(url)
        
    # 读取网页内容，如果是压缩数据则自动解码
    def read(self,readLen=0):
        if readLen>0:
            medi=self.resp.read(readLen)
        else:
            medi=self.resp.read()
        if self.resp.headers.get('content-encoding')=='deflate':
            try:
                self.page=zlib.decompress(medi,-zlib.MAX_WBITS)
            except zlib.error:
                self.page=zlib.decompress(medi)
        elif self.resp.headers.get('content-encoding')=='gzip':
            obj=StringIO.StringIO(medi)
            self.page=gzip.GzipFile(fileobj=obj,mode="r").read()
        else:
            self.page=medi
            
        #print "Set-Cookie:" + self.resp.headers.get("Set-Cookie")
        
        return self.page
    
    # 下载文件并可显示进度
    def load(self,url,name,fac=None):
        self.call(url)
        size=int(self.resp.headers.getheader('content-length'))
        have=0
        if not fac:
            fac=Navigator.Percent
        fac(0,1,size)
        try:
            with open(name,'wb') as downFile:
                while have<size:
                    data=self.read(65536)
                    downFile.write(data)
                    have+=65536
                    fac(have,1,size)
            return True
        except:
            return False
        
    # 打开并获取页面内容
    def obtain(self,url,query=None,data=None):
        self.call(url,query,data)
        return self.read()
    
    # 正则表达式提取第一个
    def search(self,rule):
        if self.page:
            return re.search(rule,self.page)
        return None
    
    # 正则表达式提取全部
    def getall(self,rule):
        if self.page:
            return re.findall(rule,self.page)
        return []

class Webproxy(object):
    def __init__(self,web,proxy=None):
        self.client=Navigator(proxy)
        self.webpxy=web
        self.query={'u':None,'b':'4','f':'norefer'}
    
    def __del__(self):
        del self.client
    
    def call(self,url,query=None,data=None):
        self.query['u']=url
        trs='http://%s/browse.php?%s'%(self.webpxy,urllib.urlencode(self.query))
        self.client.call(trs,query,data)
        if 'f' in self.query:del self.query['f']
    
    def read(self, readLen=0):
        return self.client.read(readLen)
    
    def load(self,url,name,fac=None):
        return self.client.call(url,name,fac)
    
    def obtain(self,url,query=None,data=None):
        self.client.call(url,query,data)
        return self.client.read()
    
    def search(self,rule):
        return self.client.search(rule,self.page)
    
    def getall(self,rule):
        return self.client.findall(rule,self.page)
        
if __name__=='__main__':
    pass
    