#coding:gbk

import os,sys,time

LogName = "%slogs/PyOps.log" % (os.path.abspath(sys.argv[0]).split(os.path.split(sys.argv[0])[1])[0])

def LogWrite(content):
    try:
        logging = open(LogName, "a")
    except FileNotFoundError:
        os.mkdir("%slogs/") % (os.path.abspath(sys.argv[0]).split(os.path.split(sys.argv[0])[1])[0])
        logging = open(LogName, "a")
    logging.write(content)
    logging.close()

def Message_Box(title,msg,status):
    from tkinter import messagebox
    if status == "info":
        messagebox.showinfo(title,msg)
    elif status == "warning":
        messagebox.showwarning(title,msg)
    elif status == "error":
        messagebox.showerror(title,msg)

if len(sys.argv) > 1:
    if sys.argv[1] == "ud":
        try:
            NumOne = str(input("请输入要操作的服务器组名:"))
            NumTwo = str(input("请输入要操作的类型(hp,java,mb,scp,dl,dlf):"))
        except KeyboardInterrupt:
            print ("退出")
            sys.exit()
        if os.name == "nt":
            ExecRUB = "python %sRUB.py %s %s" % (os.path.abspath(sys.argv[0]).split(os.path.split(sys.argv[0])[1])[0],NumOne,NumTwo)
        else:
            ExecRUB = "python3 %sRUB.py %s %s" % (os.path.abspath(sys.argv[0]).split(os.path.split(sys.argv[0])[1])[0],NumOne, NumTwo)
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
            ExecMonitor = "python %sMonitor.py %s" % (os.path.abspath(sys.argv[0]).split(os.path.split(sys.argv[0])[1])[0],AllAndSingle)
        else:
            ExecMonitor = "python3 %sMonitor.py %s" % (os.path.abspath(sys.argv[0]).split(os.path.split(sys.argv[0])[1])[0],AllAndSingle)
        OutFile = "\n%s Exec Montior %s" % (time.strftime("%Y%m%d %H:%M"), AllAndSingle)
        LogWrite(OutFile)
        os.system(ExecMonitor)
    elif sys.argv[1] == "dl":
        GroupName = sys.argv[2]
        Domain = sys.argv[3]
        SourcePackName = sys.argv[4]
        AimsPackName = sys.argv[5]
        if os.name == "nt":
            ExecRUB = "python %sRUB.py %s %s %s %s %s" % (os.path.abspath(sys.argv[0]).split(os.path.split(sys.argv[0])[1])[0],sys.argv[1],GroupName,Domain,SourcePackName,AimsPackName)
        else:
            ExecRUB = "python3 %sRUB.py %s %s %s %s %s" % (os.path.abspath(sys.argv[0]).split(os.path.split(sys.argv[0])[1])[0],sys.argv[1], GroupName, Domain, SourcePackName, AimsPackName)
        try:
            os.system(ExecRUB)
        except KeyboardInterrupt:
            pass
    elif sys.argv[1] == "dlf":
        GroupName = sys.argv[2]
        Domain = sys.argv[3]
        if len(sys.argv) == 5:
            if os.name == "nt":
                ExecRUB = "python %sRUB.py %s %s %s %s" % (os.path.abspath(sys.argv[0]).split(os.path.split(sys.argv[0])[1])[0], sys.argv[1], GroupName, Domain,sys.argv[4])
            else:
                ExecRUB = "python3 %sRUB.py %s %s %s" % (os.path.abspath(sys.argv[0]).split(os.path.split(sys.argv[0])[1])[0], sys.argv[1], GroupName, Domain)
        else:
            if os.name == "nt":
                ExecRUB = "python %sRUB.py %s %s %s" % (os.path.abspath(sys.argv[0]).split(os.path.split(sys.argv[0])[1])[0],sys.argv[1],GroupName,Domain)
            else:
                ExecRUB = "python3 %sRUB.py %s %s %s" % (os.path.abspath(sys.argv[0]).split(os.path.split(sys.argv[0])[1])[0],sys.argv[1], GroupName, Domain)
        try:
            os.system(ExecRUB)
        except KeyboardInterrupt:
            pass
    else:
        OutFile = "\n%s No Exec error %s" % (time.strftime("%Y%m%d %H:%M"), sys.argv[1:])
        LogWrite(OutFile)
        Outsg = "Usage:\n    python %s  <ud|mt>\n\n No such option: %s" % (sys.argv[0], sys.argv[1:])
        Message_Box('PyOps', Outsg, 'warning')
        sys.exit()
else:
    OutFile = "\n%s No Exec error %s" % (time.strftime("%Y%m%d %H:%M"), sys.argv[1:])
    LogWrite(OutFile)
    Outsg = "Usage:\n    python %s  <ud|mt>\n\n No such option: %s" % (sys.argv[0], sys.argv[1:])
    Message_Box('PyOps', Outsg, 'warning')
    sys.exit()