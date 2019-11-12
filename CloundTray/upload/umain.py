from django.shortcuts import render
from login.admin import check_user
import os

@check_user
def upload_file(request):
    if request.method == "POST":
        File = request.FILES.get("myfile", None)
        if File is None:
            return render(request,"upload/noupload.html")
        else:
            if request.POST['dir'] == '':
                return render(request,"path/nopath.html")
            else:
                if os.path.isdir("/data/server/Clound/%s" % request.POST['dir']) != True:
                    os.makedirs("/data/server/Clound/%s" % request.POST['dir'])
                with open("/data/server/Clound/%s/%s" % (request.POST['dir'],File.name), 'wb+') as f:
                    for chunk in File.chunks():
                      f.write(chunk)
                return render(request,"upload/yesupload.html")
    else:
        return render(request, "upload/upload.html")