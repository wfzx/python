#coding:utf-8
import requests,re

i = 0


def KeywordRank(searchTxt, webUrl):
    global i
    pattern = re.compile(r'class="c-showurl" style="text-decoration:none;">(.*?)&nbsp', re.S)
    result = pattern.findall(searchTxt)
    for item in result:
        i = i + 1
        file = open(r'C:\Users\Administrator\Desktop\out.txt', 'a')
        file.writelines('域名地址 %d: %s\n' % (i, item))
        file.close()
        if webUrl in item:
            return i
    return None


# content:要搜索的关键词, page:要搜索的页码
def BaiduSearch(domain,content, page):
    url = u"%s/s?wd=%s" % (domain,content)
    data = requests.get(url)
    return data.content.decode().strip()


if __name__ == "__main__":
    loops = 100 # 最多查多少页
    page = 0
    domain = input("请输入搜素网址:")
    while (loops):
        searchTxt = BaiduSearch(domain,"mnonn",page)
        page = page + 1
        rank = KeywordRank(searchTxt, "henliy.com")
        if None != rank:
            file = open(r'C:\Users\Administrator\Desktop\out.txt','a')
            file.writelines('输入的关键词排在第 %d 名\n' % rank)
            file.close()
            break
        loops = loops - 1
