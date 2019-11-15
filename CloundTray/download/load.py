from django.shortcuts import render,redirect
from login.admin import check_user
from django.http.response import FileResponse
import os

def file(request,dir):
    if os.path.isfile(dir):
        filename = request.path_info.split('/')[-1]
        file = open(dir, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=%s' % (filename)
        return response


@check_user
def TOC(request):
    global mu,root,username,olduser
    root = r'C:\Users\Administrator\Desktop\test\source'
    username = request.session["old_login_user"]
    pathname = request.path_info.split('download/')[-1]
    filename = pathname[:-1]
    if pathname == "/":
        return redirect("/download/")
    if "/download/" == request.path_info:
        dir = "%s/%s" % (root,username)
        file(request, dir)
        id = request.GET.get('id')
        print(id)
        if id != "1":
            mu = os.listdir(dir)
            mu.insert(0, "../")
            return render(request, 'download/load.html', {'TutorialList': mu})
        else:
            mu = os.listdir(root)
            request.session["dirname"] = "1"
            return render(request,'download/load.html',{'TutorialList': mu})
    else:
        if request.session["dirname"] == "1":
            request.session["dirname"] = "0"
            request.session["qt"] = "1"
            mu = os.listdir(root)
            mu.insert(0, "../")
            return render(request,"download/load.html",{'TutorialList': mu})
        else:
            if request.session["qt"] == "1":
                request.session["qt"] = "0"
                request.session["old_login_user"] = request.path_info.split("/")[3]
                return redirect("/download/")
            pathname = request.path_info.split('download/')[-1]
            if pathname == "/":
                return redirect("/download/")
            if "//" in pathname:
                first = pathname.split("//")[0]
                TheSecond = pathname.split("//")[1]
                url = "%s/%s" % (first, TheSecond)
                return redirect("/download/%s" % (url))
            dir = "%s/%s/%s" % (root, username, filename)
            file(request,dir)
            mu = os.listdir(dir)
            mu.insert(0, "../")
            return render(request, "download/load.html", {'TutorialList': mu})