from Alter import models
import requests

def WebHookAlter(request):
    Address = models.WebHook.objects.filter(Belong='PT').values_list('Address',flat=True).first()
    RequestMethod = models.WebHook.objects.filter(Belong='PT').values_list('RequestMethod',flat=True).first()
    RequestHeader = models.WebHook.objects.filter(Belong='PT').values_list('RequestHeader',flat=True).first()
    Template = models.WebHook.objects.filter(Belong='PT').values_list('Template',flat=True).first()
    print(RequestHeader)
    if RequestMethod == 'POST':
        requests.post(url=Address, headers=RequestHeader,json=Template)