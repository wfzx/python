from django.shortcuts import render

def hello(request):
    context = {}
    context['Hello'] = 'Hello World !!'
    return render(request,'hello.html',context)