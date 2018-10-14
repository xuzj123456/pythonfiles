# coding=utf-8
import os
import re

path = r'F:\电影\M-毛骗'
for f in os.listdir(path):
    root = os.path.join(path, f)
    for f in os.listdir(root):
        try:
            os.rename(os.path.join(root, str(f)), os.path.join(root, re.findall(r'\d{2}', f)[0]) +'.flv')
        except Exception as e:
            print(e)
