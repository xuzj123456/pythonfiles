# coding=utf-8
from pymongo import MongoClient

class TestMongo(object):
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db =  client['blog']