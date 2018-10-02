# coding=utf-8
# 仅能爬五分钟以内视频
import os

try:
    url = 'https://www.bilibili.com/video/av31196004'
    filename = url.strip('/')
    path = 'F://'
    info = os.system("you-get -o {} -O {} {}".format(path, filename, url))

except Exception as e:
    print(e)