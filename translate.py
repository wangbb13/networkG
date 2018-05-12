# create time : 2018-05-09
# author : wangbb13
import os
from store import StoreQuery


class Translate(object):
    def __init__(self, filename, ql='cypher'):
        self.ql = ql
        self.base_dir = 'query'
        if not os.path.exists(self.base_dir):
            os.mkdir(self.base_dir)
        self.o_stream = StoreQuery(os.path.join(self.base_dir, filename))

    def translate(self, queries):
        for q in queries:
            s = q.translate(self.ql)
            self.o_stream.writeln(s + '\n\n')
        self.o_stream.close()
