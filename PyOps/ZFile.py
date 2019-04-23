#coding:gbk

import zipfile,os

def zip_ya(startdir,file_news):
    z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir,'')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename),fpath+filename)
    z.close()

startdir = r"C:\Users\Example\Desktop\zxx\pc"
file_news = "%s.zip" % (startdir)
zip_ya(startdir,file_news)