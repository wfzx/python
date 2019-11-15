from django.shortcuts import redirect,render
from django.contrib import messages
from login.admin import check_user
import shutil

@check_user
def MV(request):
    if request.method == 'POST':
        source = request.POST['source']
        target = request.POST['target']
        if source and target:
            shutil.move(source,target)
            return redirect("/move",messages.success(request,"移动完成"))
        else:
            return redirect("/move",messages.error(request,"请正确输入路径"))
    else:
        return render(request,"move/mv.html")