# coding=utf-8
# 用于转换文件夹下的所有（二重）URL编码的文件
import os
from urllib.parse import unquote

root = ''
for file in os.listdir(root):
    if '%' in file:
        os.rename(os.path.join(root, file), os.path.join(root, unquote(unquote(file))))