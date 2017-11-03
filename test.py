# -*- coding: utf-8 -*-
import subprocess
import tempfile
import sys
from xinyou import action
import os

out_temp = tempfile.SpooledTemporaryFile(max_size=10*1000)
fileno = out_temp.fileno()
# xml = '疯狂跑得快初级场12611'
# path = 'd:\\game\\26CrazyRunFastServer'
# a= subprocess.run("for /f %i in (\'dir \""+path+"\\run\\"+xml+".xml\" /s /b\') do (start "+path+"\\ServiceLoader.exe \"auto\" \"%i\" && ping 127.0.0.1 /n 3 >nul)",stdout=fileno,shell=True)
a = subprocess.run('ipconfig',stdout = fileno,shell=True)

# action.runServiceLoader(path,xml)
out_temp.seek(0)
lines = out_temp.readlines()
out_temp.close()
print('type lines:',end='')
print(type(lines))


s= ''
for i in lines:
	s += i.decode('gbk') + '\r\n'
print(s)

print(sys.stdin.encoding)
print(sys.stdout.encoding)