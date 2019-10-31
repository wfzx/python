#coding:gbk

import sys
import configparser

def readConf(groupName):
    confName = "conf/auth.conf"
    conf = configparser.RawConfigParser()
    conf.read(confName)
    if groupName in "list":
        print(conf.sections())
    else:
        print (conf.items(groupName))

if __name__ == "__main__":
    GetName = sys.argv[1]
    readConf(GetName)