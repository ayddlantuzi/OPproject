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

def help(cmd=''):
    '''
    帮助命令
    :param cmd:   cmd不是action动作的时候 默认help帮助提示
    :return:
    '''
    actionCMD = ['start','update','get','put','show','back','compare']
    if cmd=='' or cmd not in actionCMD:
        print('在选择游戏名称后  使用多命令进行管理\n\n'
              '单命令:\n'
              '输入的字符串 会优先匹配游戏目录，游戏目录使用了模糊匹配 \n'
              '如26CrazyRunFastServer 可以输入26  或者fast  当输入匹配多个游戏时，按顺序优先进入！\n'
              'cls 清楚界面消息\n'
              'exit 退出\n\n'
              '多命令:\n'
              'start   命令  启用游戏房间 支持单个、多个、所有\n'
              'update  命令  从本地更新游戏文件 更新游戏dll 或者ServiceLoader\n'
              'back    命令  使用update 或者 put  被覆盖的文件会自动备份，back可以回退到上一个版本的文件\n'
              'get     命令  从游戏目录下载指定文件 \n'
              'put     命令  从本地上传文件到游戏目录\n'
              'show    命令  显示当前游戏的 房间\n'
              'compare 命令  比对 游戏目录  和 SVN 中的文件日期\n'
              '以上 命令使用help+动作命令  获得更详细的帮助！例如 help start')
    elif cmd == 'start':
        print('start 命令 可以单个、多个、全部 启用游戏房间\n'
              '进入游戏目录有 使用show room 可以查看游戏的房间配置文件\n'
        
              '例：\n'
              '26CrazyRunFastServer:>show room\n'
              '手机疯狂跑得快初级场12610.xml        =====未启用！\n'  
              '疯狂跑得快中级场12621.xml            =====未启用！\n'        
              '疯狂跑得快初级场12611.xml            =====未启用！\n'        
              '疯狂跑得快新手场12601.xml            =====未启用！\n'        
              '疯狂跑得快顶级场12631.xml            =====未启用！\n'
        
              '命令使用方法 start 12601     start 12601,12611    start all\n'
              '注意事项：游戏房间配置文件 命名规则    *******12601.xml  文件名最后5位为房间端口号！\n'
              '         端口号          命名规则    100+kindid**  最后两位编号\n'
              '         例： 跑得快  kindID 26     端口号应为126**  12601新手场  12611初级场  12621中级场')

    elif cmd == 'update':
        print('update 命令 用于更新游戏文件,文件从本地svn目录自动获取\n'
              'update dll  svn游戏单款dll 更新到游戏目录  旧的单款dll 文件会备份到 游戏目录back\dll中，使用back dll还原本次操作\n'
              'update exe  svn目录ServiceLoader文件  更新到游戏目录  旧的文件会备份到  游戏目录back\exe中，使用back exe还原本次操作'
              )

    elif cmd == 'back':
        print('back 命令用于 还原最近一次备份的文件\n'
              'back ini 还原最近一次备份的ini文件\n'
              'back exe 还原最近一次更新的ServiceLoader文件\n'
              'back dll 还原最近一次更新的单款dll')
    elif cmd == 'get':
        print('get 命令用于获取游戏中的文件,文件下载到本地桌面 以游戏名称命名的文件夹\n'
              '例：当前管理游戏 22CrazyLand3renServer'
              'get GameConfig.ini 将文件下载覆盖到 桌面22CrazyLand3renServer目录\n'
              'get ini 将所有ini文件下载覆盖到 桌面22CrazyLand3renServer目录'
              )
    elif cmd == 'put':
        print('put 命令用于上传桌面游戏目录中的文件到 游戏服务器'
              '例：当前管理游戏 22CrazyLand3renServer\n'
              'put GameConfig.ini 将本地桌面目录22CrazyLand3renServer的 GameConfig.ini 文件上传到游戏目录\n'
              'put ini 将所有将本地桌面目录22CrazyLand3renServer的 所有ini文件上传到游戏目录\n'
              '注意事项：被上传的文件会保留最后一次修改日期'
              )
    elif cmd == 'show':
        print('show 命令用于显示当前管理游戏的 房间或文件\n'
              '例：当前管理游戏 22CrazyLand3renServer\n'
              'show room 显示该游戏目录run文件夹下的 房间配置文件 和端口开启情况\n'
              'show file 显示该游戏目录下的所有文件信息')
    elif cmd == 'compare':
        print('compare 命令用于对比游戏目录下 ServiceLoader 和dll的时间对比\n'
              'compare dll对比游戏目录下的 单款dll 和SVN 单款dll日期\n'
              'compare exe对比游戏目录下的 ServiceLoader 和SVN 的ServiceLoader日期')

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
        if cmdList[0].lower() =='id':
            printGameDir(gameDir)
            return False
        elif cmdList[0].lower() =='help':
            help()
            return False
        else:
            return True

    if len(cmdList)>2:
        print('错误!!!  命令数超过2个')
        return False

    if len(cmdList)==2:
        if cmdList[0] =='help':
            help(cmdList[1])
            return False

        if currentGame == '':
            print('请先选择游戏目录:')
            printGameDir(gameDir)
            return False

        if not cmdList[0] in cmdaction:
            print('错误!!!   '+ cmdList[0] +'  命令动作不存在')
            return False
        elif cmdList[0] == 'help':
            help(cmdList[1])
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
        elif cmdList[0] == 'compare':
            if not cmdList[1] in ['exe','dll']:
                print('compare 命令错误 help compare 查询命令的使用方法')
                return False
    return True

def compare_cmd_client(currentGame,cmd_1):
    '''
    将服务器返回的  文件 修改日期，和SVN的 修改日期整合
    :param currentGame:
    :param cmd_1:
    :return:
    '''
    global svnServiceLoader_dir
    global dlls_dir

    maxlen = 0
    msg = ''
    compareFile = transfer_list_str_2_list(cmd_1)
    # print(compareFile)
    # 列表长度为1时候  游戏.dll   >1的时候  serviceLoader.exe   .. .dll
    num = len(compareFile)
    if num == 1:
        # 去除name 开头2-3位数字
        dllname = re.sub('^\\d{2,3}','',currentGame)+'.dll'
        dllpath = dlls_dir+dllname
        if os.path.exists(dllpath):
            maxlen = len(dllname)
            compareFile[0].append(time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(os.path.getmtime(dllpath))))
        else:
            compareFile[0].append('')
    else:
        # 统计svn目录下的 dll 和exe文件
        svnFile = []
        for file in os.listdir(svnServiceLoader_dir):
            if file[-4:] == '.dll':
                svnFile.append(file)
        svnFile.append('ServiceLoader.exe')

        for x in range(num):
            length = len(compareFile[x][0])
            if length > maxlen:
                maxlen = length


            status = False
            removeObj = ''
            for file in svnFile:
                if compareFile[x][0] == file:
                    compareFile[x].append(time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(os.path.getmtime(svnServiceLoader_dir+file))))
                    status = True
                    removeObj = file
                    break
            if status:
                svnFile.remove(removeObj)
            else:
                compareFile[x].append('')

        if len(svnFile) >0:
            for file in svnFile:
                length = len(file)
                if length > maxlen:
                    maxlen = length
                compareFile.append([file,'',time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(os.path.getmtime(svnServiceLoader_dir+file)))])

    compareFile.insert(0,['File','Using','SVN'])

    msg = saction.format_printMSG(compareFile,1,maxlen)
    print(msg)




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
            # print(file)
            if len(file) == 0:
                print(svnServiceLoader_dir+' 下没有更新文件！')
            else:
                for f in file:
                    if not os.path.isdir(svnServiceLoader_dir+f):
                        flist = os.path.splitext(f)
                        if flist[1] == '.dll':
                            exe_file_str += f+'?'
                exe_file_str += 'ServiceLoader.exe?'+svnServiceLoader_dir
                # print(exe_file_str)
                return ['update',exe_file_str]
        else:
            print('本地目录 '+svnServiceLoader_dir+' 不存在！')
    elif cmd_1 == 'dll':
        dll_name = re.sub('^\\d{2,3}','',currentGame)+'.dll'
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
        status = True
        for file in gamefile:
            if get_fuzzy.lower() == file.lower():
                putfile_str = file + '?'
                status = False
                break

        if status:
            print('桌面文件夹 ' + currentGame + ' 中没有 ' + get_fuzzy + ' 文件！')
            return False

    return ['put', putfile_str[:-1]]

        # if get_fuzzy in lower_gamefile:
        #     temp = True
        #     putfile_str = get_fuzzy +'?'
        # else:
        #     print('桌面文件夹 '+currentGame+' 中没有 '+get_fuzzy+' 文件！')
        #     return False

    # if temp:
    #     return ['put',putfile_str[:-1]]
    # else:
    #     print('桌面文件夹 '+currentGame+' 中没有 '+'ini 的文件！')
    #     return False



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
                    sftp.utime(filelist[1],(os.path.getatime(filelist[0]),os.path.getmtime(filelist[0])))
                    msgList.append(['文件',filename,'上传成功！'])
                    # print('文件 '+filelist[0].split('\\')[-1]+' 上传成功！')
                elif mode == 'get':
                    sftp.get(filelist[0],filelist[1])
                    a = paramiko.sftp_attr.SFTPAttributes.from_stat(sftp.stat(filelist[0]))
                    os.utime(filelist[1],(a.st_atime,a.st_mtime))
                    msgList.append(['文件', filename, '成功下载到桌面目录！'])
                    # print('文件   '+filelist[0].split('\\')[-1]+'  成功下载到桌面目录!')
                elif mode == 'update':
                    sftp.put(filelist[0], filelist[1])
                    sftp.utime(filelist[1], (os.path.getatime(filelist[0]), os.path.getmtime(filelist[0])))
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