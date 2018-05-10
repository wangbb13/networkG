# create time : 2018-05-09
# author : wangbb13
import os
from store import StoreQuery


class Translate(object):
    def __init__(self, filename):
        self.ql = 'cypher'
        self.base_dir = 'query'
        if not os.path.exists(self.base_dir):
            os.mkdir(self.base_dir)
        self.o_stream = StoreQuery(os.path.join(self.base_dir, filename))

    def translate(self, queries, ql='cypher'):
        for q in queries:
            s = q.translate(ql)
            self.o_stream.writeln(s)
        self.o_stream.close()
