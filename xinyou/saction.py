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
import shutil

gamedir = ''
# 默认桌面目录
desktop_dir = 'D:\\Desktop\\'

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
        msg = ('%s@%s 匹配不到游戏目录，请重新输入---！' % ('print', str))
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
        return msg,False


    if cmdList[0] == 'start':
        if ',' in cmdList[1]:
            room = cmdList[1].split(',')
            msg = runServiceLoader(gamedir+'\\'+currentGame[0],room)
        else:
            msg = runServiceLoader(gamedir+'\\'+currentGame[0],cmdList[1])

    elif cmdList[0] == 'show':
        msg = show_cmd_server(gamedir,currentGame[0],cmdList[1])

    elif cmdList[0] == 'get':
        # get ini 下载当前游戏 目录下的所有ini到桌面
        # get *** 下载明确的文件名
        # 1、检查目录中的  是否存在ini文件，或者具体文件名称是否存在
        # 2、
        msg = get_filter_File(gamedir,currentGame[0],cmdList[1])

    elif cmdList[0] == 'put':
        msg = put_check_server(gamedir,currentGame[0],cmdList[1])

        return msg

    elif cmdList[0] == 'update':
        # update exe 升级servicesLoader
        # update dll 升级游戏dll
        # 升级前 建立备份目录  并备份被升级的文件
        msg = update_cmd_server(gamedir,currentGame[0],cmdList[1])

    elif cmdList[0] =='back':
        msg = back_cmd_server(gamedir,currentGame[0],cmdList[1])

    return msg


def back_cmd_server(gamedir,currentGame,suffixal):
    '''
    还原备份文件，还原最近一次备份
    :param gamedir:
    :param currentGame:
    :param suffixal: ini  dll  exe三种
    :return:
    '''
    msg = ''
    back_source_dir = gamedir+currentGame+'\\backup\\'+suffixal
    print(back_source_dir)

    if os.path.exists(back_source_dir):
        file = os.listdir(back_source_dir)
        if len(file) == 0:
            msg = '没有'+suffixal+' 的备份文件！'
        else:
            backdir = back_source_dir+'\\'+file.pop(-1)
            msg = copyAllFileto(backdir,gamedir+currentGame)
    else:
        msg = '没有'+suffixal+' 的备份文件！'

    msg = 'print@'+msg
    return msg


def copyAllFileto(sourceDir,targetDir):
    '''
    将目录下所有的还原到 游戏目录，并且删除目录
    :param sourceDir:备份目录，游戏目录
    :param targetDir:
    :return:
    '''
    msgList = []
    maxlen = 0
    backfile = os.listdir(sourceDir)
    if len(backfile) == 0:
        msg = sourceDir + '目录中没有文件,目录被删除！'
        shutil.rmtree(sourceDir)
    else:
        for file in backfile:
            try:
                shutil.copy(sourceDir+'\\'+file,targetDir)
                os.remove(sourceDir+'\\'+file)
                width = len(file)
                if width>maxlen:
                    maxlen = width
                msgList.append([file,'还原成功!'])
            except Exception as e:
                print(e)
                msgList.append([file,e])
        if len(os.listdir(sourceDir)) == 0:
            shutil.rmtree(sourceDir)
        msg = format_printMSG(msgList,1,maxlen)
    return msg

def update_cmd_server(gamedir,currentGame,file_str):
    '''
    更新 exe   dll  命令
    :param gamedir:
    :param currentGame:
    :param file_str:
    :return:
    '''
    source_target_list = []
    rev_update_cmd = file_str.split('?')
    source_dir = rev_update_cmd.pop()
    len_rev_cmd = len(rev_update_cmd)
    msg = ''
    if  len_rev_cmd == 1:
        # 只有一个文件  备份并更新dll
        msg = backup_file(gamedir,currentGame,rev_update_cmd,'dll')
    elif len_rev_cmd > 0:
        # 多个文件 备份并更新ServiceLoader
        msg = backup_file(gamedir, currentGame, rev_update_cmd, 'exe')

    # 传输 源目录 目标目录
    for file in rev_update_cmd:
        targetClient = '\\'+currentGame+'\\'+file
        sourceServer = source_dir + file
        source_target_list.append([sourceServer,targetClient])

    msg += '+update@' + transfer_list_2_str(source_target_list)
    return msg

def show_cmd_server(gamedir,currentGame,info):
    '''
    显示游戏目录  文件，房间列表 等等
    :param gamedir: 游戏根目录
    :param currentGame: 游戏目录
    :param info: 显示的内容  room 房间(包括是否启用）   file  文件(包括修改时间)
    :return: 返回打印的消息
    '''
    msg = ''
    msgList = []
    maxlen = 0
    if info == 'room':
        path = gamedir+currentGame+'\\run'
        if os.path.exists(path):
            run_folder_files = os.listdir(path)
            xmlfile = []
            for i in run_folder_files:
                if i[-4:] =='.xml':
                    xmlfile.append(i)
            if len(xmlfile)>0:
                for i in xmlfile:
                    n='未启用！'
                    whidth = chinese(i,2)
                    if whidth>maxlen:
                        maxlen=whidth

                    if portISopen(getPortFromXML(i)):
                        # 端口状态，端口被占用 n='1'
                        n='已启用！'
                    msgList.append([i,n])
                msg = format_printMSG(msgList,1,maxlen)
            else:
                msg = '游戏目录 ' + path + '中没有房间配置文件！'
        else:
            msg = '目录 ' + path + '不存在！'
    elif info == 'file':
        path = gamedir+currentGame
        if os.path.exists(path):
            game_folder_files = os.listdir(path)
        if len(game_folder_files)>0:
            for file in game_folder_files:
                whidth = chinese(file,2)
                if whidth > maxlen:
                    maxlen = whidth
                msgList.append([file,time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(os.path.getmtime(path+'\\'+file)))])
                # msg += file + '    ' +time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(os.path.getmtime(path+'\\'+file))) +'\n'
            msg = format_printMSG(msgList,1,maxlen)
        else:
            msg = '游戏目录 ' + path + '中没有文件！'
    else:
        msg = '命令不正确,参考：\nshow room 显示房间\nshow file 显示文件'
    return 'print@'+msg



def put_check_server(gamedir,currentGame,filelist_str):
    '''
    put  上传用，判断目录是否存在，上传做备份
    :param gamedir:
    :param currentGame:
    :param get_fuzzy:
    :return:  返回msg  msg1     msg print备份消息     msg1 put消息
    '''
    global  desktop_dir
    msg=''
    print('gamedir:',end='')
    print(gamedir)
    print('currentGame:',end='')
    print(currentGame)
    gamefile = os.listdir(gamedir+'\\'+currentGame)

    filelist = filelist_str.split('?')
    source_target_list = []
    backupfile = []

    for file in filelist:
        if file in gamefile:
            backupfile.append(file)

    if len(backupfile) >0:
        msg = backup_file(gamedir,currentGame,backupfile,backupfile[0][-3:])
        # print@......+put@..... client 接收后   split'+'
        msg += '+'


    # 传输 源目录 目标目录
    for file in filelist:
        targetClient ='\\'+currentGame + '\\' + file
        sourceServer = desktop_dir+currentGame+'\\'+file
        source_target_list.append([sourceServer,targetClient])

    msg += 'put@'+transfer_list_2_str(source_target_list)

    return msg




def backup_file(gamedir,currentGame,fileList,folder):
    '''
    升级文件  ini 时   备份文件用
    :param gamedir:
    :param currentGame:
    :param fileList:
    :param folder:  备份根目录backup的下一级目录  ini  dll  serviceLoader
    :return:
    '''
    # 游戏目录备份 根目录   例E:\Game\24StandLand3renServer\backup
    backup_dir = gamedir+'\\'+currentGame+'\\backup'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # 游戏目录  备份目录例E:\Game\24StandLand3renServer\backup\ini
    backup_folder = backup_dir+'\\'+folder
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    # 根据当前日期时间 创建备份子目录
    newfolder = time.strftime('%Y-%m-%d %H %M %S',time.localtime(time.time()))
    backup_path = backup_folder + '\\'+newfolder+'\\'
    os.makedirs(backup_path)

    if folder in ['ini','dll','exe']:
        msglist = []
        maxlen = 0
        for file in fileList:
            file_length = len(file)
            shutil.copy(gamedir+'\\'+currentGame+'\\'+file,backup_path)
            if file_length > maxlen:
                maxlen = file_length
            msglist.append(['被覆盖文件',file,' 已备份！'])

    else:
        msg='print@saction.py  backup_file方法错误，请检查代码！'

    msg = 'print@'+format_printMSG(msglist,2,maxlen)
    return msg



def get_filter_File(gamedir,currentGame,get_fuzzy):
    '''                                      固定桌面目录
    get ini 用，获取游戏目录下 特定后缀 文件
    :param gamedir: 游戏总目录
    :param currentGame: 游戏下  单个游戏目录
    :param get: 文件后缀 'ini' 返回所有ini文件   其他****   返回****文件
    :return:
    '''

    global desktop_dir

    msg = ''
    filelist = []
    gamefile = os.listdir(gamedir+'\\'+currentGame)
    if get_fuzzy == 'ini':
        for file in gamefile:
            if file[-3:] == 'ini':
                sourceServer ='\\'+currentGame + '\\' + file
                targetClient = desktop_dir+currentGame+'\\'+file
                filelist.append([sourceServer,targetClient])
    else:
        if get_fuzzy in gamefile:
            sourceServer = '\\' + currentGame + '\\' + get_fuzzy
            targetClient = desktop_dir + currentGame + '\\' + get_fuzzy
            filelist.append([sourceServer, targetClient])
        else:
            msg = ('%s@%s' % ('print', get_fuzzy+'在游戏目录'+currentGame+'  中未找到！'))
            return msg
    msg =  ('%s@%s' % ('get',transfer_list_2_str(filelist)))
    return msg

def transfer_list_2_str(filelist):
    msg = ''
    if len(filelist) != 0:
        for list in filelist:

            for i in list:
                msg += i + '#'
            msg = msg[:-1] + '?'
    return msg[:-1]


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

    return msg


def format_printMSG(plist,align_column_int,align_column_maxlen):
    '''
    对返回的 print消息 格式化列
    :param plist:打印消息的list
    :param align_column_int:  要对齐的列
    :return: 格式化后的输出消息

    [['第一列', '第二列231', '三'], ['第一列', '第二列2啊啊啊啊31', '三'], ['第一列', '第二列2', '三']]   2
                    ↓↓  ↓↓  ↓↓
    第一列         第二列231                三
    第一列         第二列2啊啊啊啊31         三
    第一列         第二列2                  三
    '''
    # 定义format  正则表达式
    def_format = ''
    length = len(plist[0])
    n=0
    listnum = 0
    while length > 0:
        def_format += '{'+str(n)+':'
        if align_column_int-1 == n:
            n += 1
            def_format +='{'+str(n)+'}}'
        else:
            def_format += str(chinese(plist[0][listnum],2)+4)+'}'
        n += 1
        listnum += 1
        length -= 1

    msgStr = ''
    for i in plist:
        i.insert(align_column_int,align_column_maxlen+8-chinese(i[align_column_int-1]))
        # print(i)
        msgStr += def_format.format(*i)+'\n'

    return msgStr[:-1]



def chinese(data,mode=1):
    '''
    mode=1 默认返回str 中文字符个数，mode=2返回字符串宽度   中文占2，其他占1
    :param data:str
    :param mode:
    :return:返回字符串宽度
    '''
    count = 0
    if mode == 1:

        for s in data:
            if ord(s) > 127:
                count += 1
    elif mode == 2:
        for s in data:
            if ord(s) >127:
                count += 2
            else:
                count += 1
    return count