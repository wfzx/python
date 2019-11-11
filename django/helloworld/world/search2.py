from django.shortcuts import render


def search_post(request):
    ctx = {}
    if 'q' in request.POST:
        print (request.POST['q'])
        if request.POST['q'] == '':
            ctx['rlt'] = "空"
        else:
            ctx['rlt'] = request.POST['q']
    return render(request,"post.html",ctx)