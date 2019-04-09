#-*- coding:utf-8 -*-
#!/usr/bin/python3
import os, sys, getopt
def Create_direct():
    path = os.getcwd()
    print ("存放路径为%s" % (path))
    if len(sys.argv) == 1:
        Enter = input("Please enter the name of the directory you want to create:").split()
        for i in Enter:
            new_path = os.path.join(path, i)
            if os.path.isdir(new_path) == False:
                os.mkdir(new_path)
                print("%s创建完成" % (new_path))
            elif os.path.isdir(new_path) == True:
                print ("%s已经存在" % (new_path))
    else:
        for i in sys.argv[2:]:
            new_path = os.path.join(path, i)
            if os.path.isdir(new_path) == False:
                os.mkdir(new_path)
                print ("%s创建完成" % (new_path))
            elif os.path.isdir(new_path) == True:
                print ("%s已经存在" % (new_path))
def Create_file():
    path = os.getcwd()
    print ("存放路径为%s" % (path))
    if len(sys.argv) == 1:
        Enter = input("Please enter the name of the directory you want to create:").split()
        for i in Enter:
            new_path = os.path.join(path, i)
            if os.path.isfile(new_path) == False:
                open(new_path,'w')
                print ("%s创建完成" % (new_path))
            elif os.path.isfile(new_path) == True:
                print ("%s已经存在" % (new_path))
    else:
        for i in sys.argv[2:]:
            new_path = os.path.join(path, i)
            if os.path.isfile(new_path) == False:
                open(new_path,'w')
                print ("%s创建完成" % (new_path))
            elif os.path.isfile(new_path) == True:
                print ("%s已经存在" % (new_path))

if len(sys.argv) != 1:
    if sys.argv[1] in "D,d":
        Create_direct()
        sys.exit()	
    elif sys.argv[1] in "F,f":
        Create_file()
        sys.exit()

DF = input("文件F,目录D:")
if DF in "[D,d]":
    Create_direct()
elif DF in "[F,f]":
    Create_file()
