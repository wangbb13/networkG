# create time : 2018-05-06
# author : wangbb13
from collections import deque


class Label(object):
    def __init__(self, i, name):
        self.id = i
        self.reverse = False
        if i < 0:
            self.id = -i - 1
            self.reverse = True
        self.name = name


class Disjunct(object):
    def __init__(self):
        self.labels = deque()

    def add(self, label):
        self.labels.append(label)

    def size(self):
        return len(self.labels)


class Conjunct(object):
    def __init__(self):
        self.disjuncts = deque()
        self.star = 0
        self.source = ''
        self.target = ''

    def add(self, disj):
        self.disjuncts.append(disj)

    def size(self):
        return len(self.disjuncts)

    def set_star(self, star):
        self.star = star

    def set_source(self, src):
        self.source = src

    def set_target(self, tgt):
        self.target = tgt


class Body(object):
    def __init__(self):
        self.conjuncts = deque()

    def add(self, conj):
        self.conjuncts.append(conj)

    def size(self):
        return len(self.conjuncts)


class Query(object):
    def __init__(self, b):
        self.body = b
        self.vars = deque()

    def add(self, data):
        if isinstance(data, Conjunct):
            self.body.add(data)
        else:
            self.vars.append(data)

    def size(self):
        return self.body.size()
