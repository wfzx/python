#coding:gbk

import os

#要搜索的目录
job_path = r'D:\zhuxiaoxuan'
dir = os.listdir(job_path)

for i in range(0,len(dir)):
    wzdirname = "%s\%s" % (job_path,dir[i])
    #是否为目录
    if os.path.isdir(wzdirname):
        renamedirname = "%s-test" % (wzdirname)
        # print (renamedirname)
        os.rename(wzdirname,renamedirname)