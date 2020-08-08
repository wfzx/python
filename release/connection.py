#coding:utf-8

import logs
import paramiko
import pymysql

class connectionHost(object):
    def __init__(self,Host,UserName,Password,Port):
        self.Host = Host
        self.UserName = UserName
        self.Password = Password
        self.Port = int(Port)

    def ssh(self,*args):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.Host, self.Port, self.UserName, self.Password)
        ProjectName = args[-1]
        for i in range(0,len(args) - 1):
            Cmd = args[i]
            logs.log("SSH执行命令: Host: %s Cmd: \n\"%s\"\n" % (self.Host,Cmd),ProjectName)
            stdin, stdout, stderr = ssh.exec_command(Cmd)
            out, err = stdout.read(), stderr.read()
            outmsg, errmsg = out.decode().strip(),err.decode().strip()
            if errmsg != "":
                if 'WARNING' in errmsg:
                    logs.log("SSH警告: WARNING: \n%s\n" % errmsg,ProjectName)
                    print("SSH警告: WARNING: \n%s\n" % errmsg)
                else:
                    logs.log("SSH报错: ERROR: \n%s\n" % errmsg,ProjectName)
                    print("SSH报错: ERROR: \n%s\n" % errmsg)
                    return 1
            if outmsg != "":
                if "请联系运维" in outmsg:
                    logs.log("SSH报错: ERROR: \n%s\n" % outmsg, ProjectName)
                    print("SSH报错: ERROR: \n%s\n" % outmsg)
                    return 1
                logs.log("SSH输出: OUTPUT: \n%s\n" % outmsg,ProjectName)
                print("SSH输出: OUTPUT: \n%s\n" % outmsg)
        ssh.close()

class connectionMysqlDB(object):
    def __init__(self,Env):
        if Env == 'prd':
            self.DBHost = "47.92.207.138"
        else:
            self.DBHost = "172.26.80.252"
            # self.DBHost = "47.92.207.138"
        self.DBUserName = "CRS"
        self.DBPassWord = "hgXzlEIe9AN4zuYJ"
        self.DBPort = int(3306)
        self.DBDBName = "CrsDevOps"

    def ConnDB(self,*args):
        self.data = {}
        ProjectName = args[-1]
        # 同时执行的参数不得是多条sql
        if len(args) > 2:
            return 1
        for i in range(0,len(args) - 1):
        # for i in range(0,len(args)):
            connDB = pymysql.connect(host=self.DBHost,user=self.DBUserName,passwd=self.DBPassWord,port=self.DBPort,db=self.DBDBName)
            cursor = connDB.cursor()
            logs.log("DB执行SQL: %s\n" % (args[i]), ProjectName)
            print("DB执行SQL: %s\n" % (args[i]))
            cursor.execute(args[i])
            connDB.commit()
            Out = cursor.fetchone()
            cursor.close()
            connDB.close()
            if "select" in args[i]:
                sqlNum = args[i].split(" ")[1]
                if "*" in sqlNum:
                  self.data = Out
                elif "," in sqlNum:
                    sqlNum = sqlNum.split(",")
                    for t in range(0,len(sqlNum)):
                        self.data[sqlNum[t]] = Out[t]
                else:
                    self.data[sqlNum] = Out[0]

    def CheckApi(self,Sql):
        connDB = pymysql.connect(host=self.DBHost, user=self.DBUserName, passwd=self.DBPassWord, port=self.DBPort,
                                     db=self.DBDBName)
        cursor = connDB.cursor()
        cursor.execute(Sql)
        connDB.commit()
        if 'select' in Sql:
            self.Out = cursor.fetchall()
        cursor.close()
        connDB.close()