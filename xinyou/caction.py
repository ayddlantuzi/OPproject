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
import paramiko
from xinyou import saction


# 默认桌面目录
desktop_dir = 'D:\\Desktop\\'
# svn目录
svnServiceLoader_dir = 'D:\\SvnGame\\服务器版本\\游戏服务VS2015\\'
# 单款目录
dlls_dir = 'D:\\SvnGame\\服务器版本\\单款游戏服务\\'

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
    if len(cmdList) == 1:
        return True

    if len(cmdList)>2:
        print('错误!!!  命令数超过2个')
        return False

    if len(cmdList)==2:
        if currentGame == '':
            print('请先选择游戏目录:')
            printGameDir(gameDir)
            return False

        if not cmdList[0] in cmdaction:
            print('错误!!!   '+ cmdList[0] +'  命令动作不存在')
            return False
        elif cmdList[0] == 'put':
            # 判断桌面目录是否存在  上传的文件是否存在
            return put_check(currentGame,cmdList[1])
        elif cmdList[0] == 'update':
            # 判断上传的文件是否存在
            return update_check(currentGame,cmdList[1])
        elif cmdList[0] == 'back':
            if not cmdList[1] in ['ini','exe','dll']:
                print('back 命令错误help back 查询命令的使用方法！')
                return False

    return True


def update_check(currentGame,cmd_1):
    '''
    update 语句检查
    update exe  更新serviceLoader文件   确认目录是否存在，确认目录下是否有文件
    update dll  更新dll文件             确认目录是否存在，目录下是否有当前 游戏名称的dll
    :param currentGame:
    :param cmd_1:
    :return: False 不通过
    通过： 返回

    '''
    global svnServiceLoader_dir
    global dll_dir

    exe_file_str = ''
    if currentGame == '':
        print('请先选择 游戏目录！')
        return False

    if cmd_1 == 'exe':
        if os.path.exists(svnServiceLoader_dir):
            file = os.listdir(svnServiceLoader_dir)
            print(file)
            if len(file) == 0:
                print(svnServiceLoader_dir+' 下没有更新文件！')
            else:
                for f in file:
                    if not os.path.isdir(svnServiceLoader_dir+f):
                        flist = os.path.splitext(f)
                        if flist[1] == '.dll':
                            exe_file_str += f+'?'
                exe_file_str += 'ServiceLoader.exe?'+svnServiceLoader_dir
                print(exe_file_str)
                return ['update',exe_file_str]
        else:
            print('本地目录 '+svnServiceLoader_dir+' 不存在！')
    elif cmd_1 == 'dll':
        dll_name = re.sub('\d','',currentGame)+'.dll'
        dll_dir =dlls_dir + dll_name
        if os.path.exists(dll_dir):
            # 返回上传的dll文件
            return ['update',dll_name+'?'+dlls_dir]
        else:
            print('文件或目录 '+dlls_dir+' 不存在，请检查！')
            print('Tip：游戏目录命名规则  kindID+dll名称   例：22CrazyLand3renServer\n'
                  '     update dll 命令会根据  22CrazyLand3renServer 到dll文件夹寻找 CrazyLand3renServer.dll 文件！')
    else:
        print('update '+cmd_1+'  命令不正确！')
        print('命令帮助  help update')

    return False



def put_check(currentGame,get_fuzzy):
    '''
    上传文件时，先判断要上传的文件是否存在
    :param currentGame:
    :return: False 文件不存在
    文件存在  返回['put',文件列表 list]   list 用?分隔
    '''
    if not os.path.exists(desktop_dir+currentGame):
        os.makedirs(desktop_dir + currentGame)
        print(desktop_dir + currentGame + '   目录不存在，创建成功,请将文件放入此文件夹后再操作！')
        return False


    # filelist = []
    temp = False
    putfile_str = ''
    gamefile = os.listdir(desktop_dir+'\\'+currentGame)
    if get_fuzzy == 'ini':
        for file in gamefile:
            if file[-3:] == 'ini':
                temp = True
                putfile_str += file + '?'

                # target ='\\'+currentGame + '\\' + file
                # source = desktop_dir+currentGame+'\\'+file
                # filelist.append([source,target])

    else:
        if get_fuzzy in gamefile:
            temp = True
            putfile_str = get_fuzzy +'?'
            # target = '\\' + currentGame + '\\' + file
            # source = desktop_dir + currentGame + '\\' + file
            # filelist.append([source, target])
        else:
            print('桌面文件夹 '+currentGame+' 中没有 '+get_fuzzy+' 文件！')
            return False

    if temp:
        return ['put',putfile_str[:-1]]
    else:
        print('桌面文件夹 '+currentGame+' 中没有 '+'ini 的文件！')
        return False



# def recvBackMSG(data,currentGame):
#     '''
#     接收动作执行后的 返回消息
#     :param data: 返回的str
#     :return:.
#     '''
#     back_messageList = data.split('@')
#     if back_messageList[0] =='currentGame':
#         currentGame = back_messageList[1]
#
#
#     if back_messageList[0] =='print':
#         print(back_messageList[1])



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



def transfer_File(host,currentGame,fileList_Info,mode='put'):
    '''
    上传文件到游戏服务器
    :param host: 游戏服务器ip   str
    :param fileList_Info: 上传文件路径 和 目的文件路径(含文件名)  [['上传路径','目的路径']['','']['','']['','']]
    :param mode:   put 上传   get 下载
    :return: 执行在client端  消息直接打印
    '''
    transport  = paramiko.Transport(host,22)
    transport.connect(username='xinyou',password='EVxBhaTCWxUt')

    # 上传或下载前检查  桌面是否有currentGame目录 没有目录 默认创建
    if mode == 'get':
        if not os.path.exists(desktop_dir+currentGame):
            os.makedirs(desktop_dir+currentGame)
            print(desktop_dir+currentGame+'   目录不存在，创建成功！')


    if len(fileList_Info) != 0:
        try:
            sftp = paramiko.SFTPClient.from_transport(transport)
        except Exception as e:
            print(e)
        # 打印sftp 传输的 文件源和目标地址list
        # print('filelist:',end='')
        # print(fileList_Info)

        msgList = []
        maxlen = 0
        for filelist in fileList_Info:
            # 传输的文件名称
            filename = filelist[0].split('\\')[-1]
            filelen = len(filename)
            if filelen > maxlen:
                maxlen = filelen
            try:
                if mode == 'put':
                    sftp.put(filelist[0],filelist[1])
                    msgList.append(['文件',filename,'上传成功！'])
                    # print('文件 '+filelist[0].split('\\')[-1]+' 上传成功！')
                elif mode == 'get':
                    sftp.get(filelist[0],filelist[1])
                    msgList.append(['文件', filename, '成功下载到桌面目录！'])
                    # print('文件   '+filelist[0].split('\\')[-1]+'  成功下载到桌面目录!')
                elif mode == 'update':
                    sftp.put(filelist[0], filelist[1])
                    msgList.append(['文件',filename, '更新成功！'])
                    # print('文件   '+filelist[0].split('\\')[-1]+'  更新成功！')
                else:
                    print(mode + ' transfe rFile 模式错误！')
            except Exception as e:
                print(filelist[0],end='')
                print(filelist[1],end='')
                print(e)

        msg = saction.format_printMSG(msgList,2,maxlen)
        print(msg)
    else:
       print('上传文件列表为空！')


def transfer_list_str_2_list(liststr):
    '''
    get 操作  str 2 list           transfer文件用   Server  返回的 字符串  转换成 列表
    :param liststr:
    :return:[[],[],[],[],[]]
    '''
    returnList = []
    list1 = liststr.split('?')
    for l in list1:
        a = l.split('#')
        returnList.append(a)
    return returnList