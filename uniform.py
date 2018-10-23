# create time: 2018-04-15
# author: wangbb13
import random


class NGUniform(object):
    def __init__(self, dmin, dmax, node):
        self.dmin = dmin
        self.dmax = dmax
        self.node = node
        self.davg = round((dmin + dmax)/2)
        self.total_degree = round(node * (dmin + dmax) / 2)

    def need_extend(self):
        return 0

    def get_d_type(self):
        return 'uniform'

    def get_total_degree(self):
        return self.total_degree

    def get_d(self):
        return random.randint(self.dmin, self.dmax)

    def get_j(self):
        y = random.random()
        return round(y * self.node)
