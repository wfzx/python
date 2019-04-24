#coding:gbk

import configparser,sys,os
from PyOps.Adjustment import ConntionInfo

if len(sys.argv) > 1:
    if sys.argv[1] == "all":
        ConfName = "%sconf/sdgroup.conf" % (os.path.abspath(sys.argv[0]).split(os.path.split(sys.argv[0])[1])[0])
        conf = configparser.ConfigParser()
        conf.read(ConfName)
        sections = conf.sections()
        for i in range(1, len(sections)):
            Connection = ConntionInfo(sections[i])
            cmd = "python ~/python/agent.py"
            Connection.ConntionSSH(cmd)

    else:
        Connection = ConntionInfo(sys.argv[1])
        cmd = "python ~/python/agent.py"
        Connection.ConntionSSH(cmd)
else:
    print("Please pass the reference")
    sys.exit()