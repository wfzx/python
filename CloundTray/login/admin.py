from django.shortcuts import render,redirect
from django.contrib import messages
from . import models,md5
from mail.views import Email
import random,time

def check_user(func):
    def inner(*args,**kwargs):
        username = args[0].session.get("login_user","")
        if username == "":
            args[0].session["path"] = args[0].path
            return redirect("/")
        return func(*args,**kwargs)
    return inner

class verCode(object):
    def __init__(self):
        self.str = ""
        for i in range(6):
            ch = chr(random.randrange(ord('0'), ord('9') + 1))
            self.str += ch

    def timeOneS(self,request):
        if request.session.get("invita_time"):
            CurTimeStamp = time.time()
            TimeStamp = request.session.get("invita_time")
            JatLag = int(CurTimeStamp) - int(TimeStamp)
            if JatLag < 60 :
                RemTime = 60 - JatLag
                return messages.error(request,"请%s后重试" % RemTime)

    def Sendmail(self,request):
        models.VerCode.objects.create(code=self.str).save()
        email = request.GET['m']
        mail = Email(email,self.str)
        mail.SendCode()
        request.session["invita_code"] = self.str
        request.session["invita_time"] = time.time()

def login(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']
        md5password = md5.HashPass(password)
        user_obj = models.User.objects.filter(name=username,password=md5password).first()
        if user_obj:
            request.session["login_user"] = username
            return render(request,'index.html')
        else:
            return redirect("/",messages.error(request,"用户名密码错误"))
    else:
        if request.session.get("login_user"):
            user_obj = models.User.objects.filter(name=request.session.get('login_user')).first()
            if user_obj :
                return render(request, "index.html")
            else:
                request.session["login_user"] = ""
                return redirect('/',messages.error(request,"请重新登录"))
        else:
            return render(request,"login/dl.html")

def zc(request):
    if request.method == 'POST':
        username = request.POST['name']
        sex = request.POST['sex']
        email = request.POST['m']
        password = request.POST['password']
        repassword = request.POST['repassword']
        md5password = md5.HashPass(password)
        invitacode = request.POST['invita']
        invitavercode = request.POST['code']
        if request.POST['tj'] == '获取验证码':
            return redirect("/login?m=%s&c=1" % email)
        if username and password and repassword and sex and email and invitavercode:
            if len(password) < 6:
                return redirect("/login?m=%s&c=2",messages.error(request,"密码长度小于6位"))
            if password.isdigit():
                return redirect("/login?m=%s&c=2",messages.error(request,"密码不能为纯数字"))
            if password.isalpha():
                return redirect("/login?m=%s&c=2", messages.error(request, "密码不能为纯字母"))
            if password == repassword:
                user_obj = models.User.objects.filter(name=username).first()
                if user_obj:
                    return redirect("/login?m=%s&c=2",messages.error(request,'用户已存在'))
                else:
                    DupQuery = models.Invita.objects.filter(invitacode=invitacode).exists()
                    if DupQuery != True:
                        return redirect("/login?m=%s&c=2",messages.error(request,'邀请码不存在'))
                    else:
                        CodeQuery = models.Invita.objects.filter(invitacode=invitacode, invitaname=None).exists()
                        if CodeQuery != True:
                            return redirect('/login?m=%s&c=2', messages.error(request, "当前邀请码已被使用"))
                        VerCodeQuery = models.VerCode.objects.filter(code=invitavercode).exists()
                        if VerCodeQuery != True:
                            return redirect('/login?m=%s&c=2', messages.error(request, "验证码错误"))
                        VerCodeQueryExists =  models.VerCode.objects.filter(code=invitavercode,name=None).exists()
                        if VerCodeQueryExists != True:
                            return redirect('/login?m=%s&c=2', messages.error(request, "验证码已被使用"))
                        try:
                            models.User.objects.create(name=username,password=md5password,email=email,sex=sex).save()
                            models.Invita.objects.filter(invitacode=invitacode).update(invitaname=username,invitavercode=invitavercode)
                            models.VerCode.objects.filter(code=invitavercode).update(name=username,recode=invitavercode)
                        except:
                            return redirect('/login?m=%s&c=2',messages.error(request,"注册失败，邮箱以被使用"))
                        return redirect('/',messages.success(request,"注册成功"))
            else:
                return redirect("/login?m=%s&c=2",messages.error(request,'两次密码不一致'))
        else:
            return redirect("/login?m=%s&c=2",messages.error(request,'不能有空项'))
    else:
        if request.session.get("login_user"):
            request.session["login_user"] = ""
            return redirect("/")
        else:
            email = request.GET['m']
            if request.GET['c'] == '1':
                code = verCode()
                code.timeOneS(request)
                code.Sendmail(request)
                return redirect("/login?m=%s&c=2" % email)
            else:
                return render(request, "login/zc.html")
