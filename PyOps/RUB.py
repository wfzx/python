#coding:gbk

import paramiko,sys,configparser,time,os

#��ȡ������������Ϣ
def GetServerConnectionInformation(address) :
    conf = configparser.ConfigParser()
    conf.read("./conf/wfl.conf")
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

#�ϴ��ļ���������
def UploadFileToServer(JH) :
    scp = paramiko.Transport(IP, Port)
    scp.connect(username=User, password=Passwd)
    sftp = paramiko.SFTPClient.from_transport(scp)
    if JH != "scp":
        if JH != "h5":
            if JH == "dl":
                MobileNewTarCmd = "%s \"cp %s%s%s %s%s\"" % (ROOT_User, Project_Path, Domain,Target_name,Home_Path, Target_name)
                ConnectToTheServer(MobileNewTarCmd)
                if os.path.isdir(WPath.split(Target_name)[0]) == False:
                    os.makedirs(WPath.split(Target_name)[0])
                sftp.get(Home_Path+Target_name,WPath)
                MobileNewTarCmdTwo = "%s \"rm -rf %s%s\"" % (ROOT_User,Home_Path,Target_name)
                ConnectToTheServer(MobileNewTarCmdTwo)
            elif JH == "dlf":
                PackName = "%s.tar.gz" % (Domain.split("/")[0])
                FilePackCmd = "%s \" cd %s && tar zcf %s %s && mv %s %s\"" % (ROOT_User,Project_Path,PackName,Domain,PackName,Home_Path)
                ConnectToTheServer(FilePackCmd)
                print ("�����ɣ���ʼ����")
                sftp.get(Home_Path+PackName,Source_Path+PackName)
                MobileNewTarCmdTwo = "%s \"rm -rf %s%s\"" % (ROOT_User,Home_Path,PackName)
                ConnectToTheServer(MobileNewTarCmdTwo)
            else:
                try:
                    sftp.put(WRPath, Home_Path+"restart.sh")
                except FileNotFoundError:
                    print("restart.sh�ļ�������,�˳�ִ��")
                    sys.exit()
                MobileNewReCmd = "%s \"mv %srestart.sh %s%s\"" % (ROOT_User, Home_Path,Project_Path, Domain)
                ConnectToTheServer(MobileNewReCmd)
    if JH != "dl" and JH != "dlf":
        sftp.put(WPath, Home_Path+Target_name)
        MobileNewTarCmd = "%s \"mv %s%s %s%s\"" % (ROOT_User,Home_Path, Target_name, Project_Path, Domain)
        ConnectToTheServer(MobileNewTarCmd)
    scp.close()

#���ӵ�������
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
    if JH == "h5":
        HPath = "%s%s_%s.tar.gz" % (DAPath, Domain.split("/")[0], DATE)
        BackLastCmd = "%s\"cd %s && tar zcf %s_%s.tar.gz %s && if [ ! -f %s ];then mkdir -p %s && mv %s%s_%s.tar.gz %s;fi\"" % (ROOT_User,Project_Path, Domain.split("/")[0],DATE,Domain,HPath,DAPath, Project_Path,Domain.split("/")[0],DATE, DAPath)
    else:
        BackLastCmd = "%s\"if [ ! -f %s%s ];then mkdir -p %s && mv %s%s;fi\"" % (ROOT_User, DAPath, Target_name, DAPath, LPath, DAPath)

    DeleTarCmd = "%s\"rm -rf %s\"" % (ROOT_User,LPath)
    ConnectToTheServer(BackLastCmd,DeleTarCmd)

#�����û����붨�����
def DefineVariablesBasedOnUserInput() :
    global DTPath,LPath,Domain,WPath,Target_name, ReStart,WRPath
    SystemVariables()
    DTPath = " %s%s/" % (Backup_Path, DATE)
    Domain = "%s/" % (str(input("Please enter Domain:")))
    if sys.argv[-1] != "dlf":
        WPath = "%s%s" % (Source_Path,str(input("Please enter the name of the package to upload or download:")))
        Target_name = str(input("Please enter the package name after uploading or download:"))
        LPath = "%s%s%s" % (Project_Path, Domain, Target_name)
    WRPath = "%srestart.sh" % (Source_Path)
    ReStart = "%s%srestart.sh" % (Project_Path, Domain)

def SystemVariables():
    global  DATE, JAVA_MeM, ROOT_User,LogName
    LogName = "./logs/PyOps.log"
    DATE = time.strftime("%Y%m%d")
    JAVA_MeM = " -Xms512m -Xmx512m -jar "
    ROOT_User = "sudo su root -c "


#�����ϴ��ļ�������������
def ExecUploadFileToServer(cs):
    try:
        if cs == "dl":
            print("��ʼ����")
        elif cs == "dlf":
            print ("��ʼ���")
        else:
            print("��ʼ�ϴ�")
        UploadFileToServer(cs)
        if cs == "dl" or cs == "dlf":
            print("�������")
        else:
            print("�ϴ����")
    except PermissionError:
        print("û��Ȩ�޻����ϴ��ļ���")
    except FileNotFoundError:
        print("�ļ���Զ��Ŀ¼������")

#��������
def ExecRelease():
    try:
        BackUpTheOriginalFile(DTPath, sys.argv[-1])
        ExecUploadFileToServer(sys.argv[-1])
        ConnectToTheServer(StartServiceCmd)
    except TimeoutError:
        print ("�������������Ƿ�����")

#��ȡ�������ݿ��б�
def GetAllDBList():
    MyDbList = "%s\"mysql -u root -p%s -e 'show databases'|grep -v Database\"" % (ROOT_User,MyPass)
    ConnectToTheServer(MyDbList)

#��ȡ�û���������һ�������Ƿ�Ϊscp
if sys.argv[-1] == "scp":
    try:
        GetServerConnectionInformation(sys.argv[1])
    except configparser.NoSectionError:
        print ("No Such ",sys.argv[1]," Group")
        sys.exit()

    try:
        DefineVariablesBasedOnUserInput()
        try:
            logging = open(LogName, "a")
        except FileNotFoundError:
            os.mkdir("./logs/")
            logging = open(LogName, "a")
        OutFile = "\n%s %s Upload %s in %s" % (time.strftime("%Y%m%d%H%M"),Target_name,Domain.split("/")[0],IP)
        logging.write(OutFile)
        logging.close()
    except KeyboardInterrupt:
        print ("�˳�")
        sys.exit()
    ExecUploadFileToServer(sys.argv[-1])
# ��ȡ�û���������һ�������Ƿ�Ϊjava
elif sys.argv[-1] == "java":
    try:
        GetServerConnectionInformation(sys.argv[1])
    except configparser.NoSectionError:
        print ("No Such ",sys.argv[1]," Group")
        sys.exit()

    DefineVariablesBasedOnUserInput()
    StartServiceCmd = "%s\"sed -i 's/zhuxiaoxuan/%s/g' %s && cd %s%s && sh restart.sh && chown -R www.www %s%s\"" % (ROOT_User,Target_name,ReStart, Project_Path, Domain, Project_Path, Domain)
    ExecRelease()
#��ȡ�û���������һ�������Ƿ�Ϊh5
elif sys.argv[-1] == "h5":
    try:
        GetServerConnectionInformation(sys.argv[1])
    except configparser.NoSectionError:
        print ("No Such ",sys.argv[1]," Group")
        sys.exit()

    DefineVariablesBasedOnUserInput()
    if "zip" in Target_name:
        StartServiceCmd = "%s\" cd %s%s && rm -rf static index.html && unzip -o %s && if [ ! -d %s/%s ];then mv %s/* ./ && rm -rf %s* && chown -R www.www %s%s;else mv %s/%s/* ./ && rm -rf %s* && chown -R www.www %s%s;fi\"" % (ROOT_User, Project_Path, Domain, Target_name, Target_name.split(".")[0], Target_name.split(".")[0],Target_name.split(".")[0], Target_name.split(".")[0], Project_Path, Domain, Target_name.split(".")[0],Target_name.split(".")[0], Target_name.split(".")[0], Project_Path, Domain)
    else:
        StartServiceCmd = "%s\" cd %s%s && rm -rf static index.html && tar zxf %s && if [ ! -d %s/%s ];then mv %s/* ./ && rm -rf %s* && chown -R www.www %s%s;else mv %s/%s/* ./ && rm -rf %s* && chown -R www.www %s%s;fi\"" % (ROOT_User, Project_Path, Domain, Target_name, Target_name.split(".tar")[0], Target_name.split(".tar")[0],Target_name.split(".tar")[0], Target_name.split(".tar")[0], Project_Path, Domain, Target_name.split(".tar")[0],Target_name.split(".tar")[0], Target_name.split(".tar")[0], Project_Path, Domain)

    ExecRelease()
#��ȡ�û���������һ�������Ƿ�Ϊmb
elif sys.argv[-1] == "mb":
    try:
        GetServerConnectionInformation(sys.argv[1])
    except configparser.NoSectionError:
        print ("No Such ",sys.argv[1]," Group")
        sys.exit()

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
            TarPackCmd = "%s\"cd %s && tar zcf %s.tar.gz %s\"" % (ROOT_User, MyBackup_Path, DATE, DATE)
            ConnectToTheServer(StartInputSqlCmd,TarPackCmd)
    print ("���ݿ��Ѿ�������",MyBackup_Path,DATE,".tar.gz")
    try:
        logging = open(LogName, "a")
    except FileNotFoundError:
        os.mkdir("./logs/")
        logging = open(LogName, "a")
    OutFile = "\n%s �������ݿ� %s" % (time.strftime("%Y%m%d%H%M"), IP)
    logging.write(OutFile)
    logging.close()
#�ӷ������������ļ�������
elif len(sys.argv) > 1:
    #���򽻻�ʽ����
    if sys.argv[-1] == "dl":
        try:
            GetServerConnectionInformation(sys.argv[1])
        except configparser.NoSectionError:
            print("No Such ", sys.argv[1], " Group")
            sys.exit()
        try:
            DefineVariablesBasedOnUserInput()
            try:
                logging = open(LogName, "a")
            except FileNotFoundError:
                os.mkdir("./logs/")
                logging = open(LogName, "a")
            OutFile = "\n%s %s Download %s in %s" % (time.strftime("%Y%m%d%H%M"), Target_name, Domain.split("/")[0], IP)
            logging.write(OutFile)
            logging.close()
        except KeyboardInterrupt:
            print("�˳�")
            sys.exit()
        ExecUploadFileToServer(sys.argv[-1])
    #����Ŀ��Ŀ¼�ļ����ƴ������
    elif sys.argv[-1] == "dlf":
        try:
            GetServerConnectionInformation(sys.argv[1])
        except configparser.NoSectionError:
            print("No Such ", sys.argv[1], " Group")
            sys.exit()
        try:
            DefineVariablesBasedOnUserInput()
            try:
                logging = open(LogName, "a")
            except FileNotFoundError:
                os.mkdir("./logs/")
                logging = open(LogName, "a")
            OutFile = "\n%s  Download %s.tar.gz in %s" % (time.strftime("%Y%m%d%H%M"), Domain.split("/")[0], IP)
            logging.write(OutFile)
            logging.close()
        except KeyboardInterrupt:
            print("�˳�")
            sys.exit()
        ExecUploadFileToServer(sys.argv[-1])
    #������ʽ����
    elif sys.argv[1] == "dl":
        try:
            GetServerConnectionInformation(sys.argv[2])
        except configparser.NoSectionError:
            print ("No Such ",sys.argv[1]," Group")
            sys.exit()
        SystemVariables()
        DTPath = " %s%s/" % (Backup_Path, DATE)
        Domain = "%s/" % (sys.argv[3])
        WPath = "%s%s/%s" % (Source_Path,time.strftime("%Y%m%d%H%M"),sys.argv[4])
        WRPath = "%srestart.sh" % (Source_Path)
        Target_name = sys.argv[5]
        LPath = "%s%s%s" % (Project_Path, Domain, Target_name)
        ReStart = "%s%srestart.sh" % (Project_Path, Domain)
        try:
            logging = open(LogName, "a")
        except FileNotFoundError:
            os.mkdir("./logs/")
            logging = open(LogName, "a")
        OutFile = "\n%s %s Download %s in %s" % (time.strftime("%Y%m%d%H%M"), Target_name, Domain.split("/")[0], IP)
        logging.write(OutFile)
        logging.close()
        ExecUploadFileToServer(sys.argv[1])
#����������ھ��˳�
else:
    try:
        GetServerConnectionInformation(sys.argv[1])
    except configparser.NoSectionError:
        print (" No Such ",sys.argv[1]," Group\n")
    SystemVariables()
    try:
        logging = open(LogName, "a")
    except FileNotFoundError:
        os.mkdir("./logs/")
        logging = open(LogName, "a")
    OutFile = "\n%s No Exec error %s" % (time.strftime("%Y%m%d%H%M"), sys.argv[2:])
    logging.write(OutFile)
    logging.close()
    print(" Usage:\n","    python ",sys.argv[0]," <groupID> <java|h5|mb|scp|dl|dlf>\n\n","No such option: ",sys.argv[2:])
    sys.exit()
print("�������")