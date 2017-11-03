#encoding: utf-8

from xinyou import Color
from xinyou import action
from xinyou import caction
from socket import *

colorPrint = Color()
# colorPrint.print_green_text('fdsfa')
#当前管理的游戏
currentGame=''
#当前消息
currentMsg=''

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
table = action.unpackDirINFOstr(firstINFO)
print(table)


#打印所有游戏主目录
for i in table[1]:
    print(i)



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
    
    #空命令判断
    if data.strip() == '':
        temp=True
        continue
    
    #判断语句合法性
    # commandStatus = action.command_check(data, currentGame, table)
    # print('commandStatus',end='')
    # print(commandStatus)
    # if commandStatus[0]:
    #     if commandStatus[1].isdigit():
    #         tcpCliSock.send((currentGame+'@'+data).encode())
    #     else:
    #         currentGame = commandStatus[1]
    #         temp=True
    # else:
    #     currentMsg = commandStatus[1]
    #     temp=True
    #     print(currentMsg)
        

    #确认语句可以执行，发送command
    if not data:
        break
    tcpCliSock.send(data.encode())
    data = tcpCliSock.recv(BUFSIZ).decode()
    if not data:
        break
    print(data)

    # colorPrint.print_green_text(action.formatMessage(data))

tcpCliSock.close()




