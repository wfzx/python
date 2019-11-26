import requests

zm = list(map(chr, range(ord('a'), ord('z') + 1)))
num = 1
for i in range(len(zm)):
    one = zm[i]
    for t in range(len(zm)):
        two = zm[t]
        for th in range(len(zm)):
            there = zm[th]
            for f in range(len(zm)):
                four = zm[f]
                print('%s: %s%s%s%s.com' % (num,one,two,there,four))
                num = num + 1
                domain = "%s%s%s%s.com" % (one,two,there,four)
                url = "查询地址"
                status = requests.get(url)
                code = status.status_code
                if code != 200:
                    file = open('domain.txt','a')
                    file.write("该域名未注册%s" % (domain))
                    file.close()

