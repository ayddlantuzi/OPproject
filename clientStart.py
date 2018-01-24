#encoding: utf-8

from xinyou import Color
from xinyou import action
from xinyou import caction,saction
from socket import *
import os,time

colorPrint = Color()
# colorPrint.print_green_text('fdsfa')
#当前管理的游戏
currentGame=''
#当前消息
currentMsg=''
# 命令动作
cmdAction = ['start','update','get','put','show','back','compare']

HOST = '121.196.201.156'
PORT= 21567
BUFSIZ = 2048
ADDR = (HOST,PORT)

tcpCliSock = socket(AF_INET,SOCK_STREAM)
tcpCliSock.connect(ADDR)

print('连接成功:'+str(tcpCliSock.getpeername()))
# 拿到服务器第一次发过来的table
firstINFO = tcpCliSock.recv(BUFSIZ).decode()
# print(firstINFO)
#将str table转换成List
table = caction.unpackDirINFOstr(firstINFO)
# print(table)


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
    checkResult = caction.command_simpleCheck(data,cmdAction,currentGame,table[1])
    if checkResult == False:
        continue
    elif type(checkResult) == list:
        if checkResult[0] == 'put':
            data = 'put ' + checkResult[1]
        elif checkResult[0] == 'update':
            data = 'update '+ checkResult[1]

    if data == 'cls':
        os.system('cls')
        continue

    if data == 'exit':
        tcpCliSock.close()
        break



    if not data:
        break


    # print('发送的命令：',end='')
    # print(data)
    # 发送命令
    tcpCliSock.send(data.encode())
    time.sleep(0.1)

    # 接收数据
    data = tcpCliSock.recv(BUFSIZ).decode()
    if not data:
        break
    # print(data)

    # caction.recvBackMSG(data,currentGame)
    back_msgList = data.split('+')
    # print('client 接收到的消息#')
    # print(back_msgList)
    for onecmd in back_msgList:
        back_msg_str = onecmd.split('@')
        if back_msg_str[0]=='print':
            print(back_msg_str[1])
        elif back_msg_str[0] =='currentGame':
            currentGame = back_msg_str[1]
        elif back_msg_str[0] == 'get':
            caction.transfer_File(HOST,currentGame,caction.transfer_list_str_2_list(back_msg_str[1]),'get')
        elif back_msg_str[0] == 'put':
            caction.transfer_File(HOST,currentGame,caction.transfer_list_str_2_list(back_msg_str[1]),'put')
        elif back_msg_str[0] =='update':
            caction.transfer_File(HOST,currentGame,caction.transfer_list_str_2_list(back_msg_str[1]),'update')
        elif back_msg_str[0] == 'compare':
            caction.compare_cmd_client(currentGame,back_msg_str[1])
        else:
            pass
            # print('client调试',end='')
            # print(back_msg_str)
        # colorPrint.print_green_text(action.formatMessage(data))

tcpCliSock.close()




