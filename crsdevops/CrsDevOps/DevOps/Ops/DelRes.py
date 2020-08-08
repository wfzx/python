from django.shortcuts import redirect
from django.contrib import messages
from login.admin import check_user
from Ops.views import IsNullOrSpace
from Ops import models
import time

@check_user
def Delete(request):
    username = request.session["login_user"]
    Id = request.GET['id']
    Project = models.ProjectInfo.objects.filter(id=Id).values_list('Project', flat=True).first()
    Env = models.ProjectInfo.objects.filter(id=Id).values_list('EnvPar', flat=True).first()
    Node = models.ProjectInfo.objects.filter(id=Id).values_list('Node', flat=True).first()
    Port = models.ProjectInfo.objects.filter(id=Id).values_list('Port', flat=True).first()
    MemSize = models.ProjectInfo.objects.filter(id=Id).values_list('MemSize', flat=True).first()
    CheckOpsApi = models.ProjectInfo.objects.filter(id=Id).values_list('CheckOpsApi', flat=True).first()
    ServerType = models.ProjectInfo.objects.filter(id=Id).values_list('ServerType', flat=True).first()
    ReSet = models.ProjectInfo.objects.filter(id=Id).values_list('ReSet', flat=True).first()
    DeletePath = "/"
    if IsNullOrSpace(Id) == 0:
        return redirect(DeletePath, messages.error(request, "删除失败"))
    Date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    models.ModifyServerLog.objects.create(Project=Project, MemSize=MemSize, Node=Node,EnvPar=Env,
                                           CheckOpsApi=CheckOpsApi, Port=Port, ServerType=ServerType,
                                           ReSet=ReSet, ModifyTime=Date,Remarks='null',ModifyUser=username
                                           ).save()
    models.ProjectInfo.objects.filter(id=Id).update(Del=1)
    return redirect('/ProjectInfo')

@check_user
def Restore(request):
    username = request.session["login_user"]
    Id = request.GET['id']
    Project = models.ProjectInfo.objects.filter(id=Id).values_list('Project', flat=True).first()
    Env = models.ProjectInfo.objects.filter(id=Id).values_list('EnvPar', flat=True).first()
    Node = models.ProjectInfo.objects.filter(id=Id).values_list('Node', flat=True).first()
    Port = models.ProjectInfo.objects.filter(id=Id).values_list('Port', flat=True).first()
    MemSize = models.ProjectInfo.objects.filter(id=Id).values_list('MemSize', flat=True).first()
    CheckOpsApi = models.ProjectInfo.objects.filter(id=Id).values_list('CheckOpsApi', flat=True).first()
    ServerType = models.ProjectInfo.objects.filter(id=Id).values_list('ServerType', flat=True).first()
    ReSet = models.ProjectInfo.objects.filter(id=Id).values_list('ReSet', flat=True).first()
    RestorePath = "/"
    if IsNullOrSpace(Id) == 0:
        return redirect(RestorePath, messages.error(request, "恢复失败"))
    Date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    models.ModifyServerLog.objects.create(Project=Project, MemSize=MemSize, Node=Node,EnvPar=Env,
                                           CheckOpsApi=CheckOpsApi, Port=Port, ServerType=ServerType,
                                           ReSet=ReSet, ModifyTime=Date,Remarks='null',ModifyUser=username
                                           ).save()
    print(Id)
    models.ProjectInfo.objects.filter(id=Id).update(Del=0)
    return redirect('/ProjectInfo')