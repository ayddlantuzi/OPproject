# encoding: utf-8
from socket import *
from time import ctime
from xinyou import saction
import subprocess
import traceback
import tempfile

HOST = ''
# 获取Sconfig.ini  返回[gamedir,PORT]
sconfig = saction.getSconfig()
PORT = int(sconfig[1])
gamedir = sconfig[0]
print('端口：' + str(PORT))
print('游戏目录：' + gamedir)

#当前管理的游戏
currentGame=['']

BUFSIZ = 2048
ADDR = (HOST, PORT)
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# tcpSerSock.setblocking(0)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

dirINFO,dirList = saction.getDirINFOstr_and_list(gamedir)


while True:
    print('waiting for connection...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('...connected from:', addr)

    tcpCliSock.send(('[%s]@%s' % (bytes(ctime(), 'utf-8'), dirINFO)).encode())

    while True:
        data = tcpCliSock.recv(BUFSIZ).decode()
        out_temp = tempfile.SpooledTemporaryFile(max_size=10 * 1000)
        fileno = out_temp.fileno()

        if not data:
            break
        # 命令检查
        msg = saction.command_ServerCheck(data,currentGame,dirList)

        print('msg:'+msg)
        print('currentGame：'+currentGame[0])
        # tcpCliSock.send(('[%s]@%s' % (bytes(ctime(), 'utf-8'), commandINFO)).encode())
        tcpCliSock.send(bytes(msg,encoding='utf-8'))
        # if data == '1':
        #     # xml = '疯狂跑得快新手场12601'
        #     xml = 'all'
        #     path = 'E:\\Game\\26CrazyRunFastServer'
        #     lines = saction.runServiceLoader(path, xml)
        #     # print(lines)
        #     tcpCliSock.send(('[%s] %s' % (bytes(ctime(), 'utf-8'), lines)).encode())
        # # time.sleep()
        # else:
        #     tcpCliSock.send(('[%s] %s' % (bytes(ctime(), 'utf-8'), data)).encode())
        #     print(data)
        #     print(type(data))

    tcpCliSock.close()
tcpSerSock.close()
