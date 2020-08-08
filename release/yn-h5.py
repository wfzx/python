#conding:utf-8

import os
import sys
import logs
import time
import configparser
from connection import connectionHost

class projectInfo(object):
    def __init__(self,JJN=None,PN=None, Env=None):
        if Env in ['prd','grey']:
            ConfName = "/data/release/conf/prd"
            # ConfName = "conf/prd"
        elif Env == "dev":
            ConfName = "/data/release/conf/dev"
        else:
            ConfName = "/data/release/conf/test"
            # ConfName = "conf/test"
        conf = configparser.ConfigParser()
        conf.read(ConfName)
        self.ProjectName = PN
        self.JenkinsJobName = JJN
        self.Env = Env
        self.DATE = time.strftime('%Y%m%d%H%M%S')
        self.RootDir = conf.get("h5", "RootDir")
        self.BackupDir = conf.get("Env", "BackupDir")
        self.JenkinsWorkSpaceDir = conf.get("Env", "JenkinsDir")
        self.ContainerHosts = conf.get("Hosts",Env)
        self.Host = conf.get("h5", "Server")
        self.UserName = conf.get("Auth","UserName")
        self.Password = conf.get("Auth", "Password")

    def toolsCmd(self,Cmd):
        logs.log("Tools执行命令: Cmd: \n\"%s\"\n" % (Cmd),self.ProjectName)
        logs.log("Tools输出: OutPut: \n\"",self.ProjectName)
        print("Tools执行命令: Cmd: \n\"%s\"\n" % (Cmd), self.ProjectName)
        print("Tools输出: OutPut: \n\"")
        Output = os.system(Cmd)
        if Output != 0:
            sys.exit(1)
        logs.log("\"\n",self.ProjectName)
        print("\"\n")

    def backup(self):
        self.ProjectBackupDir = "%s/%s/%s" % (self.BackupDir, self.Host, self.ProjectName)
        if self.Env in ['prd','grey']:
            self.ProjectDir = "%s/%s" % (self.RootDir, self.ProjectName)
        else:
            self.ProjectDir = "%s/%s/%s" % (self.RootDir, self.Env, self.ProjectName)
        # 登录服务器之前判断项目目录是否存在
        IfProjectHostsDirCmd = "if [ ! -d %s ];then mkdir -p %s;fi" % (
            self.ProjectDir, self.ProjectDir)
        self.Conn.ssh(IfProjectHostsDirCmd,self.ProjectName)
        # 判断对应服务器的备份目录是否存在
        IfBackupHostsDirCmd = "if [ ! -d %s ];then mkdir -p %s;fi" % (
            self.ProjectBackupDir, self.ProjectBackupDir)
        self.Conn.ssh(IfBackupHostsDirCmd,self.ProjectName)
        # 判断对应项目保留的历史文件是否超过7个查过则删除最早的一个包
        IfBackupPackageCmd = "if [ `ls %s|wc -l` -gt 7 ];then cd %s && ls |sort |awk NR==1|xargs rm -rf;fi" % (
            self.ProjectBackupDir, self.ProjectBackupDir)
        self.toolsCmd(IfBackupPackageCmd)
        # 备份老的文件
        if self.Env in ['prd','grey']:
            BackupOldPackageCmd = "cd %s/ && tar zcf %s_%s.tar.gz %s && mv *.tar.gz %s" % (
                self.RootDir, self.ProjectName, self.DATE, self.ProjectName, self.ProjectBackupDir)
        else:
            BackupOldPackageCmd = "cd %s/iot-%s && tar zcf %s_%s.tar.gz %s && mv *.tar.gz %s" % (
            self.RootDir,self.Env,self.ProjectName,self.DATE,self.ProjectName,self.ProjectBackupDir)
        self.Conn.ssh(BackupOldPackageCmd,self.ProjectName)

    def npmCode(self):
        self.JenkinsJobDir = "%s/%s" % (self.JenkinsWorkSpaceDir, self.JenkinsJobName)
        # 删除上次的文件目录
        RmDirCmd = "rm -rf %s/%s" % (self.JenkinsJobDir,self.ProjectName)
        self.toolsCmd(RmDirCmd)
        ExecNpmCmd = "echo 未匹配;exit 1"
        if self.ProjectName == "iov-web-01":
            ExecNpmCmd = "cd %s && sudo npm install && npm run build:dev" % (self.JenkinsJobDir)
        elif self.ProjectName == "iov-web":
            if self.Env == "test":
                ExecNpmCmd = "cd %s && sudo npm install && npm run build:test" % (self.JenkinsJobDir)
            elif self.Env == "grey":
                ExecNpmCmd = "cd %s && sudo npm install && npm run build:grey" % (self.JenkinsJobDir)
            else:
                ExecNpmCmd = "cd %s && sudo npm install && npm run build" % (self.JenkinsJobDir)
        elif self.ProjectName == "iov-web-02":
            ExecNpmCmd = "cd %s && sudo npm install && npm run build:test2" % (self.JenkinsJobDir)
        elif self.ProjectName == "iov-web-03":
            ExecNpmCmd = "cd %s && sudo npm install && npm run build:test3" % (self.JenkinsJobDir)
        elif self.ProjectName == "demo-iov-web":
            ExecNpmCmd = "cd %s && sudo npm install && npm run build:demo" % (self.JenkinsJobDir)
        self.toolsCmd(ExecNpmCmd)
        self.DistFile = "%s/dist" % (self.JenkinsJobDir)
        if os.path.isdir(self.DistFile) == False:
            logs.log("NpmCode: %s文件不存在" % (self.DistFile),self.ProjectName)
            print("NpmCode: %s文件不存在" % (self.DistFile), self.ProjectName)
            sys.exit(1)

    def upload(self):
        if os.path.isdir(self.DistFile):
            MoveFileNameCmd = "mv %s %s/%s && cd %s/%s && tar zcf %s.tar.gz *" % (self.DistFile,self.JenkinsJobDir,self.ProjectName,self.JenkinsJobDir,self.ProjectName,self.ProjectName)
            self.toolsCmd(MoveFileNameCmd)
        self.SourceProjectPackageName = "%s.tar.gz" % (self.ProjectName)
        self.TargetProjectPackageName = "%s.tar.gz" % (self.ProjectName)
        # 将包上传至目标服务器
        Source = "%s/%s/%s" % (self.JenkinsJobDir,self.ProjectName, self.SourceProjectPackageName)
        Target = "%s/%s" % (self.ProjectDir, self.TargetProjectPackageName)
        logs.log("Upload: 源目录: %s 目标目录: %s\n" % (Source, Target), self.ProjectName)
        print("Upload: 源目录: %s 目标目录: %s\n" % (Source, Target))
        self.Conn.uploadFile(Source, Target)

    def execContainer(self):
        # 到远程目录解压文件
        RemoteTarFileCmd = "cd %s && tar zxf %s.tar.gz && rm -rf *.tar.gz" % (self.ProjectDir,self.ProjectName)
        self.Conn.ssh(RemoteTarFileCmd,self.ProjectName)

    def main(self):
        self.npmCode()
        for H in self.Host.split(":"):
            if Env in ['prd','grey']:
                pass
            else:
                H = "%s-%s" % (Env,H)
            self.Host = H
            self.Conn = connectionHost(H, self.UserName, self.Password)
            self.backup()
            self.upload()
            self.execContainer()

JenkinsJobName = sys.argv[1]
ProjectName = sys.argv[2]
Env = sys.argv[3]
release = projectInfo(JenkinsJobName,ProjectName,Env)
release.main()