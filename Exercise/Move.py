#coding:gbk

import shutil,os

source_path = r'D:\zhuxiaoxuan\所有公司代码\整理'
mkdir_path_qb = r'D:\zhuxiaoxuan\所有公司代码\整理'

for i in range(0,len(os.listdir(source_path))):
    mkdir_path_wb = "\%s" % (os.listdir(source_path)[i].split('-')[0])
    mkdir_path = "%s%s" % (mkdir_path_qb,mkdir_path_wb)
    dec_path = "%s\%s" % (source_path,os.listdir(source_path)[i])
    # print (mkdir_path_wb)
    if os.path.isdir(mkdir_path):
        # print (1,dec_path)
        shutil.move(dec_path,mkdir_path)
    else:
        # print (dec_path,mkdir_path)
        os.mkdir(mkdir_path)
        shutil.move(dec_path, mkdir_path)


# if os.path.isdir('../PyOps'):
#     shutil.move('../abc','../abc')