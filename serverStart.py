# encoding: utf-8
from socket import *
from time import ctime
from xinyou import action
import subprocess
import traceback
import tempfile

HOST = ''
# 获取Sconfig.ini  返回[gamedir,PORT]
sconfig = action.getSconfig()
PORT = int(sconfig[1])
gamedir = sconfig[0]
print('端口：' + str(PORT))
print('游戏目录：' + gamedir)

BUFSIZ = 2048
ADDR = (HOST, PORT)
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# tcpSerSock.setblocking(0)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
	print('waiting for connection...')
	tcpCliSock, addr = tcpSerSock.accept()
	print('...connected from:', addr)

	dirINFO = action.getDirINFOstr(gamedir)
	print(dirINFO)
	tcpCliSock.send(('[%s]@%s' % (bytes(ctime(), 'utf-8'), dirINFO)).encode())
	while True:
		data = tcpCliSock.recv(BUFSIZ).decode()
		out_temp = tempfile.SpooledTemporaryFile(max_size=10 * 1000)
		fileno = out_temp.fileno()

		if not data:
			break
		# if data == '2':
		# 	a=action.getDirINFO(gamedir)
		# 	print(type(a))
		# 	tcpCliSock.send(('[%s] %s' %(bytes(ctime(),'utf-8'),a)).encode())
		# 	print(a)
		# else:
		# 	tcpCliSock.send(('[%s] %s' %(bytes(ctime(),'utf-8'),data)).encode())
		# 	print(data)
		# 	print(type(data))
		if data == '1':
			xml = '疯狂跑得快初级场12611'
			path = 'E:\\Game\\26CrazyRunFastServer'
			a = subprocess.run(
				"for /f %i in (\'dir \"" + path + "\\run\\" + xml + ".xml\" /s /b\') do (start " + path + "\\ServiceLoader.exe \"auto\" \"%i\" && ping 127.0.0.1 /n 3 >nul)",
				stdout=fileno, shell=True)
			# a.wait()
			out_temp.seek(0)
			lines = out_temp.readlines()
			out_temp.close()
			print(lines)
			linesSend = []
			for i in lines:
				linesSend.append(i.decode('gbk'))
			# 信息简化后传输

			tcpCliSock.send(('[%s] %s' % (bytes(ctime(), 'gbk'), linesSend)).encode())
		else:
			tcpCliSock.send(('[%s] %s' % (bytes(ctime(), 'utf-8'), data)).encode())
			print(data)
			print(type(data))

	tcpCliSock.close()
tcpSerSock.close()	