#遍历目录下的所有目录和文件
def getDir(path):
    for parent,dirnames,filenames in os.walk(path):
        for dirname in dirnames:  
            print("parent folder is:" + parent)  
            print("dirname is:" + dirname)  
        for filename in filenames:    
            print("parent folder is:" + parent)  
            print("filename with full path:"+ os.path.join(parent,filename))


print('dfsafs')