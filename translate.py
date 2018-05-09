# create time : 2018-05-09
# author : wangbb13
import os
from store import StoreQuery


class Translate(object):
    def __init__(self, filename):
        self.ql = 'cypher'
        self.o_stream = StoreQuery(filename)
        self.base_dir = 'query'

    def to_cypher(self):
        pass
