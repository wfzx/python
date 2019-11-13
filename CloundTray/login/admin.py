from django.shortcuts import render,redirect
from django.contrib import messages
from . import models,md5

def check_user(func):
    def inner(*args,**kwargs):
        username = args[0].session.get("login_user","")
        if username == "":
            args[0].session["path"] = args[0].path
            return redirect("/")
        return func(*args,**kwargs)
    return inner

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
            return render(request, "index.html")
        else:
            return render(request,"login/dl.html")

def zc(request):
    if request.method == 'POST':
        username = request.POST['name']
        sex = request.POST['sex']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']
        md5password = md5.HashPass(password)
        invitacode = request.POST['invita']
        if username and password and repassword and sex and email:
            if password == repassword:
                user_obj = models.User.objects.filter(name=username).first()
                if user_obj:
                    return redirect("/login",messages.error(request,'用户已存在'))
                else:
                    DupQuery = models.Invita.objects.filter(invitacode=invitacode).exists()
                    if DupQuery != True:
                        return redirect("/login",messages.error(request,'邀请码不存在'))
                    else:
                        models.User.objects.create(name=username,password=md5password,email=email,sex=sex).save()
                        models.Invita.objects.filter(invitacode=invitacode).update(invitaname=username)
                        return redirect('/',messages.success(request,"注册成功"))
            else:
                return redirect("/login",messages.error(request,'两次密码不一致'))
        else:
            return redirect("/login",messages.error(request,'不能有空项'))
    else:
        if request.session.get("login_user"):
            request.session["login_user"] = ""
            return redirect("/")
        else:
            return render(request, "login/zc.html")
