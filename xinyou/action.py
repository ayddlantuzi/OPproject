#temp = 'a'
#while temp!='exit':
    #temp = input('>:')
    #print(temp)
    
    
import os
import socket
import os.path
import configparser
import codecs
import re

test = '1'


#cd /d %EDIR%
#for /f %%i in ('dir "%EDIR%\run\*.xml" /s /b') do (start %EDIR%\ServiceLoader.exe "auto" "%%i" && ping 127.0.0.1 /n 3 >nul)
#'

def runServiceLoader(path,xml):
    #print(os.getcwd())
    #path = 'D:\\26CrazyRunFastSe rver'
    #os.chdir(path)
    #print(os.getcwd())
    #os.system('1start.bat')
    
    
    #a = os.popen("for /f %i in (\'dir \""+path+"\\run\\"+xml+".xml\" /s /b\') do (start "+path+"\\ServiceLoader.exe \"auto\" \"%i\" && ping 127.0.0.1 /n 3 >nul)")
    #print(a.read())    
    
    #path = 'D:\\26CrazyRunFastServer'
    #xml = '疯狂跑得快初级场12611'
    #xml=  '*'
    
    os.system("for /f %i in (\'dir \""+path+"\\run\\"+xml+".xml\" /s /b\') do (start "+path+"\\ServiceLoader.exe \"auto\" \"%i\" && ping 127.0.0.1 /n 3 >nul)")

    #os.system("for /f %i in (\'dir \""+path+"\\run\\*.xml\" /s /b\') do (start "+path+"\\ServiceLoader.exe \"auto\" \"%i\" && ping 127.0.0.1 /n 3 >nul)")
    
    #os.system('for /f %i in (\'dir "D:\\26CrazyRunFastServer\\run\\*.xml" /s /b\') do (start D:\\26CrazyRunFastServer\\ServiceLoader.exe "auto" "%i" && ping 127.0.0.1 /n 3 >nul)')
    
    
#修改房间配置
def editXML(path,line,info):
    pass

#修改配置文件
def editINI(path,line,info):
    pass

#升级文件
def update():
    pass

#将cmd启动脚本返回的str 过滤 简约显示，内容：*****.xml  启动成功
def formatMessage(msg):
    a = msg.find('run')
    b = msg.find('.xml')+4
    c = msg[a:b].split('\\\\')
    return c[1]+'     启动成功 !'





#判断端口是否占用  True占用   False未占用
def portISopen(port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(0.01)
    try:
        ADDR=('127.0.0.1',port)
        s.connect(ADDR)
        s.shutdown(2)
        return True
    except Exception as e:
        print(e)
        return False
    

#遍历目录下的所有目录和文件  f
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

        

#命令合法性判断
def command_check(command,currentGame,table):
    #命令的个数  判断是否输入kindID  还是 start ***
    secondList = table[1]
    commandList = command.split()
    num = len(commandList)
    if num == 1:
        command = command.strip()
        if command.isdigit():
            gameName = inputKindID_check(command,secondList)
            if  gameName:
                return [True,gameName]
            else:
                return[False,'KindID 不在列表中！']
        else:
            return [False,'命令不正确，请核对KindID！']
        
    elif num >=2:
        if currentGame == '':
            return [False,'请先输入游戏KindID 再操作！']
        else:
            return inputCommand_check(command,currentGame,table)
    else:
        return [False,'语法错误！']



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
    