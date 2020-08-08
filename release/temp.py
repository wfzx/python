import requests
import json
# 0000001
domain = "http://47.106.123.30:8070/app/api/usercompany/getById"
parameter = "companyType=3&id=14&key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJBUFAiLCJpc3MiOiJTZXJ2aWNlIiwiZXhwIjoxNjU3ODcxOTUyLCJpYXQiOjE1OTQ3OTk5NTIsInRva2VuIjoiMTU5NDc5OTk1MjE1NSJ9.z2ybybbZv73BFzcghjIgAzCuJGk7MheK2-0IbSVv0Cw"

url = "%s?%s" % (domain,parameter)

re = requests.post(url)
data = re.json()

json_str = json.dumps(data)
data1 = json.loads(json_str)
if data1["msg"] == "查询数据不存在":
    print("不存在")
else:
    data2 = data1["data"]
    imagesAddress = "http://p5thuz78a.bkt.clouddn.com/"
    if 'companyName' in data2.keys():
        mingcheng = data2["companyName"]
    else:
        mingcheng = ''
    if 'contacts' in data2.keys():
        lianxiren = data2["contacts"]
    else:
        lianxiren = ''
    if 'address' in data2.keys():
        dizhi = data2["address"]
    else:
        dizhi = ''
    if 'repairTypeName' in data2.keys():
        xiulichexing = data2["repairTypeName"]
    else:
        xiulichexing = ''
    if 'repairScopeName' in data2.keys():
        xiulifanwei = data2["repairScopeName"]
    else:
        xiulifanwei = ''
    if 'images' in data2.keys():
        images = "%s%s" % (imagesAddress,data2["images"])
    else:
        images = ''
    if 'mobile' in data2.keys():
        shoujihao = data2["mobile"]
    else:
        shoujihao = ''
    if 'mobile2' in data2.keys():
        shoujihao2 = data2["mobile2"]
    else:
        shoujihao2 = ''
    if 'mobile3' in data2.keys():
        shoujihao3 = data2["mobile3"]
    else:
        shoujihao3 = ''
    print("名称： %s\n联系人： %s\n地址： %s\n修理车型： %s\n修理范围： %s\n电话1： %s\n电话2： %s\n电话3： %s\n图片： %s" % (
        mingcheng,lianxiren,dizhi,xiulichexing,xiulifanwei,shoujihao,shoujihao2,shoujihao3,images
    ))