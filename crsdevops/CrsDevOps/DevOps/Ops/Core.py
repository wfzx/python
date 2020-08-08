from Ops import models
import time
import requests

def ProjectStatusCheck():
    DATE = time.strftime('%Y-%m-%d %H:%M:%S')
    # 执行查询服务状态
    for IDNum in range(0,len(models.ProjectInfo.objects.filter(Del=0).values_list('id',flat=True))):
        ID = models.ProjectInfo.objects.filter(Del=0).values_list('id', flat=True)[IDNum]
        EnvPar = models.ProjectInfo.objects.filter(id=ID).values_list('EnvPar', flat=True).first()
        if EnvPar == 'prd':
            continue
        Node = models.ProjectInfo.objects.filter(id=ID).values_list('Node', flat=True).first()
        Port = models.ProjectInfo.objects.filter(id=ID).values_list('Port', flat=True).first()
        CheckOpsApi = models.ProjectInfo.objects.filter(id=ID).values_list('CheckOpsApi', flat=True).first()
        Status = {}
        for t in Node.split(":"):
            FNode = t
            url = "http://%s:%s%s" % (FNode, Port, CheckOpsApi)
            try:
                Code = requests.get(url, timeout=2)
                if Code.status_code == 200:
                    StatusInDb = "RUNNINE"
                else:
                    StatusInDb = "DOWN"
            except requests.exceptions.ConnectionError:
                StatusInDb = "DOWN"
            except requests.exceptions.ReadTimeout:
                StatusInDb = "DOWN"
            except requests.exceptions.InvalidURL:
                StatusInDb = "DOWN"
            Status[FNode] = [StatusInDb]
        models.ProjectInfo.objects.filter(id=ID).update(ProjectStatus=Status,CheckApiTime=DATE)
    models.CronExecReco.objects.create(ExecTime=DATE,Who='CrsDevOps').save()