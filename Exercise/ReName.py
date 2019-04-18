#coding:gbk

import os

#要搜索的目录
job_path = r'D:\zhuxiaoxuan\所有公司代码\项目整理'
dir = os.listdir(job_path)


for i in range(0,len(dir)):
    wzdirname = "%s\%s" % (job_path,dir[i])
    #是否为目录
    # if os.path.isdir(wzdirname):
    #是否包含在字符串中
    if "徐旭峰" in wzdirname:
        renamedirname = "%s" % (wzdirname)
        print (renamedirname)
        # os.rename(wzdirname,renamedirname)
    else:
        os.chdir(wzdirname)
        list_dir = os.listdir(wzdirname)
        for t in range(0,len(list_dir)):
            list_wzdirname = "%s\%s" % (wzdirname,list_dir[t])
            if "徐旭峰" in list_wzdirname:
                print(list_wzdirname)
