from django.shortcuts import render,redirect

def Alter(request):
    if request.method == 'POST':
        pass
    else:
        return render(request,'views/告警页.html')