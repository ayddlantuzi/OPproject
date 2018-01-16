# -*- coding: utf-8 -*-
import os

backpath = 'D:\\ini'

file = os.listdir(backpath)

for i in file:
	print(i)

print('-------------')
print(file.pop(-1))

