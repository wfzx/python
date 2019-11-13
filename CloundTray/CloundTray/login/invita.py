from django.shortcuts import redirect,render
from django.contrib import messages
from .admin import check_user
from login import models
import random,time

def Num():
    global str
    str = ""
    for i in range(6):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        str += ch
    return str

@check_user
def RanNum(request):
    user_obj = models.User.objects.filter(name=request.session.get('login_user')).first()
    if user_obj == None:
        request.session["login_user"] = ""
        return redirect('/', messages.error(request, "请重新登录"))
    if request.session.get("invita_time"):
        CurTimeStamp = time.time()
        TimeStamp = request.session.get("invita_time")
        JatLag = int(CurTimeStamp) - int(TimeStamp)
        if JatLag < 60 :
            RemTime = 60 - JatLag
            return redirect('/',messages.error(request,"请%s后重试" % RemTime))
    Num()
    DupQuery = models.Invita.objects.filter(invitacode=str).exists()
    while DupQuery:
        Num()
        DupQuery = models.Invita.objects.filter(invitacode=str).exists()
    username = request.session.get("login_user")
    models.Invita.objects.create(name=username,invitacode=str).save()
    request.session["invita_code"] = str
    request.session["invita_time"] = time.time()
    return redirect("/",messages.success(request,str))