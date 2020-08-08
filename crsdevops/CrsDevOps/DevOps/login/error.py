from django.shortcuts import redirect
from django.contrib import messages

def cw_404(request):
    return redirect("/",messages.error(request,r"Error\n页面丢失"))

def cw_500(request):
    return redirect("/",messages.error(request,r"Error\n页面超时"))