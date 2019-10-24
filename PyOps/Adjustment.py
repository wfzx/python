#coding:gbk

import paramiko,sys,configparser,os

class ConntionInfo:
    def __init__(self,GroupName=None):
        global IP,Port,User,Passwd,Backup_Path,Project_Path,Home_Path,MyPass,Source_Path
        ConfName = "%sconf/sdgroup.conf" % (os.path.abspath(sys.argv[0]).split(os.path.split(sys.argv[0])[1])[0])
        conf = configparser.ConfigParser()
        conf.read(ConfName)
        self.Source_Path = conf.get("source", 'source_path')
        self.IP = conf.get(GroupName, 'ip')
        self.Port = int(conf.get(GroupName, 'port'))
        self.User = conf.get(GroupName, 'user')
        self.Passwd = conf.get(GroupName, 'passwd')
        self.Backup_Path = conf.get(GroupName, 'backup_path')
        self.Project_Path = conf.get(GroupName, 'project_path')
        self.Home_Path = conf.get(GroupName, 'home')
        self.MyPass = conf.get(GroupName, 'mysql_passwd')
        Source_Path = conf.get("source", 'source_path')
        IP = conf.get(GroupName, 'ip')
        Port = int(conf.get(GroupName, 'port'))
        User = conf.get(GroupName, 'user')
        Passwd = conf.get(GroupName, 'passwd')
        Backup_Path = conf.get(GroupName, 'backup_path')
        Project_Path = conf.get(GroupName, 'project_path')
        Home_Path = conf.get(GroupName, 'home')
        MyPass = conf.get(GroupName, 'mysql_passwd')

    # 调用windows弹窗
    def Message_Box(self,title, msg, status):
        from tkinter import messagebox
        if status == "info":
            messagebox.showinfo(title, msg)
        elif status == "warning":
            messagebox.showwarning(title, msg)
        elif status == "error":
            messagebox.showerror(title, msg)

    def ConntionSSH(*params):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(IP, Port, User, Passwd)
        for i in params:
            stdin, stdout, stderr = ssh.exec_command(str(i))
            outmsg, errmsg = stdout.read(), stderr.read()
            if outmsg != "":
                print(outmsg.decode().strip())
            # if errmsg != "":
            #     print(errmsg.decode().strip())
        ssh.close()

    # 写入log
    def LogWrite(self,content):
        LogName = "%slogs/PyOps.log" % (os.path.abspath(sys.argv[0]).split(os.path.split(sys.argv[0])[1])[0])
        try:
            logging = open(LogName, "a")
        except FileNotFoundError:
            os.mkdir("%slogs/") % (os.path.abspath(sys.argv[0]).split(__file__)[0])
            logging = open(LogName, "a")
        logging.write(content)
        logging.close()