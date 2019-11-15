import smtplib
from email.mime.text import MIMEText

class Email(object):
    def __init__(self,recv,verCode):
        self.mailserver = "smtp.163.com"
        self.username_send = "m18538209483@163.com"
        self.password = "zxax19981227"
        self.username_recv = recv
        self.mail = MIMEText('验证码为:%s' % verCode)
        self.mail['Subject'] = 'Mnonn网站'
        self.mail['From'] = self.username_send
        self.mail['To'] = self.username_recv

    def SendCode(self):
        smtp = smtplib.SMTP_SSL(self.mailserver, port=465)
        smtp.login(self.username_send, self.password)
        smtp.sendmail(self.username_send, self.username_recv, self.mail.as_string())