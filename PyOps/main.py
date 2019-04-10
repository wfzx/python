#coding:gbk

import os,sys,time

LogName = "./logs/PyOps.log"
if len(sys.argv) > 1:
    if sys.argv[1] == "ud":
        try:
            NumOne = str(input("请输入要操作的服务器组名:"))
            NumTwo = str(input("请输入要操作的类型(h5,java,mb,scp,dl,dlf):"))
        except KeyboardInterrupt:
            print ("退出")
            sys.exit()
        if os.name == "nt":
            ExecRUB = "python RUB.py %s %s" % (NumOne,NumTwo)
        else:
            ExecRUB = "python3 RUB.py %s %s" % (NumOne, NumTwo)
        try:
            os.system(ExecRUB)
        except KeyboardInterrupt:
            sys.exit()
    elif sys.argv[1] == "mt":
        try:
            AllAndSingle = str(input("请输入要检测的服务器名称或全部检测(all|groupname):"))
        except KeyboardInterrupt:
            print ("退出")
            sys.exit()
        if os.name == "nt":
            ExecMonitor = "python Monitor.py %s" % (AllAndSingle)
        else:
            ExecMonitor = "python3 Monitor.py %s" % (AllAndSingle)
        try:
            logging = open(LogName, "a")
        except FileNotFoundError:
            os.mkdir("./logs/")
            logging = open(LogName, "a")
        OutFile = "\n%s Exec Montior %s" % (time.strftime("%Y%m%d%H%M"),AllAndSingle)
        logging.write(OutFile)
        logging.close()
        os.system(ExecMonitor)
    elif sys.argv[1] == "dl":
        ServerName = sys.argv[2]
        Domain = sys.argv[3]
        SourcePackName = sys.argv[4]
        AimsPackName = sys.argv[5]
        if os.name == "nt":
            ExecRUB = "python RUB.py %s %s %s %s %s" % (sys.argv[1],ServerName,Domain,SourcePackName,AimsPackName)
        else:
            ExecRUB = "python3 RUB.py %s %s %s %s %s" % (sys.argv[1], ServerName, Domain, SourcePackName, AimsPackName)
        try:
            os.system(ExecRUB)
        except KeyboardInterrupt:
            pass
    else:
        try:
            logging = open(LogName, "a")
        except FileNotFoundError:
            os.mkdir("./logs/")
            logging = open(LogName, "a")
        OutFile = "\n%s No Exec error %s" % (time.strftime("%Y%m%d%H%M"), sys.argv[1:])
        logging.write(OutFile)
        logging.close()
        print(" Usage:\n","    python ",sys.argv[0]," <ud|mt>\n\n","No such option: ",sys.argv[1:])
        sys.exit()