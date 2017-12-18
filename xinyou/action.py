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
#cd /d %EDIR%
#for /f %%i in ('dir "%EDIR%\run\*.xml" /s /b') do (start %EDIR%\ServiceLoader.exe "auto" "%%i" && ping 127.0.0.1 /n 3 >nul)


def runServiceLoader(path,xml):
    '''
    运行房间 path路径，xml配置文件list
    :param path: 游戏路径 str
    :param xml: 游戏配置文件 list
    :return: 启动游戏后的消息  格式 'E:/game/游戏/12001.xml   命令执行！/r/n' 返回
    '''
    # 筛选房间xml
    # 判断传入的是 部分xml还是all 并做初步的错误检查
    xml_list_getgamexml,error_msg_1 = get_gamexmlANDport(path,xml)
    # 判断端口是否被占用 占用的剔除
    xml_list,error_msg = check_xml_port_open(xml_list_getgamexml)
    error_msg.extend(error_msg_1)

    out_temp = tempfile.SpooledTemporaryFile(max_size=10 * 1000)
    fileno = out_temp.fileno()

    # xml = '疯狂跑得快初级场12611'
    # path = 'D:\\Game\\26CrazyRunFastServer'
    if xml_list[0] != 0:
        for xml_name in xml_list[1]:
            a=subprocess.run("for /f %i in (\'dir \""+path+"\\run\\"+xml_name+".xml\" /s /b\') do (start "+path+"\\ServiceLoader.exe \"auto\" \"%i\" && ping 127.0.0.1 /n 3 >nul)",stdout=fileno,shell=True)
            time.sleep(0.5)
        # a.wait()
        out_temp.seek(0)
        lines = out_temp.readlines()
        out_temp.close()
        linesSend=[]
        for i in lines[1::2]:
            linesSend.append(i.decode('gbk'))
            print(i)
        returnStr = format_RunserviceLoader_Log(linesSend)

    # 另外附带  返回房间信息的  端口状态参数
    return returnStr


    # os.system("for /f %i in (\'dir \""+path+"\\run\\"+xml+".xml\" /s /b\') do (start "+path+"\\ServiceLoader.exe \"auto\" \"%i\" && ping 127.0.0.1 /n 3 >nul)")


def get_gamexmlANDport(path,xml=None):
    '''
    获得run目录下所有的房间配置
    :param path: 游戏目录
    :param xml: 启动的 游戏xml
    :return:[n,[],[]] [xml文件List，对应xml的Port List]
    端口号都是5位数字
    '''
    temp_file = []
    temp_port = []
    error_msg = []
    n = 0

    if type(xml) == list:
        for file in xml:
            if not os.path.exists(path+'\\run\\'+file):
                print(path+'\\run\\'+file+' 文件不存在！')
                continue
            port = re.sub('\D','',file)
            if len(port) == 5:
                temp_file.append(file)
                temp_port.append(port)
                n += 1
            else:
                msg = file+'   端口异常！'
                error_msg.append(msg)
                print(msg)
        returnList = [n,temp_file,temp_port]
    elif xml == 'all':
        all_file = os.listdir(path + '\\run')
        for file in all_file:
            if os.path.splitext(file)[1] == '.xml':
                port = re.sub('\D','', file)
                if len(port) == 5:
                    temp_file.append(file[:-4])
                    temp_port.append(port)
                    n += 1
                else:
                    msg = file + '   端口异常！'
                    error_msg.append(msg)
                    print(msg)
        returnList = [n, temp_file, temp_port]
    print('end 2')
    return returnList,error_msg

def check_xml_port_open(xmllist):
    print('check_xml_port_open   start')
    error_msg = []
    n = xmllist[0]
    if xmllist[0] != 0:
        for xml in xmllist[1][:]:
            print(xml)
            port = re.sub('\D','',xml)
            if int(port) > 15000:
                xmllist[1].remove(xml)
                n -= 1
                msg = xml+ '   端口超出范围！'
                error_msg.append(msg)
                print(msg)

            if portISopen(int(port)):
                xmllist[1].remove(xml)
                n -= 1
                msg = xml + '   端口被占用！'
                error_msg.append(msg)
                print(msg)

        xmllist[0] = n

    print('check_xml_port_open  end')
    return xmllist,error_msg


# 判断端口是否占用  True占用   False未占用
def portISopen(port):
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


def format_RunserviceLoader_Log(msgList):
    '''
    将cmd启动脚本返回的str 过滤 简约显示，内容：*****.xml  启动成功
    :param msgList:启动消息List
    :return:
    '''
    returnMSG=''
    for msg in msgList:
        a = msg.find('auto')+7
        b = msg.find('.xml')+4
        c = msg[a:b].split('\\\\')
        returnMSG += c[0]+'    启动命令执行！\r\n'

    return returnMSG




#遍历目录下的所有目录和文件
#firstList  根目录下所有的文件和目录
#secondList 根目录所有包括run子目录的 目录
#thirdList  所有子目录run 下面的.xml文件 []
#返回[firstList,secondList,thirdList集合]
def getDirINFO(path):
    firstList=os.listdir(path)
    # print('firstList:',end='') 
    # print(firstList)
    
    secondList = []
    for i in firstList:
        a=path+i
        if os.path.isdir(a) and os.path.isdir(a+'\\run'):
            secondList.append(i)
    # print('secondList:',end='')
    # print(secondList)

    thirdList = []
    for i in secondList:
        a = path+i
        temp = []
        for m in os.listdir(a+'\\run'):
            if m[-4:]=='.xml':
                temp.append(m)
        thirdList.append(temp)
    # print(thirdList)
    return [firstList,secondList,thirdList]

def getDirINFOstr(path):
    firstList=os.listdir(path)
    # print('firstList:',end='') 
    # print(firstList)
    
    secondList = []
    for i in firstList:
        a=path+i
        if os.path.isdir(a) and os.path.isdir(a+'\\run'):
            secondList.append(i)
    # print('secondList:',end='')
    # print(secondList)

    thirdList = []
    for i in secondList:
        a=path+i
        temp = []
        for m in os.listdir(a+'\\run'):
            if m[-4:]=='.xml':
                temp.append(m)
        thirdList.append(temp)
    # print(thirdList)
    
    tempReturn = ''
    for i in firstList:
        tempReturn = tempReturn + i + '?'
    tempReturn = tempReturn[:-1]+'$'
    #print('firstList:')
    #print(firstList)
    #print('tempReturn:')
    #print(tempReturn)
    
    for i in secondList:
        tempReturn = tempReturn+i+'?'
    tempReturn = tempReturn[:-1]+'$'
    #print('secondList:')
    #print(secondList)
    #print('tempReturn:')
    #print(tempReturn)
    
    for i in thirdList:
        for j in i:
            k='3'
            #判断xml的端口是否启用 3默认  1启用  0未启用
            if portISopen(getPortFromXML(j)):
                k='1'
            else:
                k='0'
            #端口的状态绑定在发过去的xml最后一位
            tempReturn = tempReturn+j+k+'?'
        tempReturn = tempReturn[:-1]+'#'
    tempReturn = tempReturn[:-1]
    #print('thirdList')
    #print(thirdList)
    return tempReturn
    
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
 
 
 
 #根据xml文件名 筛选里面的端口
def getPortFromXML(xmlName):
    return int(xmlName[-9:][:5])


#判断输入的数字是否 在目录名中  返回True
def inputKindID_check(kindid,secondList):
    kindidList = re.compile(r'\d+')
    #print(secondList)
    for i in secondList:
        #print(i)
        kindidFromDir = kindidList.findall(i)
        #print(kindidFromDir)
        if kindid == kindidFromDir[0]:
            return i
    return False


def command_simpleCheck(command,cmdaction):
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
        print('ERROR!!! 命令数超过3个')
        return False

    if len(cmdList)>1:
        if not cmdList[0] in cmdaction:
            print('ERROR!!!   '+ cmdList[0] +'  命令动作不存在')
            return False

    return True


def command_check(command,currentGame,table):
    '''
    判断命令可执行性质
    :param command: 接收到的命令
    :param currentGame: 当前Game
    :param table: 当前游戏资源列表
    :return: 返回命令是否可执行 True 可执行   False不可执行
    '''










# 判断输入命令，首个命令的合法性
# 返回 1  转向 start 命令
# 返回 2  转向 update命令
# 返回 3  转向 show  命令
def inputCommand_check(command,currentGame,table):
    commandList=command.split()
    print(commandList[0])
    if commandList[0] == 'start':
        return startCommand_check_client(commandList,currentGame,table)
    elif commandList[0] =='update':
        return 2
    elif commandList[0] =='show':
        return 3
    else:
        return [False,'命令错误~']

#client端 判断start语句是否合法 对比
def startCommand_check_client(commandList,currentGame,table):
    gameindex = table[1].index(currentGame)
    #存放校验过的端口
    portList = []
    #获取start命令中的端口号
    for i in commandList:
        if i.isdigit():
            gamexml = table[2][gameindex]
            for j in gamexml:
                if i in j:
                    portList.pop(i)
                    
    print('portList:',end='')
    print(portList)
    
    #合法端口数量>1的时候发送命令
    if len(portList)>0:
        return [True,1]
    else:
        return [False,'端口错误，或不在列表中！']
            
#server端 判断start 是否可以执行
def startCommand_check_server(command,currentGame,table,gamedir):
    commandList=command.split()
    xmlList = []
    for i in commandList:
        if i.isdigit():
            gamexml = table[2][gameindex]
            for j in gamexml:
                if i in j:
                    #再判断端口是否开启
                    if not portISopen(int(i)):
                        #需要检查###########################################
                        xmlList.pop(j)
    print('xmlList:',end='')
    print(xmlList)
    
    
    #启动xml
    out_temp = tempfile.SpooledTemporaryFile(max_size=10*1000)
    fileno = out_temp.fileno()    
    
    #xml = '疯狂跑得快初级场12611'
    #path = 'D:\\26CrazyRunFastServer'
    path = gamedir+currentGame
    for xml in xmlList:
        a=subprocess.run("for /f %i in (\'dir \""+path+"\\run\\"+xml+".xml\" /s /b\') do (start "+path+"\\ServiceLoader.exe \"auto\" \"%i\" && ping 127.0.0.1 /n 3 >nul)",stdout=fileno,shell=True)
        # a.wait()
        out_temp.seek(0)
        lines = out_temp.readlines()
        out_temp.close()
        linesSend=[]
	# for i in lines:
	#     linesSend.append(i.decode('gbk'))
	# tcpCliSock.send(('[%s] %s' %(bytes(ctime(),'utf-8'),linesSend)).encode())
	# print('发送的linesSend:',end='')  
	# print(linesSend)
    

    




#读取服务器端配置文件，返回 [游戏目录,port]
def getSconfig():
    configINI = configparser.SafeConfigParser()
    #configINI.read('..\Sconfig.ini')
    configINI.read('Sconfig.ini')
    gamedir = configINI.get('Server','gamedir')
    port = configINI.get('Server','port')
    tempReturn=[gamedir,port]
    return tempReturn


#读取客户端配置文件，返回 [[ip,port],[ip,port]....]
def getConfig():
    configINI = configparser.SafeConfigParser()
    configINI.read('config.ini')
    tempReturn = []
    for s in configINI.sections():
        tempReturn.append([configINI.get(s,'ip'),configINI.get(s,'port')])
    return tempReturn




#if __name__ =='__main__':
    #runServiceLoader('D:\\26CrazyRunFastServer','疯狂跑得快初级场12611')
    #print(isOpen(55155))
    #print(startCommand_check(' start  12211 ', ['疯狂斗地主中级场12221.xml', '疯狂斗地主初级场第1场12211.xml', '疯狂斗地主初级场第2场12212.xml', '疯狂斗地主新手场第1场12201.xml', '疯狂斗地主新手场第2场12202.xml', '疯狂斗地主新手场第3场12203.xml']))
    
    #print(getDirINFOstr(path))
    