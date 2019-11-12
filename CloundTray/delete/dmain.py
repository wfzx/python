from django.shortcuts import render
from login.admin import check_user
import os,shutil

@check_user
def delete_file(request):
    if request.method == "POST":
        if request.POST['dir'] == '':
            return render(request,"delete/nodelete.html")
        else:
            dir = request.POST['dir']
            if '/' in str(dir):
                user = str(dir).split('/')[0]
            else:
                user = str(dir).split()[0]
            if request.session["login_user"] != 'zxx':
                if request.session["login_user"] != user:
                    return render(request, "delete/noadelete.html")
            path = "/data/server/Clound/%s" % request.POST['dir']
            if os.path.isfile(path) != True:
                if os.path.isdir(path) != True:
                    return render(request,"delete/nodelete.html")
                else:
                    shutil.rmtree(path)
            else:
                os.remove(path)
            return render(request, "delete/yesdelete.html")
    else:
        return render(request,"delete/delete.html")