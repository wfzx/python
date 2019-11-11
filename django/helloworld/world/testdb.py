from django.http import HttpResponse
from TestMode1.models import Test


def testdb(request):
    # test1 = Test(name='SuExamy')
    # test1.save()
    # return HttpResponse("<p>数据添加成功!</p>")
    #查看表中所有数据
    # response = ""
    # response1 = ""
    # list = Test.objects.all()
    # for var in list:
    #     response1 += var.name + " "
    # response = response1
    # return HttpResponse("<p> %s </p>" % (response))
    #更新数据
    # test1 = Test.objects.get(id=2)
    # test1.id = '1'
    # test1.save()
    # return HttpResponse("<p>更新成功</p>")
    #删除数据
    test1 = Test.objects.get(id=2)
    test1.delete()
    return HttpResponse("<p>删除成功</p>")