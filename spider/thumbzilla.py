# coding=utf-8
import collections
import os
import re
import requests
from multiprocessing import Pool
from urllib.parse import unquote

from spider.urls import *
from tools.clock import Clock



def save_func(target_url, path):
    video_page = requests.get(target_url, headers=headers)
    with open(path, 'wb') as f:
        f.write(video_page.content)
        f.close()
# 保存

def download_func(url):
    print('正在处理 %s' % url)
    req = requests.get(url, headers=headers)
    html = req.text
    target_url = re.findall(r'data-quality="(.*?)">...P</a></li>', html)[-1]
    print('video url ' + target_url)

    path = os.path.join(root, unquote(unquote(url.split('/')[-1]))) + '   ' + str(target_url.split('/')[-2]) + '.mp4'
    # 两重unquote函数是为了将url中的编码转化
    if not os.path.exists(path):
        save_func(target_url, path)
    else:
        print('**********   %s文件已存在   **************' % url)
# 获取下载url并保存

def run_func(url):
    failed_flag = False
    try:
        download_func(url)
        print('url %s has done successfully.' % url)
    except Exception as e:
        print('<*********  url %s failed   *************' % url)
        print(e)
        failed_flag = True
    return failed_flag
# 将主体置入try except中

def run(urls):
    clock = Clock()
    clock.Start()

    p = Pool(4)

    results = []
    for url in urls:
        temp = p.apply_async(run_func, args=(url,))
        results.append(temp)

    p.close()
    p.join()

    clock.End()
    clock.Time()
    results = [r.get() for r in results]
    print('共失败%d次' % collections.Counter(results)[True])    # 每个失败都将返回一个True,统计True的个数
# 主运行函数0

root = r'E:\new'    # 文件保存位置

headers = {
    'user-agent': 'Mozilla/5.0 ,(Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/68.0.3440.106 Safari/537.36',
    'Origin': 'https://www.thumbzilla.com',
}     # requests headers

if __name__ == '__main__':
    run(urls_1)
