使用本项目前请安装python3.7以上版本，请安装依赖模块paramiko和安装cryptography==2.4.2,然后使用install_agent.sh脚本安装agent进程

在python的安装目录找到sftp_client.py文件找到_transfer_with_callback函数替换为以下内容可实现上传下载的进度百分比，也可以使用pack下面的直接替换即可

    def _transfer_with_callback(self, reader, writer, file_size, callback):
        size = 0
        while True:
            data = reader.read(32768)
            print ("已完成:%.f%%" % (size / file_size * 100),end='\r')
            writer.write(data)
            size += len(data)
            if len(data) == 0:
                break
            if callback is not None:
                callback(size, file_size)
        print ()
        return size


以上操作也可以执行或参考install.sh来完成

主入口为main.py可按照提示进行操作

项目每次执行都会记录发布信息到logs/*.log中

配置文件介绍：
1.[]中为组名每个以[]为分割
2.每个组中包含服务器ip,username,password,home(临时上传目录),backup_path,project_path,mysql_passwd这些参数不得删除但可以传入空
3.source组为上传文件的路径只有一个source_path而且是必传项

项目使用方法：
main.py
1.命令行第一位参数为ud(upload/download)则会调用发布上传下载系列的服务然后根据服务的提示语向下一步步进行
2.命令行第一位参数为mt则会调用监控服务可选择查看单个服务器或所有服务器的当前服务器硬件信息
3.命令行第一位参数为dl则会调用下方第六点操作方法为：
python main.py dl <服务器组> <包的上级目录名称> <源包名称> <目的包名称>
4.命令行第一位参数为dlf则会调用下方第七点操作方法为：
python main.py dlf <服务器组> <需要打包的目录>
注：调用监控服务需要在被监控端安装agent安装agent的步骤本项目中会有一个agent.zip运行里面的install_agent.sh即可在安装期间如出现位置问题可自行百度解决
RUB.py
命令行第一位参数为目标服务器组名
命令行最后一位：
1.命令行最后一位参数为scp则会上传文件到指定的目录不做其他操作
2.命令行最后一位参数为java则会发布java项目
3.命令行最后一位参数为hp则会发布h5或php项目
4.命令行最后一位参数为mb则会备份当前机器的所有数据库
5.命令行最后一位参数为dl则会将目标服务器上的指定文件下载到本地的指定路径
6.命令行第一位参数为dl将会执行非交互式运行参数要求为；正确的操作方法应该调用mian.py来执行此步操作
python RUB.py dl <服务器组> <包的上级目录名称> <源包名称> <目的包名称>
7.命令行第一位参数为dlf将会执行非交互式运行参数要求为；正确的操作方法应该调用mian.py来执行此步操作
python RUB.py dlf <服务器组> <需要打包的目录>
8.命令行最后一位参数为dlf则会将目录压缩为.tar.gz后下载到本地指定目录
9.命令行最后一位参数为其他任意就会退出项目
