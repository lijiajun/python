#-*- encoding: gb2312 -*-
import os,sys
import paramiko
import threading  

rightHostAddr = "Not Available"

def try_sshHost(hostAddr, hostUser, hostPswd, testCmds):  
	try:  
		ssh = paramiko.SSHClient()  
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
		ssh.connect(hostAddr, 22, hostUser, hostPswd, timeout=3)
		
		for m in testCmds:  
			stdin, stdout, stderr = ssh.exec_command(m)  
#		   stdin.write("Y")   #简单交互，输入 ‘Y’   
			out = stdout.readlines()  
			#屏幕输出  
			for o in out:  
				print o,  
		print '%s\t!!!!!!!!!! Host Fount !!!!!!!!!!\n' % (hostAddr)
		
		global rightHostAddr 
		rightHostAddr = hostAddr;
		ssh.close()  
	except :  
		print '%s\tError\n' % (hostAddr)
		
if __name__=='__main__':  
	hostIpSeg= "192.168.0"
	if len(sys.argv)>1:
		hostIpSeg= sys.argv[1]
		
	testCmds = ['echo hello world!']	#执行命令列表  
	
	#hostIpSeg= "10.10.15"
	hostUser = "linaro"  				#主机用户  
	hostPswd = "lijiajun"				#主机密码  
	#hostUser="hiwifi"
	#hostPswd="admin"
	
	threads = []   						#多线程  
	print "Begin......" 
	for i in range(1,255):  
		hostAddr = hostIpSeg + "." + str(i)
		thread = threading.Thread(target=try_sshHost,args=(hostAddr, hostUser, hostPswd, testCmds))   
		thread.start()
		threads.append(thread)
		
	for thread in threads:
		thread.join()
		
	print "hostAddr is %s." % (rightHostAddr)