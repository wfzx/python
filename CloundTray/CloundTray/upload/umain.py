from django.shortcuts import render,redirect
from login.admin import check_user
from django.contrib import messages
from login import models
import os

@check_user
def upload_file(request):
    if request.method == "POST":
        File = request.FILES.get("myfile", None)
        if File is None:
            return redirect("/upload", messages.error(request, '请选择要上传的文件！！！'))
        else:
            if request.POST['dir'] == '':
                return redirect("/upload", messages.error(request, '请输入上传路径！！！'))
            else:
                dir = request.POST['dir']
                if '/' in str(dir):
                    user = str(dir).split('/')[0]
                else:
                    user = str(dir).split()[0]
                if request.session["login_user"] != 'zxx':
                    if request.session["login_user"] != user:
                        return redirect("/upload", messages.error(request, '你没有该目录的上传权限！！！'))
                if os.path.isdir("/data/server/Clound/%s" % request.POST['dir']) != True:
                    os.makedirs("/data/server/Clound/%s" % request.POST['dir'])
                with open("/data/server/Clound/%s/%s" % (request.POST['dir'],File.name), 'wb+') as f:
                    for chunk in File.chunks():
                      f.write(chunk)
                return redirect("/upload", messages.error(request, '上传完成 访问https://www.mnonn.com/download/%s查看！！！' % request.POST['dir']))
    else:
        user_obj = models.User.objects.filter(name=request.session.get('login_user')).first()
        if user_obj:
            return render(request, "upload/upload.html")
        else:
            request.session["login_user"] = ""
            return redirect('/', messages.error(request, "请重新登录"))