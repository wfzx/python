from mail.views import Email
from django.shortcuts import render
from login import models as ls

def GetAllEmailAddressOrSendMail(request):
    if request.method == 'POST':
        Title = request.POST['title']
        MailBody = request.POST['MailBody']
        ToUser = request.POST.getlist('ToUser')
        if 'all' in ToUser:
            MailAddress = []
            for i in range(0, len(ls.User.objects.values_list('email', flat=True))):
                email = ls.User.objects.values_list('email', flat=True)[i]
                MailAddress.append(email)
            mail = Email(MailAddress,Title,MailBody)
            mail.SendMail()
        else:
            MailAddress = []
            for User in range(0,len(ToUser)):
                email = ls.User.objects.filter(name=ToUser[User]).values_list('email' ,flat=True).first()
                MailAddress.append(email)
            mail = Email(MailAddress, Title, MailBody)
            mail.SendMail()
        ToUserDash = {}
        GetUserList = ls.User.objects.values_list('name', flat=True)
        for t in range(0, len(GetUserList)):
            ToUserDash[t] = [GetUserList[t]]
        return render(request, 'views/邮件.html', {'ToUserDash': ToUserDash})
    else:
        ToUserDash = {}
        GetUserList = ls.User.objects.values_list('name', flat=True)
        for t in range(0,len(GetUserList)):
            ToUserDash[t] = [GetUserList[t]]
        return render(request,'views/邮件.html',{'ToUserDash':ToUserDash})