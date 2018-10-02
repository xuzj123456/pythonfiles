# coding=utf-8
import requests
import re

url = 'https://www.ybdu.com/xiaoshuo/8/8143/'

response = requests.get(url)
response.encoding = 'gbk'
html = response.text
# 使用gbk才不会出现乱码

title = re.findall(r'<meta property="og:title" content="(.*?)"/>', html, re.S)[0]       # 找到小说名字
# re.S表示可以找到空格、换行符等

chapter_list = re.findall(r'<li><a href="(.*?)">(.*?)</a></li>', html, re.S)        # 找到章节列表，包括各章网址与章节标题

fb = open('%s.txt' % title, 'w', encoding='gbk')

for each_chapter in chapter_list:
    chapter_url, chapter_title = each_chapter
    chapter_url = url + chapter_url

    chapter_response = requests.get(chapter_url)
    chapter_response.encoding = 'gbk'
    chapter_html = chapter_response.text
    chapter_content = re.findall(r'<div id="htmlContent" class="contentbox">(.*?)<div class="ad00"><script>show_'
                                 r'style\(\);</script></div>', chapter_html, re.S)[0]       # 获取正文内容
    chapter_content = chapter_content.replace(' ', '')
    chapter_content = chapter_content.replace('&nbsp;', '')
    chapter_content = chapter_content.replace('<br/><br/>', '\n')       # 正文内容清洗

    fb.write(chapter_title)
    fb.write(chapter_content)
    fb.write('\n\n\n')        # 每章结束后换行三次

    print(chapter_title)        # 打印章节标题以获知下载进度
