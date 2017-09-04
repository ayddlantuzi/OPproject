#encoding: utf-8
from socket import *
from time import ctime
from xinyou import action
import subprocess
import traceback
import tempfile



HOST=''
# 获取Sconfig.ini  返回[gamedir,PORT]
sconfig = action.getSconfig()
PORT=int(sconfig[1])
gamedir = sconfig[0]

BUFSIZ=2048
ADDR = (HOST,PORT)

tcpSerSock = socket(AF_INET,SOCK_STREAM)
# tcpSerSock.setblocking(0)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

#判断客户端第一次连接时候  发送游戏目录消息的状态   用过一次后设置为False
send_dirinfo_status = True
while True:
	print('waiting for connection...')
	tcpCliSock, addr = tcpSerSock.accept()
	print('...connected from:',addr)

# 首次链接时候，将游戏目录的信息发送的客户端
	if send_dirinfo_status:
		ServiceLoaderINFO=action.getDirINFOstr(gamedir)
		tcpCliSock.send(('[%s] %s' %(bytes(ctime(),'utf-8'),'@'+ServiceLoaderINFO)).encode())
		print(ServiceLoaderINFO)
		send_dirinfo_status = False

	while True:
		data = tcpCliSock.recv(BUFSIZ).decode()
		# out_temp = tempfile.SpooledTemporaryFile(max_size=10*1000)
		# fileno = out_temp.fileno()


		# 接受到command 校验 和执行


		if not data:
			break
		tcpCliSock.send(('[%s] %s' %(bytes(ctime(),'utf-8'),data)).encode())
		print(ctime()+' message:'+ data)






		# if data == '1':
		# 	xml = '疯狂跑得快初级场12611'
		# 	path = 'D:\\26CrazyRunFastServer'
		# 	a=subprocess.run("for /f %i in (\'dir \""+path+"\\run\\"+xml+".xml\" /s /b\') do (start "+path+"\\ServiceLoader.exe \"auto\" \"%i\" && ping 127.0.0.1 /n 3 >nul)",stdout=fileno,shell=True)
		# 	# a.wait()
		# 	out_temp.seek(0)
		# 	lines = out_temp.readlines()
		# 	out_temp.close()
		# 	print(lines)
		# 	linesSend=[]
		# 	for i in lines:
		# 		linesSend.append(i.decode('gbk'))
		# 	tcpCliSock.send(('[%s] %s' %(bytes(ctime(),'utf-8'),linesSend)).encode())
		# 	print(linesSend)
		# else:
		# 	tcpCliSock.send(('[%s] %s' %(bytes(ctime(),'utf-8'),data)).encode())
		# 	print(data)
		# 	print(type(data))
		
	tcpCliSock.close()
tcpSerSock.close()	