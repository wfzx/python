#coding:gbk

import paramiko,sys,time,os,pymysql
from Adjustment import ConntionInfo


# 上传或下载文件
def UploadAndDownloadFile(JH):
    scp = paramiko.Transport(Conection.IP, Conection.Port)
    scp.connect(username=Conection.User, password=Conection.Passwd)
    sftp = paramiko.SFTPClient.from_transport(scp)
    if JH != "scp":
        if JH != "hp":
            if JH == "dl":
                MobileNewTarCmd = "%s \"cp %s%s%s %s%s\"" % (
                ROOT_User, Conection.Project_Path, Domain, Target_name, Conection.Home_Path, Target_name)
                ConntionInfo.ConntionSSH(MobileNewTarCmd)
                if os.path.isdir(WPath.split(Target_name)[0]) == False:
                    os.makedirs(WPath.split(Target_name)[0])
                try:
                    print("文件存放在: %s%s" % (Conection.Source_Path, Target_name))
                    sftp.get(Conection.Home_Path + Target_name, WPath)
                except ZeroDivisionError:
                    print("文件小于等于0KB,请检查文件")
                    scp.close()
                    sys.exit()
                finally:
                    if os.path.getsize(WPath) <= 0:
                        os.remove(WPath)
                MobileNewTarCmdTwo = "%s \"rm -rf %s%s\"" % (ROOT_User, Conection.Home_Path, Target_name)
                ConntionInfo.ConntionSSH(MobileNewTarCmdTwo)
            elif JH == "dlf":
                PackName = "%s_%s.tar.gz" % (Domain.split("/")[0], time.strftime("%Y%m%d%H%M"))
                FilePackCmd = "%s \" cd %s && tar zcf %s %s && mv %s %s\"" % (
                    ROOT_User, Conection.Project_Path, PackName, Domain, PackName, Conection.Home_Path)
                ConntionInfo.ConntionSSH(FilePackCmd)
                print("打包完成，开始下载")
                global Source_data_path
                Source_data_path = "%s%s" % (Conection.Source_Path, DATE)
                if os.path.isdir(Source_data_path) == False:
                    os.mkdir(Source_data_path)
                if os.name == "nt":
                    source_home = "%s\%s" % (Source_data_path, PackName)
                else:
                    source_home = "%s/%s" % (Source_data_path, PackName)
                try:
                    print("文件存放在: %s" % (source_home))
                    sftp.get(Conection.Home_Path + PackName, source_home)
                except ZeroDivisionError:
                    print("文件小于等于0KB,请检查文件")
                    scp.close()
                    sys.exit()
                finally:
                    if os.path.getsize(source_home) <= 0:
                        os.remove(source_home)
                    MobileNewTarCmdTwo = "%s \"rm -rf %s%s\"" % (ROOT_User, Conection.Home_Path, PackName)
                    ConntionInfo.ConntionSSH( MobileNewTarCmdTwo)
            else:
                try:
                    print("restart.sh")
                    print("文件存放在: %s%srestart.sh" % (Conection.Project_Path, Domain))
                    sftp.put(WRPath, Conection.Home_Path + "restart.sh")
                except FileNotFoundError:
                    print("restart.sh文件不存在,退出执行")
                    scp.close()
                    sys.exit()
                except ZeroDivisionError:
                    print("文件小于等于0KB,请检查文件")
                    scp.close()
                    sys.exit()
                MobileNewReCmd = "%s \"mv %srestart.sh %s%s\"" % (ROOT_User, Conection.Home_Path, Conection.Project_Path, Domain)
                ConntionInfo.ConntionSSH( MobileNewReCmd)
    if JH != "dl" and JH != "dlf":
        print(Target_name)
        try:
            print("文件存放在: %s%s%s" % (Conection.Project_Path, Domain, Target_name))
            sftp.put(WPath, Conection.Home_Path + Target_name)
        except ZeroDivisionError:
            print("文件小于等于0KB,请检查文件")
            scp.close()
            sys.exit()
        MobileNewTarCmd = "%s \" if [ ! -f %s%s ];then mkdir -p %s%s ;fi && mv %s%s %s%s\"" % (
            ROOT_User, Conection.Project_Path, Domain, Conection.Project_Path, Domain, Conection.Home_Path, Target_name,
            Conection.Project_Path, Domain)
        ConntionInfo.ConntionSSH(MobileNewTarCmd)
    scp.close()


# 备份原始文件
def BackUpTheOriginalFile(DAPath, JH):
    global BackLastCmd, HPath
    if JH == "hp":
        HPath = "%s%s_%s.tar.gz" % (DAPath, Domain.split("/")[0], DATE)
        BackLastCmd = "%s\"cd %s && tar zcf %s_%s.tar.gz %s && if [ ! -f %s ];then mkdir -p %s && mv %s%s_%s.tar.gz %s;else rm -rf %s_%s.tar.gz fi\"" % (
            ROOT_User, Conection.Project_Path, Domain.split("/")[0], DATE, Domain, HPath, DAPath, Conection.Project_Path,
            Domain.split("/")[0], DATE, DAPath, Domain.split("/")[0], DATE)
    else:
        BackLastCmd = "%s\"if [ ! -f %s%s ];then mkdir -p %s && mv %s %s;fi\"" % (
            ROOT_User, DAPath, Target_name, DAPath, LPath, DAPath)

    DeleTarCmd = "%s\"rm -rf %s\"" % (ROOT_User, LPath)
    ConntionInfo.ConntionSSH(BackLastCmd, DeleTarCmd)


# 根据用户输入定义变量
def DefineVariablesBasedOnUserInput():
    global DTPath, LPath, Domain, WPath, Target_name, ReStart, WRPath
    SystemVariables()
    DTPath = " %s%s/" % (Conection.Backup_Path, DATE)
    if len(sys.argv) > 3:
        Domain = sys.argv[3]
    else:
        Domain = "%s/" % (str(input("Please enter Domain:")))

    if sys.argv[-1] != "dlf" and sys.argv[1] != "dlf":
        WPath = "%s%s" % (Conection.Source_Path, str(input("Please enter the name of the package to upload or download:")))
        Target_name = str(input("Please enter the package name after uploading or download:"))
        LPath = "%s%s%s" % (Conection.Project_Path, Domain, Target_name)
    if sys.argv[-1] == "java":
        WRPath = "%srestart.sh" % (Conection.Source_Path)
        ReStart = "%s%srestart.sh" % (Conection.Project_Path, Domain)


# 默认必须的变量
def SystemVariables():
    global DATE, JAVA_MeM, ROOT_User
    DATE = time.strftime("%Y%m%d")
    JAVA_MeM = " -Xms512m -Xmx512m -jar "
    ROOT_User = "sudo su root -c "


# 调用上传或下载文件
def ExecUploadAndDownloadFile(cs):
    try:
        if cs == "dl":
            print("开始下载")
        elif cs == "dlf":
            print("开始打包")
        else:
            print("开始上传")
        UploadAndDownloadFile(cs)
        if cs == "dl" or cs == "dlf":
            print("下载完成")
        else:
            print("上传完成")
    except PermissionError:
        print("没有权限或不能上传文件夹")
    except FileNotFoundError:
        print("文件或远程目录不存在")


# 发布
def ExecRelease():
    try:
        BackUpTheOriginalFile(DTPath, sys.argv[-1])
        ExecUploadAndDownloadFile(sys.argv[-1])
        ConntionInfo.ConntionSSH(StartServiceCmd)
    except TimeoutError:
        print("请检查网络连接是否良好")


# 获取所有数据库列表
def GetAllDBList(sql):
    global outmsg
    db = pymysql.connect(Conection.IP, 'root', Conection.MyPass)
    cursor = db.cursor()
    cursor.execute(sql)
    outmsg = cursor.fetchall()



if len(sys.argv) > 1:
#获取用户传入的最后一个参数是否为scp
    if sys.argv[-1] == "scp":
        Conection = ConntionInfo(sys.argv[1])
        try:
            DefineVariablesBasedOnUserInput()
            OutFile = "\n%s %s Upload %s in %s" % (time.strftime("%Y%m%d %H:%M"), Target_name, Domain.split("/")[0], Conection.IP)
            Conection.LogWrite(OutFile)
        except KeyboardInterrupt:
            print ("退出")
            sys.exit()
        ExecUploadAndDownloadFile(sys.argv[-1])
    # 获取用户传入的最后一个参数是否为java
    elif sys.argv[-1] == "java":
        Conection = ConntionInfo(sys.argv[1])
        DefineVariablesBasedOnUserInput()
        StartServiceCmd = "%s\"sed -i 's/PyOps/%s/g' %s && cd %s%s && sh restart.sh && chown -R www.www %s%s\"" % (ROOT_User,Target_name,ReStart, Conection.Project_Path, Domain, Conection.Project_Path, Domain)
        ExecRelease()
    #获取用户传入的最后一个参数是否为hp
    elif sys.argv[-1] == "hp":
        Conection = ConntionInfo(sys.argv[1])
        DefineVariablesBasedOnUserInput()
        if "zip" in Target_name:
            StartServiceCmd = "%s\" cd %s%s && rm -rf static index.html && unzip -o %s && if [ ! -d %s/%s ];then mv %s/* ./ && rm -rf %s* && chown -R www.www %s%s;else mv %s/%s/* ./ && rm -rf %s* && chown -R www.www %s%s;fi\"" % (ROOT_User, Conection.Project_Path, Domain, Target_name, Target_name.split(".")[0], Target_name.split(".")[0],Target_name.split(".")[0], Target_name.split(".")[0], Conection.Project_Path, Domain, Target_name.split(".")[0],Target_name.split(".")[0], Target_name.split(".")[0], Conection.Project_Path, Domain)
        else:
            StartServiceCmd = "%s\" cd %s%s && tar zxf %s && if [ ! -d %s/%s ];then mv %s/* ./ && rm -rf %s* && chown -R www.www %s%s;else mv %s/%s/* ./ && rm -rf %s* && chown -R www.www %s%s;fi\"" % (ROOT_User, Conection.Project_Path, Domain, Target_name, Target_name.split("_")[0], Target_name.split("_")[0],Target_name.split("_")[0], Target_name.split("_")[0],Conection.Project_Path, Domain, Target_name.split("_")[0],Target_name.split("_")[0], Target_name.split("_")[0], Conection.Project_Path, Domain)
            print (StartServiceCmd)
        ExecRelease()
    #获取用户传入的最后一个参数是否为mb
    elif sys.argv[-1] == "mb":
        Conection = ConntionInfo(sys.argv[1])
        SystemVariables()
        SqlCmd = "show databases"
        GetAllDBList(SqlCmd)
        print("开始备份")
        for Format in outmsg:
            MD = "%s" % (Format)
            global MyBackup_Path
            if MD in ('information_schema','mysql','performance_schema'):
                continue
            else:
                MyBackup_Path = "%smysql/" % (Conection.Backup_Path)
                DumpCmd = "mysqldump -u root -p%s %s > %s%s/%s_%s.sql" % (Conection.MyPass, MD, MyBackup_Path, DATE, MD, DATE)
                StartInputSqlCmd = "%s\"if [ -d %s%s/ ];then %s;else mkdir -p %s%s/ && %s;fi\"" % (ROOT_User, MyBackup_Path, DATE, DumpCmd, MyBackup_Path, DATE, DumpCmd)
                TarPackCmd = "%s\"cd %s && tar zcf sql_%s.tar.gz %s\"" % (ROOT_User, MyBackup_Path, DATE, DATE)
                ConntionInfo.ConntionSSH(StartInputSqlCmd,TarPackCmd)
        print ("数据库已经备份在",MyBackup_Path,DATE,".tar.gz")
        OutFile = "\n%s 备份数据库 %s" % (time.strftime("%Y%m%d%H%M"), Conection.IP)
        Conection.LogWrite(OutFile)
    #程序交互式下载
    elif sys.argv[-1] == "dl":
        Conection = ConntionInfo(sys.argv[1])
        try:
            DefineVariablesBasedOnUserInput()
            OutFile = "\n%s %s Download %s in %s" % (time.strftime("%Y%m%d %H:%M"), Target_name, Domain.split("/")[0], Conection.IP)
            Conection.LogWrite(OutFile)
        except KeyboardInterrupt:
            print("退出")
            sys.exit()
        ExecUploadAndDownloadFile(sys.argv[-1])
    #输入目标目录文件名称打包下载
    elif sys.argv[-1] == "dlf":
        Conection = ConntionInfo(sys.argv[1])
        try:
            DefineVariablesBasedOnUserInput()
            OutFile = "\n%s Download %s.tar.gz in %s" % (time.strftime("%Y%m%d %H:%M"), Domain.split("/")[0], Conection.IP)
            Conection.LogWrite(OutFile)
        except KeyboardInterrupt:
            print("退出")
            sys.exit()
        ExecUploadAndDownloadFile(sys.argv[-1])
    # 命令行式目标目录文件名称打包下载
    elif sys.argv[1] == "dlf":
        Conection = ConntionInfo(sys.argv[2])
        try:
            DefineVariablesBasedOnUserInput()
            OutFile = "\n%s Download %s_%s.tar.gz in %s" % (time.strftime("%Y%m%d %H:%M"), Domain.split("/")[0],time.strftime("%Y%m%d%H%M"), Conection.IP)
            Conection.LogWrite(OutFile)
        except KeyboardInterrupt:
            print("退出")
            sys.exit()
        ExecUploadAndDownloadFile(sys.argv[1])
    #命令行式下载
    elif sys.argv[1] == "dl":
        Conection = ConntionInfo(sys.argv[2])
        SystemVariables()
        DTPath = " %s%s/" % (Conection.Backup_Path, DATE)
        Domain = "%s/" % (sys.argv[3])
        WPath = "%s%s/%s" % (Conection.Source_Path,time.strftime("%Y%m%d%H%M"),sys.argv[4])
        WRPath = "%srestart.sh" % (Conection.Source_Path)
        Target_name = sys.argv[5]
        LPath = "%s%s%s" % (Conection.Project_Path, Domain, Target_name)
        ReStart = "%s%srestart.sh" % (Conection.Project_Path, Domain)
        OutFile = "\n%s %s Download %s in %s" % (time.strftime("%Y%m%d %H:%M"), Target_name, Domain.split("/")[0], Conection.IP)
        Conection.LogWrite(OutFile)
        ExecUploadAndDownloadFile(sys.argv[1])
#如果都不等于就退出
    else:
        Conection = ConntionInfo(sys.argv[1])
        SystemVariables()
        OutFile = "\n%s No Exec error %s" % (time.strftime("%Y%m%d %H:%M"), sys.argv[2:])
        Conection.LogWrite(OutFile)
        Outsg = "Usage:\n    python %s  <groupID> <java|hp|mb|scp|dl|dlf>\n\n No such option: %s" % (sys.argv[0], sys.argv[2:])
        Conection.Message_Box('PyOps', Outsg, 'warning')
        sys.exit()
else:
    Conection = ConntionInfo('')
    SystemVariables()
    OutFile = "\n%s No Exec error %s" % (time.strftime("%Y%m%d %H:%M"), sys.argv[2:])
    Conection.LogWrite(OutFile)
    Outsg = "Usage:\n    python %s  <groupID> <java|hp|mb|scp|dl|dlf>\n\n No such option: %s" % (sys.argv[0],sys.argv[2:])
    Conection.Message_Box('PyOps',Outsg,'warning')
    sys.exit()

#正常执行后输出完毕
if sys.argv[-1] != "no":
    if os.name == "nt":
        Conection.Message_Box('PyOps',"任务完成","info")
    else:
        print("任务完成")