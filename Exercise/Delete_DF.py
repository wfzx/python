#-*- coding:utf-8 -*-
#!/usr/bin/python3
import os, sys
def Delete_direct():
    path = os.getcwd()
    print ("删除操作将在%s执行" % (path))
    if len(sys.argv) == 1:
        Enter = input("Please enter the directory you want to delete:").split()
        for i in Enter:
            new_path = os.path.join(path,i)
            if os.path.isdir(new_path) == True:
                os.rmdir(new_path)
                print ("%s已经删除" % (new_path))
            elif os.path.isdir(new_path) == False:
                print ("%s不存在" % (new_path))
    else:
        for i in sys.argv[2:]:
            new_path = os.path.join(path,i)
            if os.path.isdir(new_path) == True:
                os.rmdir(new_path)
                print ("%s已经删除" % (new_path))
            elif os.path.isdir(new_path) == False:
                print ("%s不存在" % (new_path))

def Delete_file():
    path = os.getcwd()
    print ("删除操作将在%s执行" % (path))
    if len(sys.argv) == 1:
        Enter = input("Please enter the file you want to delete:").split()
        for i in Enter:
            new_path = os.path.join(path,i)
            if os.path.isfile(new_path) == True:
                os.remove(new_path)
                print ("%s已经删除" % (new_path))
            elif os.path.isfile(new_path) == False:
                print ("%s不存在" % (new_path))
    else:
        for i in sys.argv[2:]:
            new_path = os.path.join(path,i)
            if os.path.isfile(new_path) == True:
                os.remove(new_path)
                print ("%s已经删除" % (new_path))
            elif os.path.isfile(new_path) == False:
                print ("%s不存在" % (new_path))

def Delete_All():
    path = os.getcwd()
    print ("删除操作将在%s执行" % (path))
    filename_list = os.listdir(path)
    for i in range(len(filename_list)):
        new_path = os.path.join(path,filename_list[i])
        if os.path.isdir(new_path) == True:
            print (new_path)
            os.rmdir(new_path)
        elif os.path.isfile(new_path) == True:
            print (new_path)
            os.remove(new_path)

if len(sys.argv) != 1:
    if sys.argv[1] in "D,d":
        Delete_direct()
        sys.exit()
    elif sys.argv[1] in "F,f":
        Delete_file()
        sys.exit()
    elif sys.argv[1] in "A,a":
        Delete_All()
        sys.exit()

DF = input("文件F,目录D,所有A:")
if DF == "D":
    Delete_direct()
elif DF == "F":
    Delete_file()
elif DF == "A":
    Delete_All()
