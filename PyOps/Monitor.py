#coding:gbk

import paramiko,configparser,sys,os

#获取单个服务器连接信息
def GetServerConnectionInformation(address) :
    global IP,Port,User,Passwd,Backup_Path,Project_Path,Home_Path,MyPass,Source_Path,conf
    conf = configparser.ConfigParser()
    ConfName = "%sconf/sdgroup.conf" % (os.path.abspath(sys.argv[0]).split(os.path.split(sys.argv[0])[1])[0])
    conf.read(ConfName)
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
    ConfName = "%sconf/sdgroup.conf" % (os.path.abspath(sys.argv[0]).split(os.path.split(sys.argv[0])[1])[0])
    conf.read(ConfName)
    sections = conf.sections()
    return sections

#连接到服务器
def ConnectToTheServer(*params) :
    global outmsg
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(IP, Port, User, Passwd)
    except paramiko.ssh_exception.AuthenticationException:
        print ("账号密码有误")
    for i in params:
        stdin, stdout, stderr = ssh.exec_command(i)
        outmsg, errmsg = stdout.read(), stderr.read()
        if outmsg != "":
            print(outmsg.decode().strip())
        if errmsg.decode().strip() != "":
            print("未安装插件")
    ssh.close()

if len(sys.argv) > 1:
    if sys.argv[1] == "all":
        AllServerGroupName = GetAllServerConnectionInformation()
        for i in range(1,len(AllServerGroupName)):
            try:
                GetServerConnectionInformation(AllServerGroupName[i])
            except EOFError:
                continue
            cmd = "python ~/python/agent.py"
            ConnectToTheServer(cmd)
    else:
        GetServerConnectionInformation(sys.argv[1])
        cmd = "python ~/python/agent.py"
        ConnectToTheServer(cmd)
else:
    print("Please pass the reference")
    sys.exit()