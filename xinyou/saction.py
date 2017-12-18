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

gamedir = ''

def runServiceLoader(path,xml):
    '''
    运行房间 path路径，xml配置文件list
    :param path: 游戏路径 str
    :param xml: 游戏配置文件 list
    :return: 启动游戏后的消息  格式 'E:/game/游戏/12001.xml   命令执行！/r/n' 返回
    '''
    run_msg_list = []

    # 筛选房间xml
    # 判断传入的是 部分xml还是all 并做初步的错误检查
    xml_list_getgamexml,error_msg_1 = get_gamexmlANDport(path,xml)
    # 判断端口是否被占用 占用的剔除
    xml_list,error_msg = check_xml_port_open(xml_list_getgamexml)
    error_msg.extend(error_msg_1)


    # xml = '疯狂跑得快初级场12611'
    # path = 'D:\\Game\\26CrazyRunFastServer'
    if xml_list[0] != 0:
        out_temp = tempfile.SpooledTemporaryFile(max_size=10 * 1000)
        fileno = out_temp.fileno()

        for xml_name in xml_list[1]:
            a=subprocess.run("for /f %i in (\'dir \""+path+"\\run\\"+xml_name+"\" /s /b\') do (start "+path+"\\ServiceLoader.exe \"auto\" \"%i\" && ping 127.0.0.1 /n 3 >nul)",stdout=fileno,shell=True)
            # a=subprocess.run("for /f %i in (\'dir \""+path+"\\run\\"+xml_name+".xml\" /s /b\') do (start "+path+"\\ServiceLoader.exe \"auto\" \"%i\" && ping 127.0.0.1 /n 3 >nul)",stdout=fileno,shell=True)

            time.sleep(0.5)
        # a.wait()
        out_temp.seek(0)
        lines = out_temp.readlines()
        out_temp.close()
        linesSend=[]
        for i in lines[1::2]:
            linesSend.append(i.decode('gbk'))
            print(i)

        run_msg_list = format_RunserviceLoader_Log(linesSend)


    all_msg_list = error_msg + run_msg_list
    all_msg_str = msgList_2_msgStr(all_msg_list)
    print('runServiceLoader  return:',end='')
    print(all_msg_str)
    return ('%s@%s' %('print',all_msg_str))

def msgList_2_msgStr(msgList):
    '''
    将信息的list 转换成str 返回给send
    :param msgList: 所有消息集合的Lists
    :return: 所有消息的str
    '''
    # print('msglist:')
    # print(msgList)
    n = len(msgList)
    # print('msglist   len:'+str(n))
    msgStr = ''
    for msg in msgList:
        msgStr += msg
        n -= 1
        if n != 0:
            msgStr += '\r\n'
    # print('msgStr:')
    # print(msgStr)
    return msgStr


def format_RunserviceLoader_Log(msgList):
    '''
    将cmd启动脚本返回的str 过滤 简约显示，内容：*****.xml  启动成功
    :param msgList:启动消息List
    :return:
    '''
    # print('formatbefore:',end='')
    # print(msgList)
    return_msg_list = []
    for msg in msgList:
        a = msg.find('auto')+7
        b = msg.find('.xml')+4
        c = msg[a:b].split('\\\\')
        return_msg_list.append(c[0] + '   启动命令执行!')

    # print('formatafter:',end='')
    # print(return_msg_list)

    return return_msg_list


def get_gamexmlANDport(path,xml):
    '''
    获得run目录下所有的房间配置
    :param path: 游戏目录
    :param xml: 启动的 游戏xml
    :return:[n,[],[]] [xml文件List，对应xml的Port List]
    端口号都是5位数字
    '''
    print('get_gamexmlANDport   start')
    temp_file = []
    xml_file = []
    temp_port = []
    error_msg = []
    n = 0

    all_file = os.listdir(path + '\\run')
    status = True
    for file in all_file:
        if os.path.splitext(file)[1] == '.xml':
            xml_file.append(file)
            status = False

    if status:
        msg = gamedir + '游戏目录run下没有xml '
        error_msg.append(msg)
        returnList = [0,[],[]]
        return returnList,error_msg


# 输入的[10021,10022] 检测端口 是否在xml 房间配置文件名中
    if type(xml) == list:
        for port in xml:
            status = True
            for file in xml_file:
                fileport = re.sub('\D','',file)
                if port == file:
                    temp_file.append(file)
                    temp_port.append(port)
                    n += 1
                    status = False
            if status:
                msg = '端口   '+ port + '   未匹配到对应的房间名称!'
                error_msg.append(msg)

# 信息提示需要修改？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？
    elif xml == 'all':
        for file in xml_file:
            port = file[:-4][-5:]
            if port.isdigit():
                temp_file.append(file)
                temp_port.append(port)
                n += 1
            else:
                error_msg.append(file+'端口异常，请检查!(文件名末尾5位数字端口 命名规则)')

    else:
        status = True
        for file in xml_file:
            port = file[:-4][-5:]
            # print('port:'+port)
            # print('xml:'+ xml)
            if xml == port:
                temp_file.append(file)
                temp_port.append(port)
                n += 1
                status = False
                break
        if status:
            error_msg.append('端口   '+ xml + '   未匹配到对应的房间名称!')

    returnList = [n,temp_file,temp_port]

    print('get_gamexmlANDport  end')
    print(returnList)
    return returnList,error_msg


def check_xml_port_open(xmllist):
    '''
    检查房间xml的端口是否占用
    :param xmllist:
    :return:
    '''
    print('check_xml_port_open   start')
    print('xmllist:',end='')
    print(xmllist)
    error_msg = []
    n = xmllist[0]
    if xmllist[0] != 0:
        for port in xmllist[2][:]:
            print('port:'+port)

            # if int(port) > 15000:
            #     xmllist[1].pop(0)
            #     xmllist[2].pop(0)
            #     n -= 1
            #     msg = xml+ '   端口超出范围！'
            #     error_msg += msg +'\r\n'
            #     print(msg)

            if portISopen(int(port)):
                index = xmllist[2].index(port)
                xmllist[1].pop(index)
                xmllist[2].pop(index)
                n -= 1
                msg = port + '   端口被占用！'
                error_msg.append(msg)
                print(msg)

        xmllist[0] = n

    print('check_xml_port_open  end')
    return xmllist,error_msg


def portISopen(port):
    '''
    判断本地端口是否占用  True占用   False未占用
    :param port:
    :return:
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)
    try:
        ADDR = ('127.0.0.1', port)
        s.connect(ADDR)
        s.shutdown(2)
        return True
    except Exception as e:
        print(e)
        return False



def getDirINFO(path):
    '''
    遍历目录下的所有目录和文件
    firstList  根目录下所有的文件和目录
    secondList 根目录所有包括run子目录的 目录
    thirdList  所有子目录run 下面的.xml文件 []
    :param path:
    :return: [firstList,secondList,thirdList集合]
    '''
    firstList = os.listdir(path)
    # print('firstList:',end='')
    # print(firstList)

    secondList = []
    for i in firstList:
        a = path + i
        if os.path.isdir(a) and os.path.isdir(a + '\\run'):
            secondList.append(i)
    # print('secondList:',end='')
    # print(secondList)

    thirdList = []
    for i in secondList:
        a = path + i
        temp = []
        for m in os.listdir(a + '\\run'):
            if m[-4:] == '.xml':
                temp.append(m)
        thirdList.append(temp)
    # print(thirdList)
    return [firstList, secondList, thirdList]


def getDirINFOstr_and_list(path):
    firstList = os.listdir(path)
    # print('firstList:',end='')
    # print(firstList)

    secondList = []
    for i in firstList:
        a = path + i
        if os.path.isdir(a) and os.path.isdir(a + '\\run'):
            secondList.append(i)
    # print('secondList:',end='')
    # print(secondList)

    thirdList = []
    for i in secondList:
        a = path + i
        temp = []
        for m in os.listdir(a + '\\run'):
            if m[-4:] == '.xml':
                temp.append(m)
        thirdList.append(temp)
    # print(thirdList)

    tempReturn = ''
    for i in firstList:
        tempReturn = tempReturn + i + '?'
    tempReturn = tempReturn[:-1] + '$'
    # print('firstList:')
    # print(firstList)
    # print('tempReturn:')
    # print(tempReturn)

    for i in secondList:
        tempReturn = tempReturn + i + '?'
    tempReturn = tempReturn[:-1] + '$'
    # print('secondList:')
    # print(secondList)
    # print('tempReturn:')
    # print(tempReturn)

    for i in thirdList:
        for j in i:
            k = '3'
            # 判断xml的端口是否启用 3默认  1启用  0未启用
            if portISopen(getPortFromXML(j)):
                k = '1'
            else:
                k = '0'
            # 端口的状态绑定在发过去的xml最后一位
            tempReturn = tempReturn + j + k + '?'
        tempReturn = tempReturn[:-1] + '#'
    tempReturn = tempReturn[:-1]
    # print('thirdList')
    # print(thirdList)
    return tempReturn,[firstList,secondList,thirdList]


#读取服务器端配置文件，返回 [游戏目录,port]
def getSconfig():
    global gamedir
    configINI = configparser.SafeConfigParser()
    #configINI.read('..\Sconfig.ini')
    configINI.read('Sconfig.ini')
    gamedir = configINI.get('Server','gamedir')
    port = configINI.get('Server','port')
    tempReturn=[gamedir,port]

    return tempReturn

# 根据xml文件名 筛选里面的端口
def getPortFromXML(xmlName):
    return int(xmlName[-9:][:5])



def oneCommand_check(str,secondList,currentGame):
    '''
    判断输入的数字或字符是否 在目录名中  返回目录名
    :param kindid:
    :param secondList: table[1]
    :return:
    '''
    status = False

    for i in secondList:
        if str.upper() in i.upper():
            currentGame[0] = i
            status = True
            break

    if status:
        msg = ('%s@%s' % ('currentGame', currentGame[0]))
    else:
        msg = ('%s@%s 匹配不到游戏目录，请重新输入！' % ('print', str))
    return msg

def twoCommand_check(cmdList,currentGame):
    '''

    :param cmdList:
    :param currentGame:
    :return:
    '''
    global  gamedir
    if currentGame[0] == '':
        msg = ('%s@%s' % ('print', '请先选择游戏目录！'))
        return msg


    if cmdList[0] == 'start':
        if ',' in cmdList[1]:
            room = cmdList[1].split(',')
            msg = runServiceLoader(gamedir+'\\'+currentGame[0],room)
        else:
            msg = runServiceLoader(gamedir+'\\'+currentGame[0],cmdList[1])

    elif cmdList[0] == 'show':
        pass

    elif cmdList[0] == 'get':
        pass

    elif cmdList[0] == 'push':
        pass

    elif cmdList[0] == 'update':
        pass

    return msg


def command_ServerCheck(command,currentGame,table):
    '''
    检查命令的可执行性
    :param command:server端接收到的命令
    :param currentGame:当前游戏
    :param table:当前服务器 游戏资源表
    :return:
    '''
    cmdList = command.split()
    cmdNum = len(cmdList)


    msg = ''

    # 判断是否是单个命令
    if cmdNum == 1:
        msg = oneCommand_check(cmdList[0],table[1],currentGame)
    else:
        msg = twoCommand_check(cmdList,currentGame)


    return msg

