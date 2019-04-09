#coding:gbk

import sys
from PyOps import function

if sys.argv[1] == "all":
    AllServerGroupName = function.GetAllServerConnectionInformation()
    for i in range(1,len(AllServerGroupName)):
        function.GetServerConnectionInformation(AllServerGroupName[i])
        cmd = "python3 ~/python/agent.py"
        function.ConnectToTheServer(cmd)
else:
    function.GetServerConnectionInformation(sys.argv[1])
    cmd = "python3 ~/python/agent.py"
    function.ConnectToTheServer(cmd)