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
        self.ConDB = connectionMysqlDB(Env)
        if 'mft' in self.JenkinsJobName:
            Belong = 'MFT'
        elif 'iot' in self.JenkinsJobName:
            Belong = 'IOT'
        else:
            Belong = 'PT'
        GetProjectInfoSql = "select Node,Port,MemSize,CheckOpsApi,ServerType,ReSet," \
                            "OldNode,OldNodeRm,OldPort,ReTengine,Belong,AddSkywalking from Ops_projectinfo" \
                            " where Project = '%s' and EnvPar = '%s' and Del = '0' and Belong = '%s'" % (
            self.ProjectName,self.Env,Belong)
        self.ConDB.ConnDB(GetProjectInfoSql,self.ProjectName)
        self.Host = self.ConDB.data['Node']
        self.ProjectPort = self.ConDB.data['Port']
        self.MemSize = int(self.ConDB.data['MemSize'])
        self.Xmnm = self.MemSize // 8 * 3
        self.XX = self.MemSize // 4
        self.CheckApi = self.ConDB.data['CheckOpsApi']
        self.Type = self.ConDB.data['ServerType']
        self.ResetContainer = self.ConDB.data['ReSet']
        self.OldNode = self.ConDB.data['OldNode']
        self.OldPort = self.ConDB.data['OldPort']
        self.OldNodeRm = self.ConDB.data['OldNodeRm']
        self.ReTengine = self.ConDB.data['ReTengine']
        self.Belong = self.ConDB.data['Belong']
        self.AddSkywalking = self.ConDB.data['AddSkywalking']
        GetEnvInfoSql = "select ServerUser,ServerPass,RepoAddress,RepoUser,JavaStartPar,SkywalkingAddress," \
                        "RepoPass,JenkinsDir,RootDir,BackupDir,EurekaAddress,Hosts,TenDir " \
                        "from Ops_envinfo where EnvPar = '%s'" % (self.Env)
        self.ConDB.ConnDB(GetEnvInfoSql,self.ProjectName)
        self.DATE = time.strftime('%Y%m%d%H%M%S')
        self.RootDir = self.ConDB.data['RootDir']
        self.BackupDir = self.ConDB.data['BackupDir']
        self.JenkinsWorkSpaceDir = self.ConDB.data['JenkinsDir']
        self.ContainerHosts = self.ConDB.data['Hosts']
        self.UserName = self.ConDB.data['ServerUser']
        self.Password = self.ConDB.data['ServerPass']
        self.HarborAddress = self.ConDB.data['RepoAddress']
        self.HarborUserName = self.ConDB.data['RepoUser']
        self.HarborPassword = self.ConDB.data['RepoPass']
        self.EurekaAddress = self.ConDB.data['EurekaAddress']
        self.TenDir = self.ConDB.data['TenDir']
        self.JavaStartPar = self.ConDB.data['JavaStartPar']
        self.SkywalkingAddress = self.ConDB.data['SkywalkingAddress']
        if self.Env in ['test02','dev']:
            Env = "test"
        else:
            Env = self.Env
        GetTengineNodeSql = "select Node from Ops_projectinfo" \
                            " where Project = 'h5' and EnvPar = '%s' and Del = '0'" % (Env)
        self.ConDB.ConnDB(GetTengineNodeSql,self.ProjectName)
        self.TengineNode = self.ConDB.data['Node']

    def toolsCmd(self,*args):
        for i in range(0,len(args)):
            Cmd = args[i]
            logs.log("Tools执行命令: Cmd: \n%s\n" % (Cmd),self.ProjectName)
            logs.log("Tools输出: OutPut: \n",self.ProjectName)
            print("Tools执行命令: Cmd: \n%s\n" % (Cmd), self.ProjectName)
            print("Tools输出: OutPut: \n")
            Output = os.system(Cmd)
            if Output != 0:
                sys.exit(1)
            logs.log("\n",self.ProjectName)
            print("\n")

    def ifPackJarWar(self):
        JenkinsJobDir = "%s/%s" % (self.JenkinsWorkSpaceDir, self.JenkinsJobName)
        if os.path.isdir("%s/target" % (JenkinsJobDir)):
            self.JenkinsTargetDir = "%s/target" % (JenkinsJobDir)
        else:
            self.JenkinsTargetDir = "%s/%s/target" % (JenkinsJobDir, self.ProjectName)

        # 判断包是jar还是war
        for JW in os.listdir(self.JenkinsTargetDir):
            if ".jar" in JW:
                if "original" in JW:
                    continue
                self.SourceProjectPackageName = JW
                self.TargetProjectPackageName = "%s.jar" % (self.ProjectName)
                break
            elif ".war" in JW:
                self.SourceProjectPackageName = JW
                if self.Belong == 'MFT':
                    self.TargetProjectPackageName = "mft-%s.war" % (self.ProjectName)
                else:
                    self.TargetProjectPackageName = "%s.war" % (self.ProjectName)
                break

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
        # 判断对应项目保留的历史文件是否超过7个查过则删除最早的一个包
        IfBackupPackageCmd = "if [ `ls %s|wc -l` -gt 7 ];then cd %s && ls |sort |awk NR==1|xargs rm -f;fi" % (
            self.ProjectBackupDir,self.ProjectBackupDir)
        self.toolsCmd(IfBackupHostsDirCmd,IfBackupPackageCmd)
        # 备份老的文件
        if  self.JenkinsJobName == 'rollback':
            BackupOldPackageCmd = "if [ -f %s/%s* ];then mv -f %s/*%s* %s/%s.%s_%s;fi" % (
                self.ProjectDir,self.ProjectName,self.ProjectDir,self.ProjectName,self.ProjectBackupDir,
                self.ProjectName,self.Type,self.DATE)
        else:
            BackupOldPackageCmd = "if [ -f %s/%s ];then mv -f %s/*%s* %s/%s.%s_%s;fi" % (
                self.ProjectDir,self.TargetProjectPackageName,self.ProjectDir,self.ProjectName,self.ProjectBackupDir,
                self.ProjectName,self.Type,self.DATE)
        self.Conn.ssh(BackupOldPackageCmd,self.ProjectName)
        # 检查备份是否存在
        BackupFileCheckCmd = "if [ ! -f %s/%s.%s_%s ];then echo '退出' && exit 1;fi" % (
            self.ProjectBackupDir,self.ProjectName,self.Type,self.DATE
        )
        self.Conn.ssh(BackupFileCheckCmd,self.ProjectName)

    def upload(self):
        # 将包上传至目标服务器
        Source = "%s/%s" % (self.JenkinsTargetDir,self.SourceProjectPackageName)
        Target = "%s/%s" % (self.ProjectDir,self.TargetProjectPackageName)
        logs.log("Upload: 目标主机: %s 源目录: %s 目标目录: %s\n" % (self.Host,Source,Target),self.ProjectName)
        print ("Upload: 目标主机: %s 源目录: %s 目标目录: %s\n" % (self.Host,Source,Target))
        UploadFile = "scp -P %s %s %s:%s" % (self.Port,Source,self.Host,Target)
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
        if self.RegisterEureka == "0":
            if Env == "prd":
                self.putEurekaStatusDown()
        self.backup()
        UploadFile = "scp -P %s %s %s:%s" % (self.Port, Source, self.Host, Target)
        self.toolsCmd(UploadFile)

    def putEurekaStatusDown(self):
        # 执行前先从eureka取消注册
        DownUrl = "http://%s/eureka/apps/%s/%s:%s:%s/status?value=DOWN" % (
        self.EurekaAddress, self.ProjectName.upper(), self.IP,
        self.ProjectName, self.ProjectPort)
        # 向eureka发送服务DOWN状态,并等待15秒
        logs.log("向eureka发送服务DOWN状态: url: %s" % (DownUrl), self.ProjectName)
        print("向eureka发送服务DOWN状态: url: %s" % (DownUrl))
        requests.put(DownUrl)
        time.sleep(15)

    def putEurekaStatusUP(self):
        # 执行前先从eureka取消注册
        UPUrl = "http://%s/eureka/apps/%s/%s:%s:%s/status?value=UP" % (
        self.EurekaAddress, self.ProjectName.upper(), self.IP,
        self.ProjectName, self.ProjectPort)
        # 向eureka发送服务DOWN状态,并等待15秒
        logs.log("向eureka发送服务UP状态: url: %s" % (UPUrl), self.ProjectName)
        print("向eureka发送服务UP状态: url: %s" % (UPUrl))
        requests.put(UPUrl)

    def getIfResetContainer(self):
        ReleaseTime = time.strftime('%Y-%m-%d %H:%M:%S')
        if self.ResetContainer == '1':
            self.ResetValue = '1'
            self.execContainer()
            self.checkApi()
            ResetValueIsZeroOrUpdateReleaseTime = "update Ops_projectinfo set ReSet = 0, ReleaseTime = '%s',AddSkywalking = 2 where Project = '%s' " \
                               "and EnvPar = '%s' and Del = '0'and Belong = '%s'" % (ReleaseTime,self.ProjectName,self.Env,self.Belong)
            self.ConDB.ConnDB(ResetValueIsZeroOrUpdateReleaseTime,self.ProjectName)
        else:
            self.ResetValue = '0'
            self.execContainer()
            self.checkApi()
            ResetValueIsZeroOrUpdateReleaseTime = "update Ops_projectinfo set ReleaseTime = '%s' where Project = '%s' " \
                               "and EnvPar = '%s' and Del = '0'and Belong = '%s'" % (
                               ReleaseTime, self.ProjectName, self.Env, self.Belong)
            self.ConDB.ConnDB(ResetValueIsZeroOrUpdateReleaseTime, self.ProjectName)

    def execContainer(self):
        if self.Belong == 'MFT':
            if ".war" in self.TargetProjectPackageName:
                self.ProjectName = "mft-%s" % (self.ProjectName)
        ContainerName = "%s-%s-%s" % (self.Env,self.Belong,self.ProjectName)
        ContainerOldName = "%s-%s" % (self.Env,self.ProjectName)
        ContainerOldTwoName = "%s" % (self.ProjectName)
        if self.ResetValue == "0":
            RestartOldCmd = "if [ ! -z `docker ps -a|grep %s |grep -v CON|awk '{print $1}'` ];then docker restart %s ;" \
                         "else echo '调试兼容性';fi" % (ContainerOldName,ContainerOldName)
            RestartCmd = "if [ ! -z `docker ps -a|grep %s |grep -v CON|awk '{print $1}'` ];then docker restart %s ;" \
                         "else echo '请联系运维';fi" % (ContainerName,ContainerName)
            # 重新启动容器加载新的java包
            self.Conn.ssh(RestartOldCmd, self.ProjectName)
            if self.Conn.ssh(RestartCmd, self.ProjectName) == 1:
                sys.exit(1)
        else:
            # 删除老容器
            SROldOldContainer = "if [ ! -z `docker ps -a|grep %s|grep -v CON|awk '{print $1}'` ];then docker ps -a|grep %s" \
                             "|grep -v CON|awk '{print $1}'|xargs docker stop && docker ps -a|grep %s|grep -v CON" \
                             "|awk '{print $1}'|xargs docker rm;fi" % \
                             (ContainerOldName,ContainerOldName,ContainerOldName)
            SROldContainer = "if [ ! -z `docker ps -a|grep %s|grep -v CON|awk '{print $1}'` ];then docker ps -a|grep %s" \
                             "|grep -v CON|awk '{print $1}'|xargs docker stop && docker ps -a|grep %s|grep -v CON" \
                             "|awk '{print $1}'|xargs docker rm;fi" % \
                             (ContainerName, ContainerName, ContainerName)
            SROldTwoContainer = "if [ ! -z `docker ps -a|grep %s|grep -v CON|awk '{print $1}'` ];then docker ps -a|grep %s" \
                             "|grep -v CON|awk '{print $1}'|xargs docker stop && docker ps -a|grep %s|grep -v CON" \
                             "|awk '{print $1}'|xargs docker rm;fi" % \
                             (ContainerOldTwoName, ContainerOldTwoName, ContainerOldTwoName)
            self.Conn.ssh(SROldOldContainer, self.ProjectName)
            self.Conn.ssh(SROldContainer,self.ProjectName)
            self.Conn.ssh(SROldTwoContainer,self.ProjectName)
            # 初始化镜像
            # 创建target目录下的docker目录
            MkdirDockerDirCmd = "cd %s && if [ ! -d docker ];then mkdir docker;fi" % (self.JenkinsTargetDir)
            self.toolsCmd(MkdirDockerDirCmd)
            if ".war" in self.TargetProjectPackageName:
                self.ImagesRepoName = "crs_war"
                ModifyDockerfileBodyCmd = "sed -i 's/Crs_SuExamy/%s/g' /data/release/dockerfile/War" % (
                    self.HarborAddress
                )
                ModifyDockerfileServiceNameCmd = "sed -i 's/ServiceName/%s/g' /data/release/dockerfile/War" % (
                    self.ProjectName
                )
                CopyDockerfileCmd = "cp /data/release/dockerfile/War %s/docker/Dockerfile" % (
                    self.JenkinsTargetDir
                )
                ReductionModifyDockerfileBodyCmd = "sed -i 's/%s/Crs_SuExamy/g' /data/release/dockerfile/War" % (
                    self.HarborAddress
                )
                ReductionModifyDockerfileServiceNameCmd = "sed -i 's/%s/ServiceName/g' /data/release/dockerfile/War" % (
                    self.ProjectName
                )
                DeleteUselessImagesCmd = "docker image prune -f"
                BuildDockerImageCmd = "cd %s/docker && docker build -t %s/%s/%s ." % (
                    self.JenkinsTargetDir, self.HarborAddress,self.ImagesRepoName, self.ProjectName
                )
                HarborLoginCmd = "docker login --username=%s --password=%s %s" % (
                    self.HarborUserName, self.HarborPassword, self.HarborAddress
                )
                PushImageToHarborCmd = "docker push %s/%s/%s" % (
                    self.HarborAddress, self.ImagesRepoName,self.ProjectName
                )
                DeleteOldImagesCmd = "docker image prune -f"
                PullTargetImageToHarborCmd = "docker pull %s/%s/%s" % (
                    self.HarborAddress, self.ImagesRepoName,self.ProjectName
                )
            else:
                self.ImagesRepoName = "crs_jar"
                ModifyDockerfileBodyCmd = "sed -i 's/registry.cn-shanghai.aliyuncs.com/%s/g' /data/release/dockerfile/Jar" % (
                    self.HarborAddress
                )
                ModifyDockerfileServiceNameCmd = "echo %s" % (
                    self.ProjectName
                )
                CopyDockerfileCmd = "cp /data/release/dockerfile/Jar %s/docker/Dockerfile" % (
                    self.JenkinsTargetDir
                )
                ReductionModifyDockerfileBodyCmd = "sed -i 's/%s/registry.cn-shanghai.aliyuncs.com/g' /data/release/dockerfile/Jar" % (
                    self.HarborAddress
                )
                ReductionModifyDockerfileServiceNameCmd = "echo %s" % (
                    self.ProjectName
                )
                DeleteUselessImagesCmd = "docker image prune -f"
                BuildDockerImageCmd = "cd %s/docker && docker build -t %s/%s/%s ." % (
                    self.JenkinsTargetDir, self.HarborAddress, self.ImagesRepoName,self.ProjectName
                )
                HarborLoginCmd = "docker login --username=%s --password=%s %s" % (
                    self.HarborUserName, self.HarborPassword, self.HarborAddress
                )
                PushImageToHarborCmd = "docker push %s/%s/%s" % (
                    self.HarborAddress, self.ImagesRepoName,self.ProjectName
                )
                DeleteOldImagesCmd = "docker image prune -f"
                PullTargetImageToHarborCmd = "docker pull %s/%s/%s" % (
                    self.HarborAddress, self.ImagesRepoName,self.ProjectName
                )
            # 判断不是生产环境就将dockerfile中的地址更改为测试的harbor
            # 将对应dockerfile拷贝到docker目录下
            # 还原dockerfile内容
            # 删除tools无用的镜像
            # 构建docker镜像
            # 登录镜像仓库
            # 上传镜像到harbor仓库
            self.toolsCmd(ModifyDockerfileBodyCmd,ModifyDockerfileServiceNameCmd,CopyDockerfileCmd,
                          ReductionModifyDockerfileBodyCmd,ReductionModifyDockerfileServiceNameCmd,
                          DeleteUselessImagesCmd,HarborLoginCmd,BuildDockerImageCmd,PushImageToHarborCmd)
            # 登录镜像源、删除老镜像、拉取镜像
            self.Conn.ssh(HarborLoginCmd,DeleteOldImagesCmd,PullTargetImageToHarborCmd,self.ProjectName)
            # 固定的java启动内存设置
            if self.AddSkywalking == "0":
                JavaAgent = " "
            else:
                JavaAgent = "-javaagent:/Agent/agent/skywalking-agent.jar -DSW_AGENT_NAME=%s-%s-%s -DSW_AGENT_COLLECTOR_BACKEND_SERVICES=%s" % (
            self.Env, self.Belong, self.ProjectName, self.SkywalkingAddress)
            JavaMem = "%s -Xmx%sm -Xms%sm -Xmn%sm -XX:PermSize=%sm -XX:MaxPermSize=%sm -Duser.timezone=Asia/Shanghai" % (
                JavaAgent, self.MemSize, self.MemSize, self.Xmnm, self.XX, self.XX
            )
            # 宿主机上挂载日志的目录名称
            MountProjectName = self.ProjectName
            TargetMountProjectName = self.ProjectName
            # 指定容器主机名
            DockerRunPar = "-h %s" % (self.ProjectName)
            # 判断挂载jar/war项目
            MountProjectJW = "%s:/%s" % (self.ProjectDir, self.ProjectName)
            JavaCmd = self.JavaStartPar % (JavaMem, self.ProjectName, self.TargetProjectPackageName, self.Env, self.ProjectPort)
            # 判断服务的进行添加特殊参数
            if ".war" in self.TargetProjectPackageName:
                MountProjectJW = "%s:/%s/%s" % (self.ProjectDir, self.ProjectName,self.ProjectName)
                JavaCmd = "sh /%s/info.sh %s" % (self.ProjectName,self.ProjectName)
            elif self.ProjectName == "eureka-server":
                if self.Env == "prd":
                    if self.Host == "jar02":
                        JavaCmd = "%s -jar /%s/%s --spring.profiles.active=prd2 --server.port=%s" % (
                            JavaMem,self.ProjectName,self.TargetProjectPackageName,self.ProjectPort
                        )
            elif self.ProjectName == "commonrail-report":
                JavaMem = "%s -Xss6m" % (JavaMem)
                JavaCmd = self.JavaStartPar % (JavaMem, self.ProjectName, self.TargetProjectPackageName, self.Env, self.ProjectPort)
            elif "manage-" in self.ProjectName:
                MountProjectName = "manage-network"
            MountDir = "%s-%s-%s" % (self.Env,self.Belong,TargetMountProjectName)
            # 判断日志挂载目录是否存在
            IfLogMountDirCmd = "if [ ! -d /data/mount/logs/%s ];then mkdir -p /data/mount/logs/%s;fi" % (MountDir,MountDir)
            # 临时使用##############################################################################################
            ContainerName = "%s-%s-%s" % (self.Env,self.Belong,self.ProjectName)
            # 在目标机器启动容器
            StartContainerCmd = "docker run -dit " \
                                "%s %s " \
                                "-v /data/mount/cert/keys:/alidata1/shell/keys/url " \
                                "-v /data/mount/cert/httpskey:/alidata1/httpskey " \
                                "-v /data/mount/cert/httpskey_app:/alidata1/httpskey_app " \
                                "-v /data/mount/cert/httpskey_klb:/alidata1/httpskey_klb " \
                                "-v /data/mount/db:/alidata1/db " \
                                "-v /data/mount/static:/alidata1/static " \
                                "-v /data/mount/aggregation-data:/alidata1/aggregation-data " \
                                "-v /data/mount/logs/%s:/alidata1/log/%s " \
                                "-v /data/mount/Agent:/Agent " \
                                "-v /mnt/ota_version:/home/fdfs_storage/data/ota_version " \
                                "-v /mnt/solr:/alidata1/solr " \
                                "-v %s " \
                                "--name %s " \
                                "--net host " \
                                "%s/%s/%s " \
                                "%s" % (
                self.ContainerHosts, DockerRunPar, MountDir, MountProjectName, MountProjectJW,
                ContainerName, self.HarborAddress, self.ImagesRepoName, self.ProjectName, JavaCmd
            )
            # 登录镜像源、删除老镜像、拉取镜像、创建日志挂载目录、执行创建镜像
            self.Conn.ssh(HarborLoginCmd, DeleteOldImagesCmd, PullTargetImageToHarborCmd, IfLogMountDirCmd,
                          StartContainerCmd, self.ProjectName
                          )

    def SendWebHookQYWX(self,message):
        if self.Belong == 'PT':
            SendReleaseNotifyUrl = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d8d7c526-a57e-4202-8de4-5b0a7972c24a"
        elif self.Belong == 'MFT':
            SendReleaseNotifyUrl = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=6d39ec1a-c543-4569-859d-8c0bef67b319"
        elif self.Belong == 'IOT':
            if self.Env == 'prd':
                SendReleaseNotifyUrl = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=49269db9-6702-4af6-9f73-f075a64fba19"
            else:
                SendReleaseNotifyUrl = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=63465ee5-88ce-4006-b212-ebaafb19636d"
        params = {
            "msgtype": "text",
            "text": {
                "content": message,
            }
        }
        header = {"Content-Type": "text/plain"}
        requests.post(url=SendReleaseNotifyUrl, headers=header, json=params)

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
                        if self.RegisterEureka == "0":
                            CheckEurekaStatusUrl = "http://%s/eureka/instances/%s:%s:%s" % (
                                self.EurekaAddress, self.IP,self.ProjectName, self.ProjectPort)
                            logs.log("获取eureka服务状态: url: %s" % (CheckEurekaStatusUrl),self.ProjectName)
                            print("获取eureka服务状态: url: %s" % (CheckEurekaStatusUrl))
                            time.sleep(2)
                            GetUrl = requests.get(CheckEurekaStatusUrl)
                            logs.log("获取eureka服务状态返回的内容: %s" % (GetUrl.text), self.ProjectName)
                            try:
                                UrlStatus = GetUrl.text.split('<status>')[1].split('</status>')[0]
                            except IndexError:
                                logs.log("请开发人员配置项目名在配置文件中",self.ProjectName)
                                print("请开发人员配置项目名在配置文件中")
                                message = "构建人员： %s\n环境： %s\n项目：%s\n构建分支： %s\n节点： %s\n发布完成" % (
                                    ReleaseUser, self.Env, self.ProjectName, ReleaseBranch, self.Host)
                                self.SendWebHookQYWX(message)
                                sys.exit(1)
                            if UrlStatus == "UP":
                                logs.log("获取eureka服务状态: status: %s" % (UrlStatus), self.ProjectName)
                                print("获取eureka服务状态: status: %s" % (UrlStatus))
                                message = "构建人员： %s\n环境： %s\n项目：%s\n构建分支： %s\n节点： %s\n发布完成" % (
                                    ReleaseUser, self.Env, self.ProjectName, ReleaseBranch, self.Host)
                                self.SendWebHookQYWX(message)
                                break
                            else:
                                logs.log("获取eureka服务状态: status: %s,触发脚本发送服务UP状态给Eureka" % (UrlStatus), self.ProjectName)
                                print("获取eureka服务状态: status: %s,触发脚本发送服务UP状态给Eureka" % (UrlStatus))
                                self.putEurekaStatusUP()
                                logs.log("获取eureka服务状态02: url: %s" % (CheckEurekaStatusUrl), self.ProjectName)
                                print("获取eureka服务状态02: url: %s" % (CheckEurekaStatusUrl))
                                time.sleep(2)
                                GetUrl = requests.get(CheckEurekaStatusUrl)
                                logs.log("获取eureka服务状态返回的内容02: %s" % (GetUrl.text), self.ProjectName)
                                UrlStatus = GetUrl.text.split('<status>')[1].split('</status>')[0]
                                if UrlStatus == "UP":
                                    logs.log("获取eureka服务状态02: status: %s" % (UrlStatus), self.ProjectName)
                                    print("获取eureka服务状态02: status: %s" % (UrlStatus))
                                    message = "构建人员： %s\n环境： %s\n项目：%s\n构建分支： %s\n节点： %s\n发布完成" % (
                                        ReleaseUser, self.Env, self.ProjectName, ReleaseBranch, self.Host)
                                    self.SendWebHookQYWX(message)
                                    break
                                else:
                                    logs.log("获取eureka服务状态02: status: %s" % (UrlStatus), self.ProjectName)
                                    print("获取eureka服务状态02: status: %s" % (UrlStatus))
                                    message = "构建人员： %s\n环境： %s\n项目：%s\n构建分支： %s\n节点： %s\n发布完成" % (
                                        ReleaseUser, self.Env, self.ProjectName, ReleaseBranch, self.Host)
                                    self.SendWebHookQYWX(message)
                                    sys.exit(1)
                        else:
                            break
                    else:
                        logs.log("接口监测失败: url: %s code: %s 请联系对应开发健康监测返回状态不为200" % (Url, Code.status_code),self.ProjectName)
                        print("接口监测失败: url: %s code: %s 请联系对应开发健康监测返回状态不为200" % (Url, Code.status_code))
                        logs.log("==================以下为服务启动最后100行日志==================", self.ProjectName)
                        print("==================以下为服务启动最后100行日志==================")
                        DockerLogsCmd = "docker logs --tail=100 %s-%s" % (self.Env,self.ProjectName)
                        self.Conn.ssh(DockerLogsCmd, self.ProjectName)
                        message = "构建人员： %s\n环境： %s\n项目：%s\n构建分支： %s\n节点： %s\n发布完成" % (
                            ReleaseUser, self.Env, self.ProjectName, ReleaseBranch, self.Host)
                        self.SendWebHookQYWX(message)
                        sys.exit(1)
                except requests.exceptions.ConnectionError:
                    if T == Time - 1:
                        logs.log("接口检测失败: url: %s status: 退出" % (Url),self.ProjectName)
                        print("接口检测失败: url: %s status: 退出" % (Url))
                        logs.log("==================以下为服务启动最后100行日志==================",self.ProjectName)
                        print("==================以下为服务启动最后100行日志==================")
                        DockerLogsCmd = "docker logs --tail=100 %s-%s" % (self.Env,self.ProjectName)
                        self.Conn.ssh(DockerLogsCmd, self.ProjectName)
                        message = "构建人员： %s\n环境： %s\n项目：%s\n构建分支： %s\n节点： %s\n发布完成" % (
                            ReleaseUser, self.Env, self.ProjectName, ReleaseBranch, self.Host)
                        self.SendWebHookQYWX(message)
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
                        message = "构建人员： %s\n环境： %s\n项目：%s\n构建分支： %s\n节点： %s\n发布完成" % (
                            ReleaseUser, self.Env, self.ProjectName, ReleaseBranch, self.Host)
                        self.SendWebHookQYWX(message)
                        logs.log("==================以下为服务启动最后100行日志==================",self.ProjectName)
                        print("==================以下为服务启动最后100行日志==================")
                        DockerLogsCmd = "docker logs --tail=100 %s-%s" % (self.Env,self.ProjectName)
                        self.Conn.ssh(DockerLogsCmd, self.ProjectName)
                        sys.exit(1)
                    else:
                        logs.log("接口监测: url: %s status: 服务正在启动" % (Url),self.ProjectName)
                        print("接口监测: url: %s status: 服务正在启动" % (Url))
                    continue

    def ifregistereureka(self):
        if self.ProjectName in ['activity-api-service', 'community-api-service', 'course-api-service',
                                'gateway-server', 'member-api-service', 'merchandise-api-service',
                                'message-consume-service', 'report-api-service', 'rest-api-service',
                                'soso-api-service']:
            self.RegisterEureka = "0"
        else:
            self.RegisterEureka = "1"

    def getserviceinip(self,Host):
        GetServerIPCmd = "cat /etc/hosts|grep %s|awk NR==1|awk '{print $1}'" % (Host)
        SystemOutput = os.popen(GetServerIPCmd)
        res = SystemOutput.read()
        SplitOut = res.splitlines()
        self.IP = SplitOut[0]
        logs.log("获取IP地址: Host: %s IP: %s" % (Host,self.IP), self.ProjectName)
        print("获取IP地址: Host: %s IP: %s" % (Host,self.IP))

    def ReloadTengine(self):
        if self.ReTengine == "1":
            print("开始修改tengine配置文件")
            TengineFileDir = "%s/%s-%s-%s.conf" % (self.TenDir,self.Env,self.Belong,self.ProjectName)
            file = open('/data/release/tengine/%s-%s-%s.conf' % (self.Env,self.Belong,self.ProjectName),'w')
            UpstreamSta = "upstream %s-%s-%s {\n" % (self.Env,self.Belong,self.ProjectName)
            file.write(UpstreamSta)
            for i in range(0,len(self.SouHost.split(":"))):
                Server = "        server %s:%s;\n" % (self.SouHost.split(":")[i],self.ProjectPort)
                file.write(Server)
            UpstreanEnd = "    }\n"
            file.write(UpstreanEnd)
            file.close()
            BackUpOldTengineFileCmd = "rm -rf %s.bak && mv %s %s.bak" % (TengineFileDir,TengineFileDir,TengineFileDir)
            for t in range(0,len(self.TengineNode.split(":"))):
                Conn = connectionHost(self.TengineNode.split(":")[t], self.UserName, self.Password, self.Port)
                UploadFileToHost = "scp -P %s /data/release/tengine/%s-%s-%s.conf %s:%s" % (self.Port,self.Env,
                                     self.Belong,self.ProjectName,self.TengineNode.split(":")[t],TengineFileDir)
                ReloadTengineCmd = "nginx -s reload"
                Conn.ssh(BackUpOldTengineFileCmd,self.ProjectName)
                self.toolsCmd(UploadFileToHost)
                if Conn.ssh(ReloadTengineCmd,self.ProjectName) == 1:
                    sys.exit(1)
            ResetValueIsZero = "update Ops_projectinfo set ReTengine = 0 where Project = '%s' " \
                               "and EnvPar = '%s' and Del = '0'" % (self.ProjectName,self.Env)
            self.ConDB.ConnDB(ResetValueIsZero, self.ProjectName)
            print("修改完成")
        else:
            print("不需要修改tengine配置")

    def ReNode(self):
        if self.OldNodeRm == "1":
            print("开始删除操作")
            for S in range(0,len(self.SouHost.split(":"))):
                if self.OldNode.split(":")[S] not in self.SouHost:
                    TempHost = self.OldNode.split(":")[S]
                    Conn = connectionHost(TempHost, self.UserName, self.Password, self.Port)
                    self.getserviceinip(TempHost)
                    self.putEurekaStatusDown()
                    RmOldContainerCmd = "docker stop %s && docker rm %s" % (self.ProjectName,self.ProjectName)
                    Conn.ssh(RmOldContainerCmd,self.ProjectName)
            ResetValueIsZero = "update Ops_projectinfo set OldNodeRm = 0 where Project = '%s' " \
                               "and EnvPar = '%s' and Del = '0'" % (self.ProjectName, self.Env)
            self.ConDB.ConnDB(ResetValueIsZero, self.ProjectName)
            print("删除完成")
        else:
            print("跳过删除节点")

    def main(self):
        self.SouHost = self.Host
        for H in self.Host.split(":"):
            self.ProjectName = ProjectName
            if Env != "prd":
                self.Port = 22
            else:
                self.Port = 39222
            self.Host = H
            self.getserviceinip(self.Host)
            self.ifregistereureka()
            if self.RegisterEureka == "0":
                if Env == "prd":
                    self.putEurekaStatusDown()
            self.Conn = connectionHost(H, self.UserName, self.Password,self.Port)
            self.ifPackJarWar()
            self.backup()
            self.upload()
            self.getIfResetContainer()
        self.ReloadTengine()
        self.ReNode()

    def rollbackMain(self):
        for H in self.Host.split(":"):
            if Env != "prd":
                self.Port = 22
            else:
                self.Port = 39222
            self.Host = H
            self.getserviceinip(self.Host)
            self.ifregistereureka()
            self.Conn = connectionHost(H, self.UserName, self.Password,self.Port)
            self.rollback()
            self.getIfResetContainer()

JenkinsJobName = sys.argv[1]
ProjectName = sys.argv[2]
Env = sys.argv[3]
ReleaseUser = sys.argv[4]
ReleaseBranch = sys.argv[5]
release = projectInfo(JenkinsJobName,ProjectName,Env)
if JenkinsJobName == "rollback":
    release.rollbackMain()
else:
    release.main()