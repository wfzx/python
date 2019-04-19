#coding:gbk

import paramiko,sys,configparser,time,os

#��ȡ������������Ϣ
def GetServerConnectionInformation(address) :
    conf = configparser.ConfigParser()
    ConfName = "%sconf/sdgroup.conf" % (os.path.abspath(sys.argv[0]).split(os.path.split(sys.argv[0])[1])[0])
    conf.read(ConfName)
    global IP,Port,User,Passwd,Backup_Path,Project_Path,Home_Path,MyPass,Source_Path
    Source_Path = conf.get("source",'source_path')
    IP = conf.get(address, 'ip')
    Port = int(conf.get(address, 'port'))
    User = conf.get(address,'user')
    Passwd = conf.get(address, 'passwd')
    Backup_Path = conf.get(address,'backup_path')
    Project_Path = conf.get(address,'project_path')
    Home_Path = conf.get(address,'home')
    MyPass = conf.get(address,'mysql_passwd')

#����windows����
def Message_Box(title,msg,status):
    from tkinter import messagebox
    if status == "info":
        messagebox.showinfo(title,msg)
    elif status == "warning":
        messagebox.showwarning(title,msg)
    elif status == "error":
        messagebox.showerror(title,msg)

#�ϴ��������ļ�
def UploadAndDownloadFile(JH) :
    scp = paramiko.Transport(IP, Port)
    scp.connect(username=User, password=Passwd)
    sftp = paramiko.SFTPClient.from_transport(scp)
    if JH != "scp":
        if JH != "hp":
            if JH == "dl":
                MobileNewTarCmd = "%s \"cp %s%s%s %s%s\"" % (ROOT_User, Project_Path, Domain,Target_name,Home_Path, Target_name)
                ConnectToTheServer(MobileNewTarCmd)
                if os.path.isdir(WPath.split(Target_name)[0]) == False:
                    os.makedirs(WPath.split(Target_name)[0])
                try:
                    print ("�ļ������: %s%s" % (Source_Path,Target_name))
                    sftp.get(Home_Path+Target_name,WPath)
                except ZeroDivisionError:
                    print ("�ļ�С�ڵ���0KB,�����ļ�")
                    scp.close()
                    sys.exit()
                finally:
                    if os.path.getsize(WPath) <= 0:
                        os.remove(WPath)
                MobileNewTarCmdTwo = "%s \"rm -rf %s%s\"" % (ROOT_User,Home_Path,Target_name)
                ConnectToTheServer(MobileNewTarCmdTwo)
            elif JH == "dlf":
                PackName = "%s_%s.tar.gz" % (Domain.split("/")[0],time.strftime("%Y%m%d%H%M"))
                FilePackCmd = "%s \" cd %s && tar zcf %s %s && mv %s %s\"" % (ROOT_User,Project_Path,PackName,Domain,PackName,Home_Path)
                ConnectToTheServer(FilePackCmd)
                print ("�����ɣ���ʼ����")
                global Source_data_path
                Source_data_path = "%s%s" % (Source_Path, DATE)
                if os.path.isdir(Source_data_path) == False:
                    os.mkdir(Source_data_path)
                if os.name == "nt":
                    source_home = "%s\%s" % (Source_data_path, PackName)
                else:
                    source_home = "%s/%s" % (Source_data_path, PackName)
                try:
                    print("�ļ������: %s" % (source_home))
                    sftp.get(Home_Path + PackName, source_home)
                except ZeroDivisionError:
                    print ("�ļ�С�ڵ���0KB,�����ļ�")
                    scp.close()
                    sys.exit()
                finally:
                    if os.path.getsize(source_home) <= 0 :
                        os.remove(source_home)
                    MobileNewTarCmdTwo = "%s \"rm -rf %s%s\"" % (ROOT_User,Home_Path,PackName)
                    ConnectToTheServer(MobileNewTarCmdTwo)
            else:
                try:
                    print ("restart.sh")
                    print("�ļ������: %s%srestart.sh" % (Project_Path,Domain))
                    sftp.put(WRPath, Home_Path+"restart.sh")
                except FileNotFoundError:
                    print("restart.sh�ļ�������,�˳�ִ��")
                    scp.close()
                    sys.exit()
                except ZeroDivisionError:
                    print ("�ļ�С�ڵ���0KB,�����ļ�")
                    scp.close()
                    sys.exit()
                MobileNewReCmd = "%s \"mv %srestart.sh %s%s\"" % (ROOT_User, Home_Path,Project_Path, Domain)
                ConnectToTheServer(MobileNewReCmd)
    if JH != "dl" and JH != "dlf":
        print (Target_name)
        try:
            print("�ļ������: %s%s%s" % (Project_Path,Domain,Target_name))
            sftp.put(WPath, Home_Path+Target_name)
        except ZeroDivisionError:
            print ("�ļ�С�ڵ���0KB,�����ļ�")
            scp.close()
            sys.exit()
        MobileNewTarCmd = "%s \" if [ ! -f %s%s ];then mkdir -p %s%s ;fi && mv %s%s %s%s\"" % (ROOT_User,Project_Path, Domain,Project_Path, Domain,Home_Path, Target_name, Project_Path, Domain)
        ConnectToTheServer(MobileNewTarCmd)
    scp.close()

#���ӵ�����������ִ������
def ConnectToTheServer(*params) :
    global outmsg
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(IP, Port, User, Passwd)
    for i in params:
        stdin, stdout, stderr = ssh.exec_command(i)
        outmsg, errmsg = stdout.read(), stderr.read()
        # if outmsg != "":
        #     print(outmsg)
        # if errmsg != "":
        #     print(errmsg)
    ssh.close()

#����ԭʼ�ļ�
def BackUpTheOriginalFile(DAPath,JH) :
    global BackLastCmd,HPath
    if JH == "hp":
        HPath = "%s%s_%s.tar.gz" % (DAPath, Domain.split("/")[0], DATE)
        BackLastCmd = "%s\"cd %s && tar zcf %s_%s.tar.gz %s && if [ ! -f %s ];then mkdir -p %s && mv %s%s_%s.tar.gz %s;else rm -rf %s_%s.tar.gz fi\"" % (ROOT_User,Project_Path, Domain.split("/")[0],DATE,Domain,HPath,DAPath, Project_Path,Domain.split("/")[0],DATE, DAPath,Domain.split("/")[0],DATE)
    else:
        BackLastCmd = "%s\"if [ ! -f %s%s ];then mkdir -p %s && mv %s %s;fi\"" % (ROOT_User, DAPath, Target_name, DAPath, LPath, DAPath)

    DeleTarCmd = "%s\"rm -rf %s\"" % (ROOT_User,LPath)
    ConnectToTheServer(BackLastCmd,DeleTarCmd)

#�����û����붨�����
def DefineVariablesBasedOnUserInput() :
    global DTPath,LPath,Domain,WPath,Target_name, ReStart,WRPath
    SystemVariables()
    DTPath = " %s%s/" % (Backup_Path, DATE)
    if len(sys.argv) > 3:
        Domain = sys.argv[3]
    else:
        Domain = "%s/" % (str(input("Please enter Domain:")))

    if sys.argv[-1] != "dlf" and sys.argv[1] != "dlf":
        WPath = "%s%s" % (Source_Path,str(input("Please enter the name of the package to upload or download:")))
        Target_name = str(input("Please enter the package name after uploading or download:"))
        LPath = "%s%s%s" % (Project_Path, Domain, Target_name)
    if sys.argv[-1] == "java":
        WRPath = "%srestart.sh" % (Source_Path)
        ReStart = "%s%srestart.sh" % (Project_Path, Domain)

#Ĭ�ϱ���ı���
def SystemVariables():
    global  DATE, JAVA_MeM, ROOT_User,LogName
    LogName = "%slogs/PyOps.log" % (os.path.abspath(sys.argv[0]).split(os.path.split(sys.argv[0])[1])[0])
    DATE = time.strftime("%Y%m%d")
    JAVA_MeM = " -Xms512m -Xmx512m -jar "
    ROOT_User = "sudo su root -c "


#�����ϴ��������ļ�
def ExecUploadAndDownloadFile(cs):
    try:
        if cs == "dl":
            print("��ʼ����")
        elif cs == "dlf":
            print ("��ʼ���")
        else:
            print("��ʼ�ϴ�")
        UploadAndDownloadFile(cs)
        if cs == "dl" or cs == "dlf":
            print("�������")
        else:
            print("�ϴ����")
    except PermissionError:
        print("û��Ȩ�޻����ϴ��ļ���")
    except FileNotFoundError:
        print("�ļ���Զ��Ŀ¼������")

#����
def ExecRelease():
    try:
        BackUpTheOriginalFile(DTPath, sys.argv[-1])
        ExecUploadAndDownloadFile(sys.argv[-1])
        ConnectToTheServer(StartServiceCmd)
    except TimeoutError:
        print ("�������������Ƿ�����")

#ִ�л�ȡ��������Ϣ
def ExecGetServerConnectionInformation(gname):
    try:
        GetServerConnectionInformation(gname)
    except configparser.NoSectionError:
        if os.name == "nt":
            Outsg = " No Such %s  Group\n" % (sys.argv[1])
            Message_Box('PyOps', Outsg,"warning")
        sys.exit()

#��ȡ�������ݿ��б�
def GetAllDBList():
    MyDbList = "%s\"mysql -u root -p%s -e 'show databases'|grep -v Database\"" % (ROOT_User,MyPass)
    ConnectToTheServer(MyDbList)

#д��log
def LogWrite(content):
    try:
        logging = open(LogName, "a")
    except FileNotFoundError:
        os.mkdir("%slogs/") % (os.path.abspath(sys.argv[0]).split(__file__)[0])
        logging = open(LogName, "a")
    logging.write(content)
    logging.close()

if len(sys.argv) > 1:
#��ȡ�û���������һ�������Ƿ�Ϊscp
    if sys.argv[-1] == "scp":
        ExecGetServerConnectionInformation(sys.argv[1])
        try:
            DefineVariablesBasedOnUserInput()
            OutFile = "\n%s %s Upload %s in %s" % (time.strftime("%Y%m%d %H:%M"), Target_name, Domain.split("/")[0], IP)
            LogWrite(OutFile)
        except KeyboardInterrupt:
            print ("�˳�")
            sys.exit()
        ExecUploadAndDownloadFile(sys.argv[-1])
    # ��ȡ�û���������һ�������Ƿ�Ϊjava
    elif sys.argv[-1] == "java":
        ExecGetServerConnectionInformation(sys.argv[1])
        DefineVariablesBasedOnUserInput()
        StartServiceCmd = "%s\"sed -i 's/PyOps/%s/g' %s && cd %s%s && sh restart.sh && chown -R www.www %s%s\"" % (ROOT_User,Target_name,ReStart, Project_Path, Domain, Project_Path, Domain)
        ExecRelease()
    #��ȡ�û���������һ�������Ƿ�Ϊhp
    elif sys.argv[-1] == "hp":
        ExecGetServerConnectionInformation(sys.argv[1])
        DefineVariablesBasedOnUserInput()
        if "zip" in Target_name:
            StartServiceCmd = "%s\" cd %s%s && rm -rf static index.html && unzip -o %s && if [ ! -d %s/%s ];then mv %s/* ./ && rm -rf %s* && chown -R www.www %s%s;else mv %s/%s/* ./ && rm -rf %s* && chown -R www.www %s%s;fi\"" % (ROOT_User, Project_Path, Domain, Target_name, Target_name.split(".")[0], Target_name.split(".")[0],Target_name.split(".")[0], Target_name.split(".")[0], Project_Path, Domain, Target_name.split(".")[0],Target_name.split(".")[0], Target_name.split(".")[0], Project_Path, Domain)
        else:
            StartServiceCmd = "%s\" cd %s%s && tar zxf %s && if [ ! -d %s/%s ];then mv %s/* ./ && rm -rf %s* && chown -R www.www %s%s;else mv %s/%s/* ./ && rm -rf %s* && chown -R www.www %s%s;fi\"" % (ROOT_User, Project_Path, Domain, Target_name, Target_name.split("_")[0], Target_name.split("_")[0],Target_name.split("_")[0], Target_name.split("_")[0], Project_Path, Domain, Target_name.split("_")[0],Target_name.split("_")[0], Target_name.split("_")[0], Project_Path, Domain)
            print (StartServiceCmd)
        ExecRelease()
    #��ȡ�û���������һ�������Ƿ�Ϊmb
    elif sys.argv[-1] == "mb":
        ExecGetServerConnectionInformation(sys.argv[1])
        SystemVariables()
        GetAllDBList()
        for MD in outmsg.split( ):
            global MyBackup_Path
            if MD.decode().strip() in ('information_schema','mysql','performance_schema'):
                continue
            else:
                MyBackup_Path = "%smysql/" % (Backup_Path)
                DumpCmd = "mysqldump -u root -p%s %s > %s%s/%s_%s.sql" % (MyPass, MD.decode().strip(), MyBackup_Path, DATE, MD.decode().strip(), DATE)
                StartInputSqlCmd = "%s\"if [ -d %s%s/ ];then %s;else mkdir -p %s%s/ && %s;fi\"" % (ROOT_User, MyBackup_Path, DATE, DumpCmd, MyBackup_Path, DATE, DumpCmd)
                TarPackCmd = "%s\"cd %s && tar zcf sql_%s.tar.gz %s\"" % (ROOT_User, MyBackup_Path, DATE, DATE)
                print ("��ʼ����")
                ConnectToTheServer(StartInputSqlCmd,TarPackCmd)
        print ("���ݿ��Ѿ�������",MyBackup_Path,DATE,".tar.gz")
        OutFile = "\n%s �������ݿ� %s" % (time.strftime("%Y%m%d%H%M"), IP)
        LogWrite(OutFile)
    #���򽻻�ʽ����
    elif sys.argv[-1] == "dl":
        ExecGetServerConnectionInformation(sys.argv[1])
        try:
            DefineVariablesBasedOnUserInput()
            OutFile = "\n%s %s Download %s in %s" % (time.strftime("%Y%m%d %H:%M"), Target_name, Domain.split("/")[0], IP)
            LogWrite(OutFile)
        except KeyboardInterrupt:
            print("�˳�")
            sys.exit()
        ExecUploadAndDownloadFile(sys.argv[-1])
    #����Ŀ��Ŀ¼�ļ����ƴ������
    elif sys.argv[-1] == "dlf":
        ExecGetServerConnectionInformation(sys.argv[1])
        try:
            DefineVariablesBasedOnUserInput()
            OutFile = "\n%s Download %s.tar.gz in %s" % (time.strftime("%Y%m%d %H:%M"), Domain.split("/")[0], IP)
            LogWrite(OutFile)
        except KeyboardInterrupt:
            print("�˳�")
            sys.exit()
        ExecUploadAndDownloadFile(sys.argv[-1])
    # ������ʽĿ��Ŀ¼�ļ����ƴ������
    elif sys.argv[1] == "dlf":
        ExecGetServerConnectionInformation(sys.argv[2])
        try:
            DefineVariablesBasedOnUserInput()
            OutFile = "\n%s Download %s_%s.tar.gz in %s" % (time.strftime("%Y%m%d %H:%M"), Domain.split("/")[0],time.strftime("%Y%m%d%H%M"), IP)
            LogWrite(OutFile)
        except KeyboardInterrupt:
            print("�˳�")
            sys.exit()
        ExecUploadAndDownloadFile(sys.argv[1])
    #������ʽ����
    elif sys.argv[1] == "dl":
        ExecGetServerConnectionInformation(sys.argv[2])
        SystemVariables()
        DTPath = " %s%s/" % (Backup_Path, DATE)
        Domain = "%s/" % (sys.argv[3])
        WPath = "%s%s/%s" % (Source_Path,time.strftime("%Y%m%d%H%M"),sys.argv[4])
        WRPath = "%srestart.sh" % (Source_Path)
        Target_name = sys.argv[5]
        LPath = "%s%s%s" % (Project_Path, Domain, Target_name)
        ReStart = "%s%srestart.sh" % (Project_Path, Domain)
        OutFile = "\n%s %s Download %s in %s" % (time.strftime("%Y%m%d %H:%M"), Target_name, Domain.split("/")[0], IP)
        LogWrite(OutFile)
        ExecUploadAndDownloadFile(sys.argv[1])
#����������ھ��˳�
    else:
        ExecGetServerConnectionInformation(sys.argv[1])
        SystemVariables()
        OutFile = "\n%s No Exec error %s" % (time.strftime("%Y%m%d %H:%M"), sys.argv[2:])
        LogWrite(OutFile)
        Outsg = "Usage:\n    python %s  <groupID> <java|hp|mb|scp|dl|dlf>\n\n No such option: %s" % (sys.argv[0], sys.argv[2:])
        Message_Box('PyOps', Outsg, 'warning')
        sys.exit()
else:
    SystemVariables()
    OutFile = "\n%s No Exec error %s" % (time.strftime("%Y%m%d %H:%M"), sys.argv[2:])
    LogWrite(OutFile)
    Outsg = "Usage:\n    python %s  <groupID> <java|hp|mb|scp|dl|dlf>\n\n No such option: %s" % (sys.argv[0],sys.argv[2:])
    Message_Box('PyOps',Outsg,'warning')
    sys.exit()

#����ִ�к�������
if sys.argv[-1] != "no":
    if os.name == "nt":
        Message_Box('PyOps',"�������","info")
    else:
        print("�������")