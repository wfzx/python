#coding:gbk

import os

#Ҫ������Ŀ¼
job_path = r'D:\zhuxiaoxuan'
dir = os.listdir(job_path)

for i in range(0,len(dir)):
    wzdirname = "%s\%s" % (job_path,dir[i])
    #�Ƿ�ΪĿ¼
    if os.path.isdir(wzdirname):
        renamedirname = "%s-test" % (wzdirname)
        # print (renamedirname)
        os.rename(wzdirname,renamedirname)