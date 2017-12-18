#encoding: utf-8

from xinyou import Color
from xinyou import action
from xinyou import caction
from socket import *
import os,time

colorPrint = Color()
# colorPrint.print_green_text('fdsfa')
#当前管理的游戏
currentGame=''
#当前消息
currentMsg=''
# 命令动作
cmdAction = ['start','update','get','push','show']

HOST = '121.196.201.156'
PORT= 21567
BUFSIZ = 2048
ADDR = (HOST,PORT)

tcpCliSock = socket(AF_INET,SOCK_STREAM)
tcpCliSock.connect(ADDR)

print('连接成功:'+str(tcpCliSock.getpeername()))
# 拿到服务器第一次发过来的table
firstINFO = tcpCliSock.recv(BUFSIZ).decode()
print(firstINFO)
#将str table转换成List
table = caction.unpackDirINFOstr(firstINFO)
print(table)


#打印所有游戏主目录
caction.printGameDir(table[1])



#控制是否读取服务器端消息的开关
recv_status= True

while True:
    
    # data = tcpCliSock.recv(BUFSIZ).decode()
    # if not data:
    #     print('没有消息，退出~')
    #     break
	#
    # recvCheck = caction.recvCheck(data)
    # if recvCheck:
    #     table = caction.recvOperate(recvCheck)
    #

    data = input(currentGame+':>')

    #命令简单判断
    if not caction.command_simpleCheck(data,cmdAction,currentGame,table[1]):
        continue

    if data == 'cls':
        os.system('cls')
        continue

    if data == 'exit':
        tcpCliSock.close()
        break

    if not data:
        break



    # 发送命令
    tcpCliSock.send(data.encode())
    time.sleep(0.1)

    # 接收数据
    data = tcpCliSock.recv(BUFSIZ).decode()
    if not data:
        break
    # print(data)

    caction.recvBackMSG(data,currentGame)
    back_messageList = data.split('@')
    if back_messageList[0] =='currentGame':
        currentGame = back_messageList[1]

    # colorPrint.print_green_text(action.formatMessage(data))

tcpCliSock.close()




