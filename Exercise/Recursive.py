#coding:gbk

import os,shutil,re

def search(root, target,lx='mo'):
    global path,IP,domain
    try:
        items = os.listdir(root)
        for item in items:
            path = os.path.join(root, item)
            if os.path.isdir(path):
                if lx == "copy":
                    search(path,target,"copy")
                else:
                    search(path, target)
            elif path.split('\\')[-1] == target:
                print("Path:",path)
                with open(path, 'rb') as text:
                    words = text.read().split()
                    for word in words:
                        if "http://" in word.decode().strip() or "https://" in word.decode().strip():
                            domain = word.decode().strip().split("/")[2]
                            if domain == "http:":
                                domain = word.decode().strip().split("/")[4]
                            pattern = re.compile('[0-9]')
                            match = pattern.findall(domain)
                            if "\"" in domain:
                                ydomain = domain.split("\"")[0]
                                import socket
                                try:
                                    print("Domain:",ydomain)
                                    myaddr = socket.getaddrinfo(ydomain, 'http')
                                    IP = myaddr[0][4][0]
                                except socket.gaierror:
                                    print("No parsing record")
                            elif match:
                                break
                            else:
                                import socket
                                try:
                                    print("Domain:", domain)
                                    myaddr = socket.getaddrinfo(domain, 'http')
                                    IP = myaddr[0][4][0]
                                except socket.gaierror:
                                    print("Adress:No parsing record\n")
                                    break
                            if IP == "39.98.179.202":
                                print("Adress:%s\n" % (IP))
                            elif IP == "47.93.223.92":
                                print("Adress:%s" % (IP))
                                if os.path.isdir(os.path.join(HomePath,domain)):
                                    DecPath = path.split(path.split("\\")[5])[0]
                                    print ("HomePath:%s" % (os.path.join(HomePath,domain)))
                                    if os.path.isdir(os.path.join(DecPath,domain)) == False:
                                        print ("Status:copy...")
                                        if lx == "copy":
                                            shutil.copytree(os.path.join(HomePath,domain),os.path.join(DecPath,domain))
                                        print ("Success")
                                    else:
                                        print("DecPath:%s existed\n" % (os.path.join(DecPath,domain)))
                                else:
                                    print("HomePath:None\n")
                            else:
                                print("Adress:%s\n"% (IP))
                            break
    except FileNotFoundError:
        print ("Path:%s\nDomain:None\nAdress:None\n" % (path))

HomePath = r"D:\zhuxiaoxuan\92_wwwroot\wwwroot"
source = r"D:\zhuxiaoxuan\所有公司代码\项目整理"
search(source,'Constant.java')