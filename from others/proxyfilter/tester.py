import json
from urlparse import parse_qs

from proxyfilter.db import RedisClient
from proxyfilter import grequests
from proxyfilter.config import *


class ValidTester():
    def __init__(self):
        self.conn = RedisClient()
    
    def exception(self, request, exception):
        proxies = request.kwargs.get('proxies')
        scheme = list(proxies.keys())[0]
        proxy = proxies.get(scheme).replace(scheme + '://', '')
        print('Get Exception of', scheme, proxy, 'Down it')
        self.conn.down(scheme, proxy)

    
    def valid_test(self):
        keys = self.conn.keys()
        for key in keys:
            scheme = key.decode('utf-8').split(':')[1]
            queue = []
            proxies = self.conn.all(scheme)
            for proxy in proxies:
                proxy = proxy.decode('utf-8').strip()
                queue.append(grequests.get(TEST_URL, proxies={
                    'http': 'http' + '://' + proxy,
                    'https': 'https' + '://' + proxy
                }, data={
                    'proxy': proxy
                }))
            responses = grequests.map(queue, exception_handler=self.exception, gtimeout=5)
            for response in responses:
                if not response is None:
                    if response.status_code == 200:
                        proxy = parse_qs(response.request.body).get('proxy')[0]
                        print('Valid Proxy', proxy)
                        self.conn.up(scheme, proxy)
                    else:
                        proxy = parse_qs(response.request.body).get('proxy')[0]
                        print('InValid Proxy', proxy)
                        self.conn.down(scheme, proxy)
