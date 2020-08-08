import smtplib
from email.mime.text import MIMEText

class Email(object):
    def __init__(self,recv,Title,body):
        self.mailserver = "hwsmtp.exmail.qq.com"
        self.username_send = "zhuxiaoxuan@gongguizhijia.com"
        self.password = "Zxax1998"
        self.username_recv = recv
        self.mail = MIMEText(body)
        self.mail['Subject'] = Title
        self.mail['From'] = 'CrsDevOps'
        self.mail['To'] = ','.join(self.username_recv)

    def SendMail(self):
        smtp = smtplib.SMTP_SSL(self.mailserver, port=465)
        smtp.login(self.username_send, self.password)
        smtp.sendmail(self.username_send, self.username_recv, self.mail.as_string())