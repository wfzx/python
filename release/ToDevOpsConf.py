import configparser
import requests

ConfName = "conf/dev"
conf = configparser.ConfigParser()
conf.read(ConfName)
for i in range(0,len(conf.sections())):
    t = conf.sections()[i]
    if t in ['Auth','Env','Hosts','h5']:
        continue
    else:
        ServerName = t
        Server = conf.get(t,'Server')
        Port = conf.get(t,'Port')
        MemSize = conf.get(t,'MemSize')
        CheckApi = conf.get(t,'CheckApi')
        Type = conf.get(t,'Type')
        print("Server = %s\nPort = %s\nMemSize = %s\nCheckApi = %s\nType = %s" % (Server,Port,MemSize,CheckApi,Type))
        url = "http://crsdevops.51gonggui.com/AddServer?ServerName=%s&ServerMem=%s&ServerNode=%s&CheckOps=%s&ServerPort=%s&" \
              "ServerType=%s&ResetImages=0&Env=dev&Remarks=新增服务初始化" % \
              (ServerName,MemSize,Server,CheckApi,Port,Type)
        print(url)
        requests.get(url)