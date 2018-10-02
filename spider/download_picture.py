# coding=utf-8
import requests
import os

url = ''
root = ''       # 文件保存根目录
path = root + url.split('/')[-1]        # 第二项为文件名称
if not os.path.exists(root):        # 检查根目录是否存在
    os.makedirs(root)
if not os.path.exists(path):        # 检查文件是否存在
    response = requests.get(url)
    with open(path, 'wb') as f:
        f.write(response.content)
        f.close()
        print('图片保存成功')
else:
    print('图片已存在')