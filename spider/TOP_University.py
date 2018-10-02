# coding=utf-8
import requests
from bs4 import BeautifulSoup
import bs4


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return "error"


def fillUnivList(ulist, html):
    soup = BeautifulSoup(html, "lxml")
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag):     # 判断类型
            tds = tr('td')      # 所有td标签为一个列表
            ulist.append([tds[0].string, tds[1].string, tds[3].string])


def printUnivList(ulist, num):
    print("{0}\t{1:^25}\t{2:^10}".format("排名", "学校名称", "总分"))
    for i in range(num):
        u = ulist[i]
        print("%s\t%10s\t%10s" % (u[0], u[1], u[2]))


def main():
    uinfo = []
    url = 'http://www.zuihaodaxue.cn/zuihaodaxuepaiming2016.html'
    html = getHTMLText(url)
    fillUnivList(uinfo, html)
    printUnivList(uinfo, 20)


main()
