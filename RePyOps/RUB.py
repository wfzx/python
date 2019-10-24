#coding: UTF-8

import os
import sys
import logs
import paramiko
import configparser

class ConntionInfo(object):
    def __init__(self,GroupName=None,PackageName=None):
        ConfName = "conf/RUB.conf"
        conf = configparser.ConfigParser()
        conf.read(ConfName)
        self.IP = conf.get(GroupName,"ip")
        self.User = conf.get(GroupName,"user")
        self.Passwd = conf.get(GroupName,"password")
        self.Port = int(conf.get(GroupName,"port"))
        self.SourcePackDir = conf.get("SourcePackagesDir","Dir")
        self.TargetPackDir = conf.get(GroupName,"Dir")
        self.BackupDir = conf.get(GroupName,"backup")
        self.PackageName = PackageName
        self.SourcePackage = "%s\%s" % (self.SourcePackDir, self.PackageName)
        self.TargetPackage = "%s/%s" % (self.TargetPackDir, self.PackageName)
        self.BackupPackage = "%s/%s" % (self.BackupDir, self.PackageName)

    def UploadFile(self):
        scp = paramiko.Transport(self.IP, self.Port)
        scp.connect(username=self.User, password=self.Passwd)
        sftp = paramiko.SFTPClient.from_transport(scp)
        sftp.put(self.SourcePackage,self.TargetPackage)
        scp.close()
        logs.log('UploadFile: SourcePackage:%s TargetPackage:%s' % (self.SourcePackage,self.TargetPackage))

    def ConntionSSH(self,cmd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.IP,self.Port, self.User, self.Passwd)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        outmsg, errmsg = stdout.read(), stderr.read()
        if errmsg != "":
            print (errmsg.decode().strip())
        ssh.close()
        logs.log('ConntionSSH: ip:%s  port:%s user:%s  passwd:%s cmd:%s' % (self.IP,self.Port,self.User,self.Passwd,cmd))
        return outmsg.decode().strip()

    def BackUP(self):
        self.CheckFile()
        cmd = "/bin/cp -f %s %s" % (self.TargetPackage,self.BackupPackage)
        self.ConntionSSH(cmd)

    def CheckFile(self):
        CheckSourcePackage = os.path.isfile(self.SourcePackage)
        if CheckSourcePackage:
            pass
        else:
            print ("File Not Exist %s" % (self.SourcePackage))
            logs.log("CheckFile: File Not Exist %s" % (self.SourcePackage))
            sys.exit(1)
        CheckRemotePackDir = "if [ ! -d %s ];then mkdir -p %s;fi && if [ ! -d %s ];then mkdir -p %s;fi" % (self.TargetPackDir,self.TargetPackDir,self.BackupDir,self.BackupDir)
        self.ConntionSSH(CheckRemotePackDir)

    def RestartService(self):
        Status = "restart"
        cmd1 = "supervisorctl status %s" % (self.PackageName)
        ExecBeforeCheckStatus = self.ConntionSSH(cmd1)
        for t in ExecBeforeCheckStatus:
            if "STOPPED" in t:
                Status = "start"
                logs.log("StopStartService: Before Exec %s Status STOPPED" % (self.PackageName))
        cmd = "supervisorctl %s %s" % (Status,self.PackageName)
        CheckStatus = self.ConntionSSH(cmd)
        for i in CheckStatus:
            if "ERROR" in i:
                print ("%s %s Failes!!!" % (self.PackageName,Status))
                logs.log("StopStartService: %s %s Failes!" % (self.PackageName,Status))
                sys.exit(1)
            elif 'RUNNING' in i:
                print ("%s %s Successful!!!" % (self.PackageName,Status))
                logs.log("StopStartService: %s %s Successful!" % (self.PackageName, Status))


    def main(self):
        self.BackUP()
        self.UploadFile()
        self.RestartService()

if __name__ == "__main__":
    GroupName = sys.argv[1]
    PackageName = sys.argv[2]
    for x in GroupName.split(":"):
        Release = ConntionInfo(GroupName,PackageName)
        Release.main()