#-*- encoding: gb2312 -*-
import os, sys, string
import poplib

# pop3��������ַ
host = "mail.asiainfo.com"
# �û���
username = "lijj@asiainfo.com"
# ����
password = os.getenv("aintPswd")
# ����һ��pop3�������ʱ��ʵ�����Ѿ������Ϸ�������
pp = poplib.POP3(host)
# ���õ���ģʽ�����Կ�����������Ľ�����Ϣ
pp.set_debuglevel(1)
# ������������û���
pp.user(username)
# ���������������
pp.pass_(password)
# ��ȡ���������ż���Ϣ��������һ���б���һ����һ���ж��Ϸ��ʼ����ڶ����ǹ��ж����ֽ�
ret = pp.stat()
print "! stat:%d {{{" % len(ret)
print ret
print "}}}"
# ��Ҫȡ�������ż���ͷ�����ż�id�Ǵ�1��ʼ�ġ�
for i in range(1, ret[0]+1):
	# ȡ���ż�ͷ����ע�⣺topָ�������������ż�ͷΪ�����ģ�Ҳ����˵��ȡ0�У�
	# ��ʵ�Ƿ���ͷ����Ϣ��ȡ1����ʵ�Ƿ���ͷ����Ϣ֮���ٶ�1�С�
	mlist = pp.top(i, 0)
	print 'line: ', len(mlist[1])
	
# �г����������ʼ���Ϣ��������ÿһ���ʼ������id�ʹ�С������stat��������ܵ�ͳ����Ϣ
ret = pp.list()

print "total mail count:%d" % len(ret)

for itList in ret:
	print itList
	
print "total mail count:%d" % len(ret)


try:
	# ȡ��һ���ʼ�������Ϣ���ڷ���ֵ��ǰ��д洢��down[1]���б���ġ�down[0]�Ƿ��ص�״̬��Ϣ
	down = pp.retr(1)
	print 'lines:', len(down)
	# ����ʼ�
	iLineNo = 0
	for line in down[1]:
		print "No%d:%s" % (iLineNo, line)
		iLineNo =  iLineNo + 1
except:
	print "real_mail_error"
# �˳�
pp.quit()