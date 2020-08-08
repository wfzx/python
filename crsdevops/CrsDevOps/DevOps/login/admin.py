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
                request.session['yzm'] = "0"
                request.session['timeout'] = RemTime
                print("请稍后重试")

    def Sendmail(self,request):
        Title = '验证码'
        models.VerCode.objects.create(code=self.str).save()
        email = request.session['mail']
        mail = Email(email,Title,request.session['body'])
        mail.SendMail()
        request.session["invita_code"] = self.str
        request.session["invita_time"] = time.time()
        print("发送成功")

def login(request):
    request.session["yzm"] = ""
    request.session["qt"] = ""
    request.session["dirname"] = ""
    request.session["path"] = ""
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']
        md5password = md5.HashPass(password)
        user_obj = models.User.objects.filter(name=username,password=md5password).first()
        if user_obj:
            request.session["login_user"] = username
            request.session["old_login_user"] = request.session["login_user"]
            return redirect('/')
        else:
            return redirect("/",messages.error(request,"用户名密码错误"))
    else:
        if request.session.get("login_user"):
            user_obj = models.User.objects.filter(name=request.session.get('login_user')).first()
            if user_obj :
                request.session["old_login_user"] = request.session["login_user"]
                username = request.session["login_user"]
                IfAdmin = models.User.objects.filter(name=username).values_list('admin', flat=True).first()
                return render(request, "index.html",{'userName':request.session["login_user"],'IfAdmin':IfAdmin})
            else:
                request.session["login_user"] = ""
                return redirect('/',messages.error(request,"请重新登录"))
        else:
            return render(request,"login.html")

def zc(request):
    if request.method == 'POST':
        email = request.POST['m']
        if len(email) == 0:
            return redirect("/login",messages.error(request,"请填写邮件地址"))
        if request.POST['tj'] == '获取验证码':
            if models.User.objects.filter(email=email).exists():
                return redirect("/login",messages.error(request,"该邮箱已被注册"))
            print("开始发送验证码")
            request.session['yzm'] = "1"
            request.session['mail'] = request.POST['m']
            return redirect("/login",request)
        username = request.POST['name']
        sex = request.POST['sex']
        password = request.POST['password']
        repassword = request.POST['repassword']
        md5password = md5.HashPass(password)
        invitacode = request.POST['invita']
        invitavercode = request.POST['code']
        if username and password and repassword and sex and email and invitavercode:
            if len(password) < 6:
                return redirect("/login",messages.error(request,"密码长度小于6位"))
            if password.isdigit():
                return redirect("/login",messages.error(request,"密码不能为纯数字"))
            if password.isalpha():
                return redirect("/login", messages.error(request, "密码不能为纯字母"))
            if password == repassword:
                user_obj = models.User.objects.filter(name=username).first()
                if user_obj:
                    return redirect("/login",messages.error(request,'用户已存在'))
                else:
                    DupQuery = models.Invita.objects.filter(invitacode=invitacode).exists()
                    if DupQuery != True:
                        return redirect("/login",messages.error(request,'邀请码不存在'))
                    else:
                        CodeQuery = models.Invita.objects.filter(invitacode=invitacode, invitaname=None).exists()
                        if CodeQuery != True:
                            return redirect('/login', messages.error(request, "当前邀请码已被使用"))
                        VerCodeQuery = models.VerCode.objects.filter(code=invitavercode).exists()
                        if VerCodeQuery != True:
                            return redirect('/login', messages.error(request, "验证码错误"))
                        VerCodeQueryExists =  models.VerCode.objects.filter(code=invitavercode,recode=None).exists()
                        if VerCodeQueryExists != True:
                            return redirect('/login', messages.error(request, "验证码已被使用"))
                        try:
                            Date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                            models.User.objects.create(name=username,password=md5password,email=email,sex=sex,CreateTime=Date,admin=1).save()
                            models.Invita.objects.filter(invitacode=invitacode).update(invitaname=username,invitavercode=invitavercode)
                            models.VerCode.objects.filter(code=invitavercode).update(name=username,recode=invitavercode)
                        except:
                            return redirect('/login',messages.error(request,"注册失败，邮箱以被使用"))
                        return redirect('/',messages.success(request,"注册成功"))
            else:
                return redirect("/login",messages.error(request,'两次密码不一致'))
        else:
            return redirect("/login",messages.error(request,'不能有空项'))
    else:
        if request.session.get("login_user"):
            request.session.clear()
            return redirect("/")
        else:
            if request.session['yzm'] == True:
                request.session['yzm'] = ""
                return render(request, "views/用户注册.html")
            else:
                if request.session["yzm"] == '1':
                    code = verCode()
                    code.timeOneS(request)
                    if request.session["yzm"] != '0':
                        request.session['body'] = "验证码为: %s" % (code.str)
                        code.Sendmail(request)
                        request.session['yzm'] = "0"
                        return redirect("/login", messages.success(request, "验证码已发送"))
                    else:
                        return  redirect("/login",messages.error(request,"请%s秒后再次发送" % (request.session["timeout"])))
                else:
                    return render(request, "views/用户注册.html")
