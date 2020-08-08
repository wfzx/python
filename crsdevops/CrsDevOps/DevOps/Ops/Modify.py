from django.shortcuts import render,redirect
from django.contrib import messages
from Ops import models
from Ops.views import IsNullOrSpace
from login.admin import check_user
import time

# 修改服务相关配置
@check_user
def ModifyServer(request):
    username = request.session["login_user"]
    if request.method == 'POST':
        id = request.POST['id']
        ServerName = request.POST['ServerName']
        ServerMem = request.POST['ServerMem']
        ServerNode = request.POST['ServerNode']
        CheckOps = request.POST['CheckOps']
        ServerPort = request.POST['ServerPort']
        ServerType = request.POST['ServerType']
        ResetImages = request.POST['ResetImages']
        TenProxy = request.POST['TenProxy']
        ReTengine = request.POST['ReTengine']
        AddSkywalking = request.POST['AddSkywalking']
        Remarks = request.POST['Remarks']
        AddServerPath = '/ModifyServer?id=%s' % (id)
        # 判断参数是否有空值或包含空格
        for i in [ServerName,ServerMem, ServerNode, CheckOps, ServerPort, ServerType,Remarks,AddSkywalking]:
            if IsNullOrSpace(i) == 0:
                return redirect(AddServerPath, messages.error(request, "参数不得为空"))
            elif IsNullOrSpace(i) == 1:
                return redirect(AddServerPath, messages.error(request, "输入的内容不允许包含空格"))
        # 记录修改日志
        Date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        Env = models.ProjectInfo.objects.filter(id=id).values_list('EnvPar', flat=True).first()
        Belong = models.ProjectInfo.objects.filter(id=id).values_list('Belong', flat=True).first()
        if TenProxy == "1":
            Old_Node = models.ProjectInfo.objects.filter(id=id).values_list('Node',flat=True).first()
            Old_Port = models.ProjectInfo.objects.filter(id=id).values_list('Port',flat=True).first()
            if ServerNode == Old_Node:
                Node = 0
            else:
                Node = 1
            if ServerPort == Old_Port:
                Port = 0
            else:
                Port = 1
            if Node == Port:
                ReTengine = 0
            else:
                if ServerNode != Old_Node:
                    models.ProjectInfo.objects.filter(id=id).update(OldNode=Old_Node,OldNodeRm='1',OldPort=Old_Port)
                elif ServerPort != Old_Port:
                    models.ProjectInfo.objects.filter(id=id).update(OldNode=Old_Node,OldNodeRm='1',OldPort=Old_Port)
                ReTengine = 1
        models.ModifyServerLog.objects.create(Project=ServerName, MemSize=ServerMem, Node=ServerNode,EnvPar=Env,
                                           CheckOpsApi=CheckOps, Port=ServerPort, ServerType=ServerType,Belong=Belong,
                                           ReSet=ResetImages, ModifyTime=Date,Remarks=Remarks,ModifyUser=username
                                           ).save()
        models.ProjectInfo.objects.filter(id=id).update(Project=ServerName, MemSize=ServerMem, Node=ServerNode,
                                         CheckOpsApi=CheckOps, Port=ServerPort, ServerType=ServerType,Belong=Belong,
                                         ReSet=ResetImages, ModifyTime=Date,ReTengine=ReTengine,TenProxy=TenProxy,
                                                        AddSkywalking=AddSkywalking
                                         )
        return redirect(AddServerPath, messages.info(request, "%s服务修改成功" % ServerName))
    else:
        ModifyServerOut = {}
        id = request.GET['id']
        Project = models.ProjectInfo.objects.filter(id=id).values_list('Project', flat=True).first()
        Env = models.ProjectInfo.objects.filter(id=id).values_list('EnvPar', flat=True).first()
        Node = models.ProjectInfo.objects.filter(id=id).values_list('Node', flat=True).first()
        Port = models.ProjectInfo.objects.filter(id=id).values_list('Port', flat=True).first()
        MemSize = models.ProjectInfo.objects.filter(id=id).values_list('MemSize', flat=True).first()
        CheckOpsApi = models.ProjectInfo.objects.filter(id=id).values_list('CheckOpsApi', flat=True).first()
        ServerType = models.ProjectInfo.objects.filter(id=id).values_list('ServerType', flat=True).first()
        ReSet = models.ProjectInfo.objects.filter(id=id).values_list('ReSet', flat=True).first()
        TenProxy = models.ProjectInfo.objects.filter(id=id).values_list('TenProxy', flat=True).first()
        ReTengine = models.ProjectInfo.objects.filter(id=id).values_list('ReTengine', flat=True).first()
        Belong = models.ProjectInfo.objects.filter(id=id).values_list('Belong', flat=True).first()
        AddSkywalking = models.ProjectInfo.objects.filter(id=id).values_list('AddSkywalking', flat=True).first()
        ModifyServerOut[id] = [Project,Env,Node,Port,MemSize,CheckOpsApi,ServerType,ReSet,TenProxy,ReTengine,Belong,AddSkywalking]
        return render(request,"views/修改服务.html",{'list':ModifyServerOut})

# 修改环境相关配置
@check_user
def ModifyEnv(request):
    username = request.session["login_user"]
    if request.method == 'POST':
        id = request.POST['id']
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
        Remarks = request.POST['Remarks']
        JavaStartPar = request.POST['JavaStartPar']
        SkywalkingAddress = request.POST['SkywalkingAddress']
        AddEnvPath = '/ModifyEnv?id=%s' % (id)
        # 判断参数是否有空值或包含空格
        for i in [ServerUser, ServerPass, RepoAddress, RepoUser, RepoPass, JenkinsDir, RootDir, BackupDir,
                  EurekaAddress, Hosts,Remarks,TenDir,JavaStartPar,SkywalkingAddress]:
            if IsNullOrSpace(i) == 0:
                return redirect(AddEnvPath, messages.error(request, "参数不得为空"))
        EnvPar = models.EnvInfo.objects.filter(id=id).values_list('EnvPar').first()
        # 记录修改日志
        Date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        models.ModifyEnvLog.objects.create(EnvPar=EnvPar, ServerUser=ServerUser, ServerPass=ServerPass,
                                           RepoAddress=RepoAddress,RepoUser=RepoUser, RepoPass=RepoPass,RootDir=RootDir,
                                           JenkinsDir=JenkinsDir,BackupDir=BackupDir,ModifyUser=username,
                                           EurekaAddress=EurekaAddress,Hosts=Hosts,Remarks=Remarks,ModifyTime=Date
                                           ).save()
        models.EnvInfo.objects.filter(id=id).update(ServerUser=ServerUser, ServerPass=ServerPass,JavaStartPar=JavaStartPar,
                                      RepoAddress=RepoAddress,RepoUser=RepoUser, RepoPass=RepoPass,SkywalkingAddress=SkywalkingAddress,
                                      JenkinsDir=JenkinsDir, RootDir=RootDir,BackupDir=BackupDir,
                                      EurekaAddress=EurekaAddress, Hosts=Hosts,ModifyTime=Date,TenDir=TenDir
                                                    )
        return redirect(AddEnvPath, messages.info(request, "%s环境修改成功" % EnvPar))
    else:
        ModifyEnvOut = {}
        id = request.GET['id']
        Env = models.EnvInfo.objects.filter(id=id).values_list('EnvPar', flat=True).first()
        ServerUser = models.EnvInfo.objects.filter(id=id).values_list('ServerUser', flat=True).first()
        ServerPass = models.EnvInfo.objects.filter(id=id).values_list('ServerPass', flat=True).first()
        RepoAddress = models.EnvInfo.objects.filter(id=id).values_list('RepoAddress', flat=True).first()
        RepoUser = models.EnvInfo.objects.filter(id=id).values_list('RepoUser', flat=True).first()
        RepoPass = models.EnvInfo.objects.filter(id=id).values_list('RepoPass', flat=True).first()
        JenkinsDir = models.EnvInfo.objects.filter(id=id).values_list('JenkinsDir', flat=True).first()
        RootDir = models.EnvInfo.objects.filter(id=id).values_list('RootDir', flat=True).first()
        BackupDir = models.EnvInfo.objects.filter(id=id).values_list('BackupDir', flat=True).first()
        EurekaAddress = models.EnvInfo.objects.filter(id=id).values_list('EurekaAddress', flat=True).first()
        Hosts = models.EnvInfo.objects.filter(id=id).values_list('Hosts', flat=True).first()
        TenDir = models.EnvInfo.objects.filter(id=id).values_list('TenDir', flat=True).first()
        JavaStartPar = models.EnvInfo.objects.filter(id=id).values_list('JavaStartPar', flat=True).first()
        SkywalkingAddress = models.EnvInfo.objects.filter(id=id).values_list('SkywalkingAddress', flat=True).first()
        ModifyEnvOut[Env] = [id, ServerUser, ServerPass, RepoAddress, RepoUser, RepoPass, JenkinsDir, RootDir,
                           BackupDir, EurekaAddress, Hosts,TenDir,JavaStartPar,SkywalkingAddress
                           ]
        return render(request,'views/修改环境.html',{'list':ModifyEnvOut})

# 修改连接环境相关配置
@check_user
def ModifyEnvConn(request):
    username = request.session["login_user"]
    if request.method == 'POST':
        id = request.POST['id']
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
        AddEnvConnPath = '/ModifyEnvConn?id=%s' % (id)
        # 判断参数是否有空值或包含空格
        for i in [KafkaInt,KafkaExt,HbaseInt,HbaseExt,HbaseUser,HbasePass,MysqlInt,MysqlExt
            ,MysqlUser,MysqlPass,RedisInt,RedisExt,RedisPass]:
            if IsNullOrSpace(i) == 0:
                return redirect(AddEnvConnPath, messages.error(request, "参数不得为空"))
        EnvPar = models.EnvConnInfo.objects.filter(id=id).values_list('EnvPar').first()
        # 记录修改日志
        Date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        models.ModifyEnvConnLog.objects.create(EnvPar=EnvPar, KafkaInt=KafkaInt, KafkaExt=KafkaExt,HbaseInt=HbaseInt,
                                        HbaseExt=HbaseExt,HbaseUser=HbaseUser,HbasePass=HbasePass, MysqlInt=MysqlInt,
                                        MysqlExt=MysqlExt,MysqlUser=MysqlUser,MysqlPass=MysqlPass,ModifyUser=username,
                                        RedisInt=RedisInt,RedisExt=RedisExt,RedisPass=RedisPass,ModifyTime=Date
                                           ).save()
        models.EnvConnInfo.objects.filter(id=id).update(KafkaInt=KafkaInt, KafkaExt=KafkaExt,HbaseInt=HbaseInt,
                                        HbaseExt=HbaseExt,HbaseUser=HbaseUser,HbasePass=HbasePass, MysqlInt=MysqlInt,
                                        MysqlExt=MysqlExt,MysqlUser=MysqlUser,MysqlPass=MysqlPass,
                                        RedisInt=RedisInt,RedisExt=RedisExt,RedisPass=RedisPass,ModifyTime=Date
                                                    )
        return redirect(AddEnvConnPath, messages.info(request, "%s环境修改成功" % EnvPar))
    else:
        ModifyEnvConnOut = {}
        id = request.GET['id']
        Env = models.EnvConnInfo.objects.filter(id=id).values_list('EnvPar', flat=True).first()
        KafkaInt = models.EnvConnInfo.objects.filter(id=id).values_list('KafkaInt', flat=True).first()
        KafkaExt = models.EnvConnInfo.objects.filter(id=id).values_list('KafkaExt', flat=True).first()
        HbaseInt = models.EnvConnInfo.objects.filter(id=id).values_list('HbaseInt', flat=True).first()
        HbaseExt = models.EnvConnInfo.objects.filter(id=id).values_list('HbaseExt', flat=True).first()
        HbaseUser = models.EnvConnInfo.objects.filter(id=id).values_list('HbaseUser', flat=True).first()
        HbasePass = models.EnvConnInfo.objects.filter(id=id).values_list('HbasePass', flat=True).first()
        MysqlInt = models.EnvConnInfo.objects.filter(id=id).values_list('MysqlInt', flat=True).first()
        MysqlExt = models.EnvConnInfo.objects.filter(id=id).values_list('MysqlExt', flat=True).first()
        MysqlUser = models.EnvConnInfo.objects.filter(id=id).values_list('MysqlUser', flat=True).first()
        MysqlPass = models.EnvConnInfo.objects.filter(id=id).values_list('MysqlPass', flat=True).first()
        RedisInt = models.EnvConnInfo.objects.filter(id=id).values_list('RedisInt', flat=True).first()
        RedisExt = models.EnvConnInfo.objects.filter(id=id).values_list('RedisExt', flat=True).first()
        RedisPass = models.EnvConnInfo.objects.filter(id=id).values_list('RedisPass', flat=True).first()
        ModifyEnvConnOut[Env] = [id, KafkaInt, KafkaExt, HbaseInt, HbaseExt, HbaseUser, HbasePass, MysqlInt,
                           MysqlExt, MysqlUser, MysqlPass,RedisInt,RedisExt,RedisPass
                           ]
        return render(request,'views/修改连接环境.html',{'list':ModifyEnvConnOut})