#coding:gbk

import paramiko,configparser

#获取单个服务器连接信息
def GetServerConnectionInformation(address) :
    global IP,Port,User,Passwd,Backup_Path,Project_Path,Home_Path,MyPass,Source_Path,conf
    conf = configparser.ConfigParser()
    conf.read("./conf/wfl.conf")
    Source_Path = conf.get("source",'source_path')
    IP = conf.get(address, 'ip')
    Port = int(conf.get(address, 'port'))
    User = conf.get(address,'user')
    Passwd = conf.get(address, 'passwd')
    Backup_Path = conf.get(address,'backup_path')
    Project_Path = conf.get(address,'project_path')
    Home_Path = conf.get(address,'home')
    MyPass = conf.get(address,'mysql_passwd')
    print (IP)

def GetAllServerConnectionInformation() :
    global IP,Port,User,Passwd,Backup_Path,Project_Path,Home_Path,MyPass,Source_Path,conf,sections
    conf = configparser.ConfigParser()
    conf.read("./conf/wfl.conf")
    sections = conf.sections()
    return sections

#连接到服务器
def ConnectToTheServer(*params) :
    global outmsg
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(IP, Port, User, Passwd)
    for i in params:
        stdin, stdout, stderr = ssh.exec_command(i)
        outmsg, errmsg = stdout.read(), stderr.read()
        if outmsg != "":
            print(outmsg.decode().strip())
        # if errmsg != "":
        #     print(errmsg)
    ssh.close()


