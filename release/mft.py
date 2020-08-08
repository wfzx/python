#conding:utf-8

import os
import sys
import logs
import time
import requests
import configparser
from connection import connectionHost

class projectInfo(object):
    def __init__(self,JJN=None,PN=None, Env=None,MS=None):
        if Env == "prd":
            self.ConfName = "/data/release/conf/mft-prd"
        else:
            self.ConfName = "/data/release/conf/mft-test"
        conf = configparser.ConfigParser()
        conf.read(self.ConfName)
        self.ProjectName = PN
        self.JenkinsJobName = JJN
        self.Env = Env
        self.DATE = time.strftime('%Y%m%d%H%M%S')
        self.RootDir = conf.get("Env", "RootDir")
        self.BackupDir = conf.get("Env", "BackupDir")
        self.JenkinsWorkSpaceDir = conf.get("Env", "JenkinsDir")
        self.ContainerHosts = conf.get("Hosts",Env)
        self.Host = conf.get(PN, MS)
        self.UserName = conf.get("Auth","UserName")
        self.Password = conf.get("Auth", "Password")
        self.CheckApi = conf.get(PN,"CheckApi")
        self.ProjectPort = conf.get(PN,"Port")
        self.Type = conf.get(PN,"Type")
        self.MemSize = int(conf.get(PN,"MemSize"))
        self.Xmnm = self.MemSize // 8 * 3
        self.XX = self.MemSize // 4
        self.HarborAddress = conf.get("Env","Harbor")
        self.HarborUserName = conf.get("Env","UserName")
        self.HarborPassword = conf.get("Env", "Password")
        self.ResetContainer = conf.get("Env", "Reset")

    def toolsCmd(self,*args):
        for i in range(0,len(args)):
            Cmd = args[i]
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
        self.ProjectBackupDir = "%s/%s/%s" % (self.BackupDir,self.Host,self.ProjectName)
        self.ProjectDir = "%s/%s/%s" % (self.RootDir,self.Host,self.ProjectName)
        # 登录服务器之前判断项目目录是否存在
        IfProjectHostsDirCmd = "if [ ! -d %s ];then mkdir -p %s;fi" % (
            self.ProjectDir, self.ProjectDir)
        self.Conn.ssh(IfProjectHostsDirCmd,self.ProjectName)
        # 判断对应服务器的备份目录是否存在
        IfBackupHostsDirCmd = "if [ ! -d %s ];then mkdir -p %s;fi" % (
            self.ProjectBackupDir,self.ProjectBackupDir)
        self.toolsCmd(IfBackupHostsDirCmd)
        # 判断对应项目保留的历史文件是否超过7个查过则删除最早的一个包
        IfBackupPackageCmd = "if [ `ls %s|wc -l` -gt 7 ];then cd %s && ls |sort |awk NR==1|xargs rm -f;fi" % (
            self.ProjectBackupDir,self.ProjectBackupDir)
        self.toolsCmd(IfBackupPackageCmd)
        # 备份老的文件
        BackupOldPackageCmd = "if [ -f %s/%s* ];then mv %s/%s* %s/%s.%s_%s;fi" % (
            self.ProjectDir,self.ProjectName,self.ProjectDir,self.ProjectName,self.ProjectBackupDir,
            self.ProjectName,self.Type,self.DATE)
        self.toolsCmd(BackupOldPackageCmd)

    def upload(self):
        JenkinsJobDir = "%s/%s" % (self.JenkinsWorkSpaceDir,self.JenkinsJobName)
        if os.path.isdir("%s/target" % (JenkinsJobDir)):
            self.JenkinsTargetDir = "%s/target" % (JenkinsJobDir)
        else:
            self.JenkinsTargetDir = "%s/%s/target" % (JenkinsJobDir, self.ProjectName)

        # 判断包是jar还是war
        for JW in os.listdir(self.JenkinsTargetDir):
            if ".war" in JW:
                self.SourceProjectPackageName = JW
                self.TargetProjectPackageName = "%s.war" % (self.ProjectName)
                break
        # 将包上传至目标服务器
        Source = "%s/%s" % (self.JenkinsTargetDir,self.SourceProjectPackageName)
        Target = "%s/%s" % (self.ProjectDir,self.TargetProjectPackageName)
        logs.log("Upload: 目标主机: %s 源目录: %s 目标目录: %s\n" % (self.Host,Source,Target),self.ProjectName)
        print ("Upload: 目标主机: %s 源目录: %s 目标目录: %s\n" % (self.Host,Source,Target))
        UploadFile = "scp -P %s %s %s:%s" % (self.Port, Source, self.Host, Target)
        self.toolsCmd(UploadFile)

    def rollback(self):
        self.ProjectBackupDir = "%s/%s/%s" % (self.BackupDir, self.Host, self.ProjectName)
        self.ProjectDir = "%s/%s/%s" % (self.RootDir, self.Host, self.ProjectName)
        logs.log("Rollback: Source: %s" % (os.listdir(self.ProjectBackupDir)))
        print("回滚源:")
        SourceName = os.listdir(self.ProjectBackupDir)
        SourceName.sort()
        for S in range(0,len(SourceName)):
            print(SourceName[S])
        RollbackName = input("请输入上面回滚源名称:")
        Source = "%s/%s" % (self.ProjectBackupDir,RollbackName)
        Target = "%s/%s.%s" % (self.ProjectDir, self.ProjectName,self.Type)
        logs.log("Rollback: 目标主机: %s 源目录: %s 目标目录: %s\n" % (self.Host,Source, Target), self.ProjectName)
        print("Rollback: 目标主机: %s 源目录: %s 目标目录: %s\n" % (self.Host,Source, Target))
        RollbackCmd = "mv %s %s" % (Source,Target)
        self.toolsCmd(RollbackCmd)

    def getIfResetContainer(self):
        if self.ProjectName in self.ResetContainer:
            self.ResetValue = "1"
            ReplaceResetValue = self.ResetContainer.replace("%s," % (self.ProjectName), "")
        else:
            self.ResetValue = "0"
            ReplaceResetValue = self.ResetContainer
        with open(self.ConfName, 'r') as Original, open('temp', 'w') as ReplaceTmp:
            for BodyLine in Original.readlines():
                if "Reset = " in BodyLine:
                    BodyLine = BodyLine.replace(BodyLine, "Reset = %s\n" % (ReplaceResetValue))
                ReplaceTmp.write(BodyLine)
        os.remove(self.ConfName)
        os.rename("temp", self.ConfName)

    def execContainer(self):
        # 判断目标服务器是否存在对应项目的容器
        if self.ResetValue == "0":
            RestartCmd = "docker restart %s" % (self.ProjectName)
            # 重新启动容器加载新的java包
            self.Conn.ssh(RestartCmd, self.ProjectName)
        else:
            # 删除老容器
            StopOldContainer = "docker ps -a|grep %s|grep -v CON|awk '{print $1}'|xargs docker stop" % (self.ProjectName)
            RmOldContainer = "docker ps -a|grep %s|grep -v CON|awk '{print $1}'|xargs docker rm" % (self.ProjectName)
            self.Conn.ssh(StopOldContainer,RmOldContainer,self.ProjectName)
            # 初始化镜像
            # 创建target目录下的docker目录
            MkdirDockerDirCmd = "cd %s && if [ ! -d docker ];then mkdir docker;fi" % (self.JenkinsTargetDir)
            self.toolsCmd(MkdirDockerDirCmd)
            ModifyDockerfileBodyCmd = "sed -i 's/Crs_SuExamy/%s/g' /data/release/dockerfile/War" % (
                self.HarborAddress
            )
            ModifyDockerfileServiceNameCmd = "sed -i 's/ServiceName/mft-%s/g' /data/release/dockerfile/War" % (
                self.ProjectName
            )
            CopyDockerfileCmd = "cp /data/release/dockerfile/War %s/docker/Dockerfile" % (
                self.JenkinsTargetDir
            )
            ReductionModifyDockerfileBodyCmd = "sed -i 's/%s/Crs_SuExamy/g' /data/release/dockerfile/War" % (
                self.HarborAddress
            )
            ReductionModifyDockerfileServiceNameCmd = "sed -i 's/mft-%s/ServiceName/g' /data/release/dockerfile/War" % (
                self.ProjectName
            )
            BuildDockerImageCmd = "cd %s/docker && docker build -t %s/crs_war/mft-%s ." % (
                self.JenkinsTargetDir, self.HarborAddress, self.ProjectName
            )
            HarborLoginCmd = "docker login --username=%s --password=%s %s" % (
                self.HarborUserName, self.HarborPassword, self.HarborAddress
            )
            PushImageToHarborCmd = "docker push %s/crs_war/mft-%s" % (
                self.HarborAddress, self.ProjectName
            )
            PullTargetImageToHarborCmd = "docker pull %s/crs_war/mft-%s" % (
                self.HarborAddress, self.ProjectName
            )
            # 判断不是生产环境就将dockerfile中的地址更改为测试的harbor
            self.toolsCmd(ModifyDockerfileBodyCmd)
            self.toolsCmd(ModifyDockerfileServiceNameCmd)
            # 将对应dockerfile拷贝到docker目录下
            self.toolsCmd(CopyDockerfileCmd)
            # 还原dockerfile内容
            self.toolsCmd(ReductionModifyDockerfileBodyCmd)
            self.toolsCmd(ReductionModifyDockerfileServiceNameCmd)
            # 构建docker镜像
            self.toolsCmd(BuildDockerImageCmd)
            # 登录镜像仓库
            self.toolsCmd(HarborLoginCmd)
            # 上传镜像到harbor仓库
            self.toolsCmd(PushImageToHarborCmd)
            # 在目标机器登录镜像源
            self.Conn.ssh(HarborLoginCmd, self.ProjectName)
            # 在目标机器拉取镜像
            self.Conn.ssh(PullTargetImageToHarborCmd, self.ProjectName)
            # 固定的java启动内存设置
            JavaMem = "-Xmx%sm -Xms%sm -Xmn%sm -XX:PermSize=%sm -XX:MaxPermSize=%sm -Duser.timezone=Asia/Shanghai" % (
                self.MemSize,self.MemSize,self.Xmnm,self.XX,self.XX
            )
            # 宿主机上挂载日志的目录名称
            MountProjectName = self.ProjectName
            # 指定容器主机名
            DockerRunPar = "-h %s" % (self.ProjectName)
            # 判断挂载jar/war项目
            MountProjectJW = "%s:/%s" % (self.ProjectDir, self.ProjectName)
            JavaCmd = "%s -jar /%s/%s --spring.profiles.active=%s --server.port=%s" % (
                JavaMem, self.ProjectName, self.TargetProjectPackageName, self.Env, self.ProjectPort)
            # 判断服务的进行添加特殊参数
            if ".war" in self.TargetProjectPackageName:
                MountProjectJW = "%s:/mft-%s/mft-%s" % (self.ProjectDir, self.ProjectName,self.ProjectName)
                JavaCmd = "sh /mft-%s/info.sh %s" % (self.ProjectName,self.ProjectName)
            # 判断日志挂载目录是否存在
            IfLogMountDirCmd = "if [ ! -d /data/mount/logs/%s-%s/%s ];then mkdir -p /data/mount/logs/%s-%s/%s;fi" % (
                self.Env,self.ProjectName,self.Host,self.Env,self.ProjectName,self.Host)
            self.toolsCmd(IfLogMountDirCmd)
            # 在目标机器启动容器
            StartContainerCmd = "docker run -dit " \
                                "%s %s " \
                                "-v /data/mount/db:/data/db " \
                                "-v /data/mount/logs/%s-mft-%s/%s:/alidata1/log/mft-%s " \
                                "-v /data/mount/logs/%s-mft-%s/%s/logs:/mft-%s/logs " \
                                "-v %s " \
                                "--name %s " \
                                "--net host " \
                                "%s/crs_war/mft-%s " \
                                "%s" % (
                self.ContainerHosts,DockerRunPar,self.Env,MountProjectName,self.Host,self.ProjectName,self.Env,MountProjectName,self.Host,self.ProjectName,MountProjectJW,self.ProjectName,
                self.HarborAddress,self.ProjectName,JavaCmd)
            self.Conn.ssh(StartContainerCmd, self.ProjectName)

    def checkApi(self):
        if self.CheckApi != "/":
            Url = "http://%s:%s%s" % (self.Host, self.ProjectPort, self.CheckApi)
            Time = 240
            for T in range(1, Time):
                try:
                    Code = requests.get(Url, timeout=1)
                    if Code.status_code == 200:
                        logs.log("接口监测成功: url: %s code: %s" % (Url, Code.status_code),self.ProjectName)
                        print("接口监测成功: url: %s code: %s" % (Url, Code.status_code))
                        break
                    else:
                        logs.log("接口监测失败: url: %s code: %s 请联系对应开发健康监测返回状态不为200" % (Url, Code.status_code),self.ProjectName)
                        print("接口监测失败: url: %s code: %s 请联系对应开发健康监测返回状态不为200" % (Url, Code.status_code))
                        logs.log("==================以下为服务启动最后100行日志==================", self.ProjectName)
                        print("==================以下为服务启动最后100行日志==================")
                        DockerLogsCmd = "docker logs --tail=100 %s" % (self.ProjectName)
                        self.Conn.ssh(DockerLogsCmd, self.ProjectName)
                        sys.exit(1)
                except requests.exceptions.ConnectionError:
                    if T == Time - 1:
                        logs.log("接口检测失败: url: %s status: 退出" % (Url),self.ProjectName)
                        print("接口检测失败: url: %s status: 退出" % (Url))
                        logs.log("==================以下为服务启动最后100行日志==================",self.ProjectName)
                        print("==================以下为服务启动最后100行日志==================")
                        DockerLogsCmd = "docker logs --tail=100 %s" % (self.ProjectName)
                        self.Conn.ssh(DockerLogsCmd, self.ProjectName)
                        sys.exit(1)
                    else:
                        logs.log("接口检测: url: %s status: 服务正在启动" % (Url),self.ProjectName)
                        print("接口监测: url: %s status: 服务正在启动" % (Url))
                    time.sleep(1)
                    continue
                except requests.exceptions.ReadTimeout:
                    if T == Time - 1:
                        logs.log("接口检测失败: url: %s status: 退出" % (Url),self.ProjectName)
                        print("接口检测失败: url: %s status: 退出" % (Url))
                        logs.log("==================以下为服务启动最后100行日志==================",self.ProjectName)
                        print("==================以下为服务启动最后100行日志==================")
                        DockerLogsCmd = "docker logs --tail=100 %s" % (self.ProjectName)
                        self.Conn.ssh(DockerLogsCmd, self.ProjectName)
                        sys.exit(1)
                    else:
                        logs.log("接口监测: url: %s status: 服务正在启动" % (Url),self.ProjectName)
                        print("接口监测: url: %s status: 服务正在启动" % (Url))
                    continue

    def main(self):
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
            self.getIfResetContainer()
            self.execContainer()
            self.checkApi()

    def rollbackMain(self):
        for H in self.Host.split(":"):
            if Env != "prd":
                H = "%s-%s" % (Env,H)
                self.Port = 22
            else:
                self.Port = 39222
            self.Host = H
            self.Conn = connectionHost(H, self.UserName, self.Password,self.Port)
            self.backup()
            self.rollback()
            self.execContainer()
            self.checkApi()

JenkinsJobName = sys.argv[1]
ProjectName = sys.argv[2]
Env = sys.argv[3]
MasterSlave = sys.argv[4]
release = projectInfo(JenkinsJobName,ProjectName,Env,MasterSlave)
if JenkinsJobName == "rollback":
    release.rollbackMain()
else:
    release.main()