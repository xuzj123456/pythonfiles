# coding=utf-8
import requests
import re
import os
import time

time_start = time.time()

url = 'https://gs.amac.org.cn/amac-infodisc/res/pof/securities/index.html'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Upgrade-Insecure-Requests':'1',
    'Connection':'keep-alive',
    'Host':'gs.amac.org.cn',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'If-Modified-Since': 'Wed, 07 Apr 2021 11:26:39 GMT',
    'If-None-Match': r'W/"606d96ef-2ab9"',
    'sec-ch-ua': r'" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'sec-ch-ua-mobile': '?0',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
}

root = r'F:\download'

req = requests.get(url, headers=headers)
html = req.text
target_url = re.findall(r'data-quality="(.*?)">...P</a></li>', html)[-1]
print(target_url)

path = os.path.join(root, url.split('/')[-1]) + '   ' + str(target_url.split('/')[-2][:3]) + '.mp4'
if not os.path.exists(path):
    video_page = requests.get(target_url, headers=headers)
    with open(path, 'wb') as f:
        f.write(video_page.content)
        f.close()
    print('url %s has done successfully.' % url)
else:
    print('%s文件已存在' % url)

time_end = time.time()
t = time_end - time_start
print(str(t) + 's')
