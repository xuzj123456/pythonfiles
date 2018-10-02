# coding=utf-8
import requests
import re
import os
import time

time_start = time.time()

url = 'https://thumbzilla.sitescrack.site/video/ph5b47cde821320/chinese-femdom-facesitting-ass-licking-handjob'

headers = {
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/68.0.3440.106 Safari/537.36'
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
