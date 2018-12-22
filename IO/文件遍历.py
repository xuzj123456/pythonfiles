# coding=utf-8
import os
import re

root = ''
for file in os.listdir(root):
    path = os.path.join(root, file)
    for file in os.listdir(path):
        try:
            os.rename(os.path.join(path, str(file)), os.path.join(path, re.findall(r'\d{2}', file)[0]) + '.flv')
        except Exception as e:
            print(e)
