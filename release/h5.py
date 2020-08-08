#conding:utf-8

import os
import sys
import logs
import time
import requests
from connection import connectionHost,connectionMysqlDB

class projectInfo(object):
    def __init__(self,JJN=None,PN=None, Env=None):
        self.ProjectName = PN
        self.JenkinsJobName = JJN
        self.Env = Env
        self.DATE = time.strftime('%Y%m%d%H%M%S')
        self.ConDB = connectionMysqlDB(Env)
        GetProjectInfoSql = "select Node,CheckOpsApi from Ops_projectinfo" \
                            " where Project = 'h5' and EnvPar = '%s' and Del = '0'" % (self.Env)
        self.ConDB.ConnDB(GetProjectInfoSql, self.ProjectName)
        self.Host = self.ConDB.data['Node']
        self.RootDir = self.ConDB.data['CheckOpsApi']
        GetEnvInfoSql = "select ServerUser,ServerPass,JenkinsDir,BackupDir " \
                        "from Ops_envinfo where EnvPar = '%s'" % (self.Env)
        self.ConDB.ConnDB(GetEnvInfoSql, self.ProjectName)
        self.UserName = self.ConDB.data['ServerUser']
        self.Password = self.ConDB.data['ServerPass']
        self.JenkinsWorkSpaceDir = self.ConDB.data['JenkinsDir']
        self.BackupDir = self.ConDB.data['BackupDir']

    def toolsCmd(self,Cmd):
        logs.log("Tools执行命令: Cmd: \n\"%s\"\n" % (Cmd),self.ProjectName)
        logs.log("Tools输出: OutPut: \n\"",self.ProjectName)
        print("Tools执行命令: Cmd: \n\"%s\"\n" % (Cmd), self.ProjectName)
        print("Tools输出: OutPut: \n\"")
        Output = os.system(Cmd)
        logs.log("\"\n",self.ProjectName)
        print("\"\n")

    def backup(self):
        self.ProjectBackupDir = "%s/%s/%s" % (self.BackupDir, self.Host, self.ProjectName)
        if self.Env != "prd":
            self.ProjectDir = "%s/%s/%s" % (self.RootDir, self.Env,self.ProjectName)
        else:
            self.ProjectDir = "%s/%s" % (self.RootDir, self.ProjectName)
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
        if self.Env == 'prd':
            BackupOldPackageCmd = "cd %s && tar zcf %s_%s.tar.gz %s && mv *.tar.gz %s" % (
            self.RootDir,self.ProjectName,self.DATE,self.ProjectName,self.ProjectBackupDir)
        else:
            BackupOldPackageCmd = "cd %s/%s && tar zcf %s_%s.tar.gz %s && mv *.tar.gz %s" % (
            self.RootDir,self.Env,self.ProjectName,self.DATE,self.ProjectName,self.ProjectBackupDir)
        self.Conn.ssh(BackupOldPackageCmd,self.ProjectName)

    def npmCode(self):
        self.JenkinsJobDir = "%s/%s" % (self.JenkinsWorkSpaceDir, self.JenkinsJobName)
        # 删除上次的文件目录
        RmDirCmd = "rm -rf %s/%s" % (self.JenkinsJobDir,self.ProjectName)
        self.toolsCmd(RmDirCmd)
        if self.ProjectName == "admin-front":
            if self.Env != "prd":
                ExecNpmCmd = "cd %s && sudo npm install && npm run build:stage" % (self.JenkinsJobDir)
            else:
                ExecNpmCmd = "cd %s && sudo npm install && npm run build:prod" % (self.JenkinsJobDir)
        else:
            ExecNpmCmd = "cd %s && sudo npm install && npm run build" % (self.JenkinsJobDir)
        self.toolsCmd(ExecNpmCmd)
        if self.ProjectName == "empApp":
            self.DistFile = "%s/dist_admin" % (self.JenkinsJobDir)
            if os.path.isdir(self.DistFile) == False:
                logs.log("NpmCode: %s文件不存在" % (self.DistFile), self.ProjectName)
                print("NpmCode: %s文件不存在" % (self.DistFile), self.ProjectName)
                sys.exit(1)
        else:
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
        UploadFile = "scp -P %s %s %s:%s" % (self.Port, Source, self.Host, Target)
        self.toolsCmd(UploadFile)

    def execContainer(self):
        # 到远程目录解压文件
        print("解压")
        RemoteTarFileCmd = "cd %s && tar zxf %s.tar.gz && rm -rf *.tar.gz" % (self.ProjectDir,self.ProjectName)
        self.Conn.ssh(RemoteTarFileCmd,self.ProjectName)
        if "iov-web" in ProjectName:
            message = "构建人员： %s\n环境： %s\n项目：%s\n构建分支： %s\n节点： %s\n发布完成" % (
            ReleaseUser, self.Env, self.ProjectName, ReleaseBranch, self.Host)
            self.SendWebHookQYWX(message)

    def SendWebHookQYWX(self,message):
        if self.Env == 'prd':
            SendReleaseNotifyUrl = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=49269db9-6702-4af6-9f73-f075a64fba19"
        else:
            SendReleaseNotifyUrl = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=63465ee5-88ce-4006-b212-ebaafb19636d"
        params = {
            "msgtype": "text",
            "text": {
                "content": message,
                "mentioned_list": ["@all"],
            }
        }
        header = {"Content-Type": "text/plain"}
        requests.post(url=SendReleaseNotifyUrl, headers=header, json=params)

    def main(self):
        self.npmCode()
        for H in self.Host.split(":"):
            if Env != "prd":
                H = "%s-%s" % (Env,H)
                self.Port = 22
            else:
                self.Port = 39222
            self.Host = H
            self.Conn = connectionHost(H, self.UserName, self.Password,self.Port)
            self.backup()
            self.upload()
            self.execContainer()


JenkinsJobName = sys.argv[1]
ProjectName = sys.argv[2]
Env = sys.argv[3]
ReleaseUser = sys.argv[4]
ReleaseBranch = sys.argv[5]
release = projectInfo(JenkinsJobName,ProjectName,Env)
release.main()
