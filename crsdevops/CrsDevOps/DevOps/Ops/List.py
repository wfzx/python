from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Count
from Ops import models
from login import models as ls
from login.admin import check_user

# 服务清单
@check_user
def ProjectInfo(request):
    username = request.session["login_user"]
    IfAdmin = ls.User.objects.filter(name=username).values_list('admin', flat=True).first()
    if request.method == 'POST':
        Env = request.POST['Env']
        ProjectGroupName = request.POST['ProjectGroupName']
        ServerListOut = {}
        EnvListOut = {}
        ProjectGroup = {}
        IfEnvValue = models.ProjectInfo.objects.filter(EnvPar=Env).first()
        if IfEnvValue == None:
            return redirect('/ProjectInfo',messages.error(request,'%s环境没有相关服务' % (Env)))
        for t in range(0, len(models.EnvInfo.objects.values_list('id', flat=True))):
            if t == 0:
                id = models.EnvInfo.objects.filter(EnvPar=Env).values_list('id',flat=True).first()
                EnvList = Env
                oneid = id
            else:
                id = models.EnvInfo.objects.values_list('id', flat=True)[t]
                if id == oneid:
                    id = 1
                EnvList = models.EnvInfo.objects.filter(id=id).values_list('EnvPar', flat=True).first()
            EnvListOut[EnvList] = [id, EnvList]
        # 组别
        for P in range(0,len(models.ProjectInfo.objects.values('Belong').annotate(Count('Belong')))):
            ProjectGroupNameInDB = models.ProjectInfo.objects.values('Belong').annotate(Count('Belong'))[P][
                'Belong']
            ProjectGroup[P] = [ProjectGroupNameInDB]
        if ProjectGroupName == 'IOT':
            ProjectGroup[1] = ['PT']
        elif ProjectGroupName == 'MFT':
            ProjectGroup[2] = ['PT']
        ProjectGroup[0] = [ProjectGroupName]
        # 搜索
        if request.POST['grep'] != '':
            Grep = request.POST['grep']
            Del = request.POST['Del']
            IfGrepDB = models.ProjectInfo.objects.filter(EnvPar=Env, Del=Del, Belong=ProjectGroupName, Project__contains=Grep).exists()
            if IfGrepDB:
                for i in range(0,len(models.ProjectInfo.objects.filter(EnvPar=Env, Del=Del, Belong=ProjectGroupName, Project__contains=Grep))):
                    Project = models.ProjectInfo.objects.filter(EnvPar=Env, Del=Del, Belong=ProjectGroupName, Project__contains=Grep)[i]
                    id = models.ProjectInfo.objects.filter(EnvPar=Env, Del=Del, Belong=ProjectGroupName, Project__contains=Grep).values_list('id')[i][0]
                    Node = models.ProjectInfo.objects.filter(id=id).values_list('Node', flat=True).first()
                    Port = models.ProjectInfo.objects.filter(id=id).values_list('Port', flat=True).first()
                    MemSize = models.ProjectInfo.objects.filter(id=id).values_list('MemSize', flat=True).first()
                    CheckOpsApi = models.ProjectInfo.objects.filter(id=id).values_list('CheckOpsApi', flat=True).first()
                    ServerType = models.ProjectInfo.objects.filter(id=id).values_list('ServerType', flat=True).first()
                    ReSet = models.ProjectInfo.objects.filter(id=id).values_list('ReSet', flat=True).first()
                    TenProxy = models.ProjectInfo.objects.filter(id=id).values_list('TenProxy', flat=True).first()
                    ReTengine = models.ProjectInfo.objects.filter(id=id).values_list('ReTengine', flat=True).first()
                    Belong = models.ProjectInfo.objects.filter(id=id).values_list('Belong', flat=True).first()
                    ReleaseTime = models.ProjectInfo.objects.filter(id=id).values_list('ReleaseTime', flat=True).first()
                    Status = models.ProjectInfo.objects.filter(id=id).values_list('ProjectStatus', flat=True).first()
                    AddSkywalking = models.ProjectInfo.objects.filter(id=id).values_list('AddSkywalking', flat=True).first()
                    if 'DOWN' in str(Status):
                        ProjectStatus = '0'
                    else:
                        ProjectStatus = '1'
                    ServerListOut[id] = [Project, Env, Node, Port, MemSize, CheckOpsApi,
                                         ServerType, ReSet,TenProxy,ReTengine,ProjectStatus,
                                         Status,Belong,ReleaseTime,AddSkywalking]
                return render(request, "views/服务清单.html", {'list': ServerListOut, 'EnvList': EnvListOut,
                                                           'IfAdmin': IfAdmin, 'Grep': Grep,'Del':Del,
                                                           'ProjectGroup':ProjectGroup})
            else:
                return redirect("/ProjectInfo")
        # 搜索内容为空，按项目组搜索
        else:
            Grep = ''
            Del = request.POST['Del']
            for i in range(0,len(models.ProjectInfo.objects.filter(EnvPar=Env, Belong=ProjectGroupName, Del=Del).values_list('id',flat=True))):
                id = models.ProjectInfo.objects.filter(EnvPar=Env, Belong=ProjectGroupName, Del=Del).values_list('id',flat=True)[i]
                Project = models.ProjectInfo.objects.filter(id=id).values_list('Project', flat=True).first()
                Node = models.ProjectInfo.objects.filter(id=id).values_list('Node', flat=True).first()
                Port = models.ProjectInfo.objects.filter(id=id).values_list('Port', flat=True).first()
                MemSize = models.ProjectInfo.objects.filter(id=id).values_list('MemSize', flat=True).first()
                CheckOpsApi = models.ProjectInfo.objects.filter(id=id).values_list('CheckOpsApi', flat=True).first()
                ServerType = models.ProjectInfo.objects.filter(id=id).values_list('ServerType', flat=True).first()
                ReSet = models.ProjectInfo.objects.filter(id=id).values_list('ReSet', flat=True).first()
                TenProxy = models.ProjectInfo.objects.filter(id=id).values_list('TenProxy', flat=True).first()
                ReTengine = models.ProjectInfo.objects.filter(id=id).values_list('ReTengine', flat=True).first()
                Belong = models.ProjectInfo.objects.filter(id=id).values_list('Belong', flat=True).first()
                ReleaseTime = models.ProjectInfo.objects.filter(id=id).values_list('ReleaseTime', flat=True).first()
                Status = models.ProjectInfo.objects.filter(id=id).values_list('ProjectStatus', flat=True).first()
                AddSkywalking = models.ProjectInfo.objects.filter(id=id).values_list('AddSkywalking', flat=True).first()
                if 'DOWN' in str(Status):
                    ProjectStatus = '0'
                else:
                    ProjectStatus = '1'
                ServerListOut[id] = [Project,Env,Node,Port,MemSize,CheckOpsApi,
                                     ServerType,ReSet,TenProxy,ReTengine,ProjectStatus,
                                     Status,Belong,ReleaseTime,AddSkywalking]
        return render(request,"views/服务清单.html",{'list':ServerListOut,'EnvList':EnvListOut,
                                                 'IfAdmin': IfAdmin,'Grep': Grep,'Del':Del,'ProjectGroup':ProjectGroup})
    #请求不为POST
    else:
        IfEnvNull = models.EnvInfo.objects.values_list('id').first()
        if IfEnvNull == None:
            return redirect('/', messages.error(request, "请先添加环境信息，在查看服务信息"))
        ServerListOut = {}
        EnvListOut = {}
        ProjectGroup = {}
        Env = 'test'
        Del = '0'
        for i in range(0,len(models.ProjectInfo.objects.filter(EnvPar=Env, Del=0).values_list('id',flat=True))):
            id = models.ProjectInfo.objects.filter(EnvPar=Env, Del=0).values_list('id',flat=True)[i]
            Project = models.ProjectInfo.objects.filter(id=id).values_list('Project', flat=True).first()
            Node = models.ProjectInfo.objects.filter(id=id).values_list('Node', flat=True).first()
            Port = models.ProjectInfo.objects.filter(id=id).values_list('Port', flat=True).first()
            MemSize = models.ProjectInfo.objects.filter(id=id).values_list('MemSize', flat=True).first()
            CheckOpsApi = models.ProjectInfo.objects.filter(id=id).values_list('CheckOpsApi', flat=True).first()
            ServerType = models.ProjectInfo.objects.filter(id=id).values_list('ServerType', flat=True).first()
            ReSet = models.ProjectInfo.objects.filter(id=id).values_list('ReSet', flat=True).first()
            TenProxy = models.ProjectInfo.objects.filter(id=id).values_list('TenProxy', flat=True).first()
            ReTengine = models.ProjectInfo.objects.filter(id=id).values_list('ReTengine', flat=True).first()
            Belong = models.ProjectInfo.objects.filter(id=id).values_list('Belong', flat=True).first()
            ReleaseTime = models.ProjectInfo.objects.filter(id=id).values_list('ReleaseTime', flat=True).first()
            Status = models.ProjectInfo.objects.filter(id=id).values_list('ProjectStatus',flat=True).first()
            AddSkywalking = models.ProjectInfo.objects.filter(id=id).values_list('AddSkywalking',flat=True).first()
            if 'DOWN' in str(Status):
                ProjectStatus = '0'
            else:
                ProjectStatus = '1'
            ServerListOut[id] = [Project,Env,Node,Port,MemSize,CheckOpsApi
                ,ServerType,ReSet,TenProxy,ReTengine,ProjectStatus,Status,Belong,ReleaseTime,AddSkywalking]
        for t in range(0,len(models.EnvInfo.objects.values_list('id', flat=True))):
            id =  models.EnvInfo.objects.values_list('id', flat=True)[t]
            EnvList = models.EnvInfo.objects.filter(id=id).values_list('EnvPar', flat=True).first()
            EnvListOut[EnvList] = [id,EnvList]
        # 组别
        for P in range(0, len(models.ProjectInfo.objects.values('Belong').annotate(Count('Belong')))):
            ProjectGroupName = models.ProjectInfo.objects.values('Belong').annotate(Count('Belong'))[P]['Belong']
            ProjectGroup[P] = [ProjectGroupName]
        return render(request,"views/服务清单.html",{'list':ServerListOut,
                                                 'EnvList':EnvListOut,"IfAdmin": IfAdmin,'Del':Del,'ProjectGroup':ProjectGroup})

# 环境清单
@check_user
def EnvList(request):
    username = request.session["login_user"]
    IfAdmin = ls.User.objects.filter(name=username).values_list('admin', flat=True).first()
    if request.method == 'POST':
        Env = request.POST['Env']
        EnvListOut = {}
        EnvBodyOut = {}
        IfEnvValue = models.EnvInfo.objects.filter(EnvPar=Env).first()
        if IfEnvValue == None:
            return redirect('/ProjectInfo',messages.error(request,'%s环境没有相关服务' % (Env)))
        for t in range(0, len(models.EnvInfo.objects.values_list('id', flat=True))):
            if t == 0:
                id = models.EnvInfo.objects.filter(EnvPar=Env).values_list('id',flat=True).first()
                EnvList = models.EnvInfo.objects.filter(id=id).values_list('EnvPar', flat=True).first()
                oneid = id
            else:
                id = models.EnvInfo.objects.values_list('id', flat=True)[t]
                if id == oneid:
                    id = 1
                EnvList = models.EnvInfo.objects.filter(id=id).values_list('EnvPar', flat=True).first()
            EnvListOut[EnvList] = [id, EnvList]
        id = models.EnvInfo.objects.filter(EnvPar=Env).values_list('id', flat=True).first()
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
        CreateTime = models.EnvInfo.objects.filter(id=id).values_list('CreateTime', flat=True).first()
        JavaStartPar = models.EnvInfo.objects.filter(id=id).values_list('JavaStartPar', flat=True).first()
        SkywalkingAddress = models.EnvInfo.objects.filter(id=id).values_list('SkywalkingAddress', flat=True).first()
        EnvBodyOut[Env] = [id, ServerUser, ServerPass, RepoAddress, RepoUser, RepoPass, JenkinsDir, RootDir,
                               BackupDir, EurekaAddress, Hosts, CreateTime,TenDir,JavaStartPar,SkywalkingAddress
                               ]
        return render(request, "views/环境清单.html", {'list': EnvBodyOut, "IfAdmin": IfAdmin, 'EnvList': EnvListOut})
    else:
        EnvListOut = {}
        EnvBodyOut = {}
        Env = 'test'
        for t in range(0, len(models.EnvInfo.objects.values_list('id', flat=True))):
            id = models.EnvInfo.objects.values_list('id', flat=True)[t]
            EnvList = models.EnvInfo.objects.filter(id=id).values_list('EnvPar', flat=True).first()
            EnvListOut[EnvList] = [id, EnvList]
        id = models.EnvInfo.objects.filter(EnvPar=Env).values_list('id', flat=True).first()
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
        CreateTime = models.EnvInfo.objects.filter(id=id).values_list('CreateTime', flat=True).first()
        JavaStartPar = models.EnvInfo.objects.filter(id=id).values_list('JavaStartPar', flat=True).first()
        SkywalkingAddress = models.EnvInfo.objects.filter(id=id).values_list('SkywalkingAddress', flat=True).first()
        EnvBodyOut[Env] = [id, ServerUser, ServerPass, RepoAddress, RepoUser, RepoPass, JenkinsDir, RootDir,
                               BackupDir, EurekaAddress, Hosts, CreateTime,TenDir,JavaStartPar,SkywalkingAddress
                               ]
        return render(request,"views/环境清单.html",{'list':EnvBodyOut,"IfAdmin": IfAdmin,'EnvList':EnvListOut})

# 环境连接信息
@check_user
def EnvConnList(request):
    username = request.session["login_user"]
    IfAdmin = ls.User.objects.filter(name=username).values_list('admin', flat=True).first()
    if request.method == 'POST':
        Env = request.POST['Env']
        EnvConnListOut = {}
        EnvConnBodyOut = {}
        IfEnvValue = models.EnvConnInfo.objects.filter(EnvPar=Env).first()
        if IfEnvValue == None:
            return redirect('/ProjectInfo', messages.error(request, '%s环境没有相关服务' % (Env)))
        for t in range(0, len(models.EnvConnInfo.objects.values_list('id', flat=True))):
            if t == 0:
                id = models.EnvConnInfo.objects.filter(EnvPar=Env).values_list('id',flat=True).first()
                EnvList = models.EnvConnInfo.objects.filter(id=id).values_list('EnvPar', flat=True).first()
                oneid = id
            else:
                id = models.EnvConnInfo.objects.values_list('id', flat=True)[t]
                if id == oneid:
                    id = 1
                EnvList = models.EnvConnInfo.objects.filter(id=id).values_list('EnvPar', flat=True).first()
            EnvConnListOut[EnvList] = [id, EnvList]
        id = models.EnvConnInfo.objects.filter(EnvPar=Env).values_list('id', flat=True).first()
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
        ModifyTime = models.EnvConnInfo.objects.filter(id=id).values_list('ModifyTime', flat=True).first()
        EnvConnBodyOut[Env] = [id, KafkaInt, KafkaExt, HbaseInt, HbaseExt, HbaseUser, HbasePass, MysqlInt,
                           MysqlExt, MysqlUser, MysqlPass, ModifyTime, RedisInt,RedisExt,RedisPass
                           ]
        return render(request, "views/环境连接清单.html", {'list': EnvConnBodyOut, "IfAdmin": IfAdmin, 'EnvList': EnvConnListOut})
    # 请求不是POST
    else:
        EnvConnListOut = {}
        EnvConnBodyOut = {}
        Env = 'test'
        for t in range(0, len(models.EnvConnInfo.objects.values_list('id', flat=True))):
            id = models.EnvConnInfo.objects.values_list('id', flat=True)[t]
            EnvList = models.EnvConnInfo.objects.filter(id=id).values_list('EnvPar', flat=True).first()
            EnvConnListOut[EnvList] = [id, EnvList]
        id = models.EnvConnInfo.objects.filter(EnvPar=Env).values_list('id', flat=True).first()
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
        ModifyTime = models.EnvConnInfo.objects.filter(id=id).values_list('ModifyTime', flat=True).first()
        EnvConnBodyOut[Env] = [id, KafkaInt, KafkaExt, HbaseInt, HbaseExt, HbaseUser, HbasePass, MysqlInt,
                               MysqlExt, MysqlUser, MysqlPass, ModifyTime, RedisInt, RedisExt, RedisPass
                               ]
        return render(request,"views/环境连接清单.html",{'list':EnvConnBodyOut,"IfAdmin": IfAdmin,'EnvList':EnvConnListOut})