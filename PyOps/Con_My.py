#coding:gbk

import pymysql
from Adjustment import ConntionInfo
Connection = ConntionInfo('test')
print (Connection.IP,Connection.MyPass)
db = pymysql.connect(Connection.IP, 'root', 'Zxx123456!')
cursor = db.cursor()
sql = "show databases"
cursor.execute(sql)
outmsg = cursor.fetchall()
for i in outmsg:
    a = "%s" % (i)
    print (a)
# �ر����ݿ�����
cursor.close()
db.close()