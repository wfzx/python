#coding:gbk

import pymysql

db = pymysql.connect('120.78.212.211','python','Python123!','te_python')

# ʹ�� cursor() ��������һ���α���� cursor
cursor = db.cursor()

# ʹ�� execute() ����ִ�� SQL������������ɾ��
cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

# ʹ��Ԥ������䴴����
sql = """CREATE TABLE EMPLOYEE (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,  
         SEX CHAR(1),
         INCOME FLOAT )"""

cursor.execute(sql)

# �ر����ݿ�����
db.close()