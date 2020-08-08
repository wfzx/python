from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Count
from Ops import models
from Ops.views import IsNullOrSpace
from login.admin import check_user
import time

# 添加服务
@check_user
def AddServer(request):
    if request.method == 'POST':
        ServerName = request.POST['ServerName']
        ServerMem = request.POST['ServerMem']
        ServerNode = request.POST['ServerNode']
        CheckOps = request.POST['CheckOps']
        ServerType = request.POST['ServerType']
        ResetImages = request.POST['ResetImages']
        Remarks = request.POST['Remarks']
        TenProxy = request.POST['TenProxy']
        BelongEnv = request.POST['Env']
        Belong = request.POST['Belong']
        AddSkywalking = request.POST['AddSkywalking']
        AddServerPath = '/AddServer'
        # 判断参数是否有空值或包含空格
        for i in [ServerName,ServerMem,ServerNode,CheckOps,ServerType,Remarks,BelongEnv,Belong,AddSkywalking]:
            if IsNullOrSpace(i) == 0:
                return redirect(AddServerPath, messages.error(request, "参数不得为空"))
            elif IsNullOrSpace(i) == 1:
                return redirect(AddServerPath, messages.error(request, "输入的内容不允许包含空格"))
        # 判断添加的服务是否已经存在
        IsExits = models.ProjectInfo.objects.filter(Project=ServerName,EnvPar=BelongEnv,Belong=Belong)
        if IsExits:
            return redirect(AddServerPath, messages.info(request, "%s服务在%s环境中已存在，请不要重复创建" % (ServerName,BelongEnv)))
        else:
            # 记录添加日志
            Date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            ReTengine = TenProxy
            models.AddServerLog.objects.create(Project=ServerName, MemSize=ServerMem, Node=ServerNode,
                                             CheckOpsApi=CheckOps, Port='1', ServerType=ServerType,
                                             ReSet=ResetImages,CreateTime=Date,Remarks=Remarks,Belong=Belong
                                             ).save()
            models.ProjectInfo.objects.create(Project=ServerName,EnvPar=BelongEnv,Node=ServerNode,Port='1',Belong=Belong,
                                             MemSize=ServerMem,CheckOpsApi=CheckOps, ServerType=ServerType,ReTengine=ReTengine,
                                             ReSet=ResetImages,ModifyTime=Date,CreateTime=Date,Del=0,TenProxy=TenProxy,
                                              ProjectStatus='DOWN',AddSkywalking=AddSkywalking
                                             ).save()
            Pid = models.ProjectInfo.objects.filter(Project=ServerName,EnvPar=BelongEnv).values_list('id',flat=True).first()
            if len(str(Pid)) == 1:
                Port = "200%s" % Pid
            elif len(str(Pid)) == 2:
                Port = "20%s" % Pid
            elif len(str(Pid)) == 3:
                Port = "2%s" % Pid
            else:
                Port = Pid
            models.ProjectInfo.objects.filter(id=Pid).update(Port=Port)
            return redirect(AddServerPath, messages.info(request, "%s服务在%s环境中添加成功" % (ServerName,BelongEnv)))
    else:

        IfEnvNull = models.EnvInfo.objects.values_list('id').first()
        if IfEnvNull == None:
            return redirect('/ProjectInfo',messages.error(request,"请先添加环境信息，在查看服务信息"))
        EnvListOut = {}
        for t in range(0, len(models.EnvInfo.objects.values_list('id', flat=True))):
            id = models.EnvInfo.objects.values_list('id', flat=True)[t]
            EnvList = models.EnvInfo.objects.filter(id=id).values_list('EnvPar', flat=True).first()
            EnvListOut[EnvList] = [id, EnvList]
        ProjectGroup = {}
        for P in range(0,len(models.ProjectInfo.objects.values('Belong').annotate(Count('Belong')))):
            ProjectGroupName = models.ProjectInfo.objects.values('Belong').annotate(Count('Belong'))[P]['Belong']
            ProjectGroup[ProjectGroupName] = [ProjectGroupName]
        return render(request,'views/添加服务.html',{'EnvList': EnvListOut,'ProjectGroup':ProjectGroup})

# 添加环境q
@check_user
def AddEnv(request):
    if request.method == 'POST':
        EnvPar = request.POST['EnvPar']
        ServerUser = request.POST['ServerUser']
        ServerPass = request.POST['ServerPass']
        RepoAddress = request.POST['RepoAddress']
        RepoUser = request.POST['RepoUser']
        RepoPass = request.POST['RepoPass']
        JenkinsDir = request.POST['JenkinsDir']
        RootDir = request.POST['RootDir']
        BackupDir = request.POST['BackupDir']
        EurekaAddress = request.POST['EurekaAddress']
        Hosts = request.POST['Hosts']
        TenDir = request.POST['TenDir']
        JavaStartPar = request.POST['JavaStartPar']
        SkywalkingAddress = request.POST['SkywalkingAddress']
        AddEnvPath = '/AddEnv'
        # 判断参数是否有空值或包含空格
        for i in [EnvPar,ServerUser,ServerPass,RepoAddress,RepoUser,RepoPass,JenkinsDir
            ,RootDir,BackupDir,EurekaAddress,Hosts,TenDir,JavaStartPar,SkywalkingAddress]:
            if IsNullOrSpace(i) == 0:
                return redirect(AddEnvPath, messages.error(request, "参数不得为空"))
        # 记录修改日志
        Date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        models.AddEnvLog.objects.create(EnvPar=EnvPar, ServerUser=ServerUser, ServerPass=ServerPass,
                                        RepoAddress=RepoAddress,RepoUser=RepoUser, RepoPass=RepoPass,
                                        JenkinsDir=JenkinsDir,RootDir=RootDir,BackupDir=BackupDir,
                                        EurekaAddress=EurekaAddress,Hosts=Hosts,CreateTime=Date
                                        ).save()
        models.EnvInfo.objects.create(EnvPar=EnvPar, ServerUser=ServerUser, ServerPass=ServerPass,JavaStartPar=JavaStartPar,
                                      RepoAddress=RepoAddress,RepoUser=RepoUser, RepoPass=RepoPass,SkywalkingAddress=SkywalkingAddress,
                                      JenkinsDir=JenkinsDir, RootDir=RootDir,BackupDir=BackupDir,TenDir=TenDir,
                                      EurekaAddress=EurekaAddress, Hosts=Hosts,ModifyTime=Date,CreateTime=Date
                                      ).save()
        return redirect(AddEnvPath, messages.info(request, "%s环境添加成功" % EnvPar))
    else:
        return render(request,'views/添加环境.html')

# 添加环境
@check_user
def AddEnvConn(request):
    if request.method == 'POST':
        EnvPar = request.POST['EnvPar']
        KafkaInt = request.POST['KafkaInt']
        KafkaExt = request.POST['KafkaExt']
        HbaseInt = request.POST['HbaseInt']
        HbaseExt = request.POST['HbaseExt']
        HbaseUser = request.POST['HbaseUser']
        HbasePass = request.POST['HbasePass']
        MysqlInt = request.POST['MysqlInt']
        MysqlExt = request.POST['MysqlExt']
        MysqlUser = request.POST['MysqlUser']
        MysqlPass = request.POST['MysqlPass']
        RedisInt = request.POST['RedisInt']
        RedisExt = request.POST['RedisExt']
        RedisPass = request.POST['RedisPass']
        AddEnvPath = '/AddEnvConn'
        # 判断参数是否有空值或包含空格
        for i in [EnvPar,KafkaInt,KafkaExt,HbaseInt,HbaseExt,HbaseUser,HbasePass,MysqlInt,MysqlExt
            ,MysqlUser,MysqlPass,RedisInt,RedisExt,RedisPass]:
            if IsNullOrSpace(i) == 0:
                return redirect(AddEnvPath, messages.error(request, "参数不得为空"))
        # 记录修改日志
        Date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        models.AddEnvConnLog.objects.create(EnvPar=EnvPar, KafkaInt=KafkaInt, KafkaExt=KafkaExt,HbaseInt=HbaseInt,
                                        HbaseExt=HbaseExt,HbaseUser=HbaseUser,HbasePass=HbasePass, MysqlInt=MysqlInt,
                                        MysqlExt=MysqlExt,MysqlUser=MysqlUser,MysqlPass=MysqlPass,
                                        RedisInt=RedisInt,RedisExt=RedisExt,RedisPass=RedisPass,CreateTime=Date
                                        ).save()
        models.EnvConnInfo.objects.create(EnvPar=EnvPar, KafkaInt=KafkaInt, KafkaExt=KafkaExt,HbaseInt=HbaseInt,
                                        HbaseExt=HbaseExt,HbaseUser=HbaseUser,HbasePass=HbasePass, MysqlInt=MysqlInt,
                                        MysqlExt=MysqlExt,MysqlUser=MysqlUser,MysqlPass=MysqlPass,ModifyTime=Date,
                                        RedisInt=RedisInt,RedisExt=RedisExt,RedisPass=RedisPass,CreateTime=Date
                                      ).save()
        return redirect(AddEnvPath, messages.info(request, "%s环境添加成功" % EnvPar))
    else:
        return render(request,'views/添加连接环境.html')