#coding:gbk

import os

#Ҫ������Ŀ¼
job_path = r'D:\zhuxiaoxuan\���й�˾����\��Ŀ����'
dir = os.listdir(job_path)


for i in range(0,len(dir)):
    wzdirname = "%s\%s" % (job_path,dir[i])
    #�Ƿ�ΪĿ¼
    # if os.path.isdir(wzdirname):
    #�Ƿ�������ַ�����
    if "�����" in wzdirname:
        renamedirname = "%s" % (wzdirname)
        print (renamedirname)
        # os.rename(wzdirname,renamedirname)
    else:
        os.chdir(wzdirname)
        list_dir = os.listdir(wzdirname)
        for t in range(0,len(list_dir)):
            list_wzdirname = "%s\%s" % (wzdirname,list_dir[t])
            if "�����" in list_wzdirname:
                print(list_wzdirname)
