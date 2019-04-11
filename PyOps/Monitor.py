#coding:gbk

import sys
from PyOps import function

if len(sys.argv) > 1:
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
else:
    print("Please pass the reference")
    sys.exit()