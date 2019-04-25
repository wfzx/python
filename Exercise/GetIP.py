#coding:gbk

import socket


with open('../PyOps/conf/domain.conf','r') as content:
    domain =content.read().split()
    for i in range(0,len(domain)):
        # print(domain[i])
        print ("")
        if "/" in domain[i]:
            continue
        try:
            myaddr = socket.getaddrinfo(domain[i], 'http')
            IP = myaddr[0][4][0]
            print (IP)
        except socket.gaierror:
            print ("未解析")