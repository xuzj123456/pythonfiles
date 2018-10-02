# coding=utf-8
import redis
from proxy.config import *


class RedisClient(object):

    def __init__(self, domain=DOMAIN, host=HOST, port=PORT):
        self._db = redis.StrictRedis(host=HOST, port=PORT, db=0)
        self.domain = domain

    def key(self, scheme):
        return '{domain}:{scheme}'.format(domain=self.domain,scheme=scheme)

    def test(self):
        print(self._db.keys('zset1'))


def main():
    test = RedisClient()
    test.test()


if __name__ == '__main__':
    main()
