#encoding: utf-8
import os
import socket
import os.path
import configparser
import codecs
import re
import tempfile
import time
import subprocess



def command_simpleCheck(command,cmdaction,currentGame,gameDir):
    '''
    对input的字符进行简易 错误判断

    命令是否是空字符串
    命令个数是否超过限制 3个
    命令开头是否为可执行命令

    :param command: input 的字符串
    :param cmdaction: 命令动作List ['start','update']
    :return: True 通过  False 有误，重新输入
    '''
    cmd = command.strip()
    if cmd == '':
        return False

    cmdList = cmd.split()
    if len(cmdList)>3:
        print('错误!!!  命令数超过3个')
        return False

    if len(cmdList)>1:
        if not cmdList[0] in cmdaction:
            print('错误!!!   '+ cmdList[0] +'  命令动作不存在')
            return False
        else:
            if currentGame == '':
                print('请先选择游戏目录:')
                printGameDir(gameDir)
                return False
    return True


def recvBackMSG(data,currentGame):
    '''
    接收动作执行后的 返回消息
    :param data: 返回的str
    :return:.
    '''
    back_messageList = data.split('@')
    if back_messageList[0] =='currentGame':
        currentGame = back_messageList[1]


    if back_messageList[0] =='print':
        print(back_messageList[1])



def unpackDirINFOstr(dirStr):
    '''
    将客户端收到的 getDirINFOstr解析成list
    :param dirStr: 接收到的字符串
    :return: 返回 List 集合
    '''
    strList = dirStr.split('@')
    dirList = strList[1].split('$')
    firstList = dirList[0].split('?')
    secondList = dirList[1].split('?')
    thirdList = []
    for i in dirList[2].split('#'):
        if '?' in i:
            j = i.split('?')
        else:
            j = i.split('?')
        thirdList.append(j)
    return [firstList, secondList, thirdList]


#服务端发来的消息  第一层 筛选判断
#两个参数，第二参数 为消息
#三个参数，第二参数为动作标识，第三参数
def recvCheck(data):
    strList= data.split('@')
    len_data = len(strList)
    if len_data == 3:
        if strList[1] == 'dirinfo':
            return strList[2]
        else:
            print(data)
            return False
    elif len_data == 2:
        print(strList[1])
        return False
    else:
        print(data)
        return False
    
    
#将客户端收到的 getDirINFOstr解析成list
def recvOperate(data):
    dirList = data.split('$')
    firstList = dirList[0].split('?')
    secondList = dirList[1].split('?')
    thirdList = []
    for i in dirList[2].split('#'):
        if '?' in i:
            j = i.split('?')
        else:
            j = i.split('?')
        thirdList.append(j)
    return [firstList,secondList,thirdList]
    



#将客户端收到的 getDirINFOstr解析成list
def unpackDirINFOstr(dirStr):
    strList = dirStr.split('@')
    dirList = strList[1].split('$')
    firstList = dirList[0].split('?')
    secondList = dirList[1].split('?')
    thirdList = []
    for i in dirList[2].split('#'):
        if '?' in i:
            j = i.split('?')
        else:
            j = i.split('?')
        thirdList.append(j)
    return [firstList,secondList,thirdList]



#读取客户端配置文件，返回 [[ip,port],[ip,port]....]
def getConfig():
    configINI = configparser.SafeConfigParser()
    configINI.read('config.ini')
    tempReturn = []
    for s in configINI.sections():
        tempReturn.append([configINI.get(s,'ip'),configINI.get(s,'port')])
    return tempReturn


def printGameDir(gameDirList):
    '''
    打印游戏目录
    :param gameDirList:
    :return:
    '''
    for i in gameDirList:
        print(i)



