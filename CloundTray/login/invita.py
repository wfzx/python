from django.shortcuts import redirect
from django.contrib import messages
from .admin import check_user
from . import models
import random

def Num():
    global str
    str = ""
    for i in range(6):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        str += ch
    return str

@check_user
def RanNum(request):
    Num()
    DupQuery = models.Invita.objects.filter(invitacode=str).exists()
    while DupQuery:
        Num()
        DupQuery = models.Invita.objects.filter(invitacode=str).exists()
    username = request.session.get("login_user")
    models.Invita.objects.create(name=username,invitacode=str).save()
    request.session["invita_code"] = str
    return redirect("/",messages.success(request,str))