# coding=utf-8

import requests

url = r'http://taolu.me/'
req = requests.get(url)
print(req.text)