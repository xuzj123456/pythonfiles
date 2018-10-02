# coding=utf-8
import requests, re, os
from tools.clock import Clock
from multiprocessing import Pool
from spider.urls import *


class Thu_spider:
    failed_num = 0
    root = r'F:\new'
    headers = {
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/68.0.3440.106 Safari/537.36'
    }
    def __init__(self, url):
        self.url = url

    def download_func(self):
        print('正在处理 %s' % self.url)
        self.req = requests.get(self.url, headers=self.headers)
        self.html = self.req.text
        self.target_url = re.findall(r'data-quality="(.*?)">...P</a></li>', self.html)[-1]
        print('video url ' + self.target_url)

        self.path = os.path.join(self.root, self.url.split('/')[-1]) + '   ' + str(self.target_url.split('/')[-2]) + '.mp4'
        if not os.path.exists(self.path):
            self.save_func()
            self.check_repeat()
        else:
            print('**********   %s文件已存在   **************' % self.url)

    def save_func(self):
        self.video_page = requests.get(self.target_url, headers=self.headers)
        with open(self.path, 'wb') as f:
            f.write(self.video_page.content)
            f.close()

    def check_repeat(self):
        self.file_name = str(self.target_url.split('/')[-2]) + '.mp4'
        if self.file_name in os.listdir(r'F:\delete'):
            os.remove(os.path.join(r'F:\delete', self.file_name))

    def run_func(self):
        try:
            self.download_func()
            print('url %s has done successfully.' % self.url)
        except Exception as e:
            print('*********  url %s failed   *************' % self.url)
            print(e)
            Thu_spider.failed_num += 1

def run(url):
    s = Thu_spider(url)
    s.run_func()

def main():
    clock = Clock()
    clock.Start()

    Thu_spider.failed_num = 0

    p = Pool(4)

    for url in urls_1:
        p.apply_async(run, args=(url,))

    print('共失败%d次' % Thu_spider.failed_num)
    p.close()
    p.join()



    clock.End()
    clock.Time()

if __name__ == '__main__':
    main()
