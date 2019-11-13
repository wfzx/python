from django.shortcuts import render,redirect
from login.admin import check_user
from django.contrib import messages
from login import models
import os,shutil

@check_user
def delete_file(request):
    if request.method == "POST":
        if request.POST['dir'] == '':
            return redirect("/delete", messages.error(request, '请输入要删除文件的完整路径！！！'))
        else:
            dir = request.POST['dir']
            if '/' in str(dir):
                user = str(dir).split('/')[0]
            else:
                user = str(dir).split()[0]
            if request.session["login_user"] != 'zxx':
                if request.session["login_user"] != user:
                    return redirect("/delete", messages.error(request, '你没有删除该目录的权限！！！'))
            path = "/data/server/Clound/%s" % request.POST['dir']
            if os.path.isfile(path) != True:
                if os.path.isdir(path) != True:
                    return redirect("/delete", messages.error(request, '请输入要删除文件的完整路径！！！'))
                else:
                    shutil.rmtree(path)
            else:
                os.remove(path)
            return redirect("/delete", messages.error(request, '删除完成 访问https://www.mnonn.com/download查看！！！'))
    else:
        user_obj = models.User.objects.filter(name=request.session.get('login_user')).first()
        if user_obj:
            return render(request,"delete/delete.html")
        else:
            request.session["login_user"] = ""
            return redirect('/', messages.error(request, "请重新登录"))