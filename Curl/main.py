#-*- coding:utf-8 -*-

import sys,requests
def GetUrlStatusCode(url):
    try:
        request = requests.get(url)
        httpstatuscode = request.status_code
        return httpstatuscode
    except requests.exceptions.ConnectionError:
        return 1
    except requests.exceptions.MissingSchema:
        return requests.exceptions.MissingSchema

url = str(input("Please Enter Check Url :"))

if url[0:7] != 'http://':
    if url[0:8] != 'https://':
        print ('Please in Domain Add http:// or https://')
        sys.exit(0)

Code = GetUrlStatusCode(url)
if Code == 1:
    print ('The domain name entered is incorrect : %s' % (url))
    sys.exit(0)
else:
    print (Code)

