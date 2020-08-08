import time
import requests
from connection import connectionMysqlDB

DATE = time.strftime('%Y-%m-%d %H:%M:%S')
Env = 'prd'
ConDB = connectionMysqlDB(Env)
GetProjectInfoSql = "select id,Node,Port,CheckOpsApi from Ops_projectinfo" \
                            " where EnvPar = '%s' and Del = '0'" % (Env)
ConDB.CheckApi(GetProjectInfoSql)
for i in range(0,len(ConDB.Out)):
    ID = ConDB.Out[i][0]
    Node = ConDB.Out[i][1]
    Port = ConDB.Out[i][2]
    CheckOpsApi = ConDB.Out[i][3]
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
    UpdateDataSQL = "update Ops_projectinfo set ProjectStatus = \"%s\",CheckApiTime = '%s' where id = %s" % (Status,DATE,ID)
    ConDB.CheckApi(UpdateDataSQL)
ExecUpdateDataSQL = "insert Ops_cronexecreco (ExecTime,Who) values ('%s','ReleasePrd')" % (DATE)
ConDB.CheckApi(ExecUpdateDataSQL)