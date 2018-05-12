# create time : 2018-05-06
# author : wangbb13
from collections import deque
from utility import SomeVar


class Label(object):
    def __init__(self, i, name):
        self.id = i
        self.reverse = False
        if i < 0:
            self.id = -i - 1
            self.reverse = True
        self.name = name

    def is_reverse(self):
        return self.reverse

    def to_str(self, var=True):
        if var:
            prefix = SomeVar.edge_var
            return prefix + str(self.id)
        else:
            return self.name


class Disjunct(object):
    def __init__(self):
        self.labels = deque()

    def add(self, label):
        self.labels.append(label)

    def size(self):
        return len(self.labels)

    def to_cypher_one(self):
        if self.size() == 0:
            return ''
        return self.labels[0].to_str()


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

    def to_cypher(self):
        if self.size() == 0:
            return ''
        prefix = SomeVar.node_var
        where_cond = []
        source = self.source
        target = self.target
        if source[0] != prefix:
            where_cond.append('id(var' + self.source + ') = ' + self.source)
            source = 'var' + source
        if target[0] != prefix:
            where_cond.append('id(var' + self.target + ') = ' + self.target)
            target = 'var' + target
        where_clause = ' AND '.join(where_cond)
        if self.star:
            content = '(%s)-[:%s*]->(%s)' % \
                      (source, '|'.join([disj.to_cypher_one() for disj in self.disjuncts]), target)
        else:
            disj = self.disjuncts[0]
            elem = []
            for label in disj.labels:
                if label.is_reverse():
                    elem.append('<-[:' + label.to_str() + ']-')
                else:
                    elem.append('-[:' + label.to_str() + ']->')
            content = '(' + source + ')' + '()'.join(elem) + '(' + target + ')'
        return content, where_clause


class Body(object):
    def __init__(self):
        self.conjuncts = deque()

    def add(self, conj):
        self.conjuncts.append(conj)

    def size(self):
        return len(self.conjuncts)

    def to_cypher(self):
        if self.size() == 0:
            return '', ''
        conj_res = [conj.to_cypher() for conj in self.conjuncts]
        return ', '.join([t[0] for t in conj_res]), ' AND '.join([t[1] for t in conj_res if t[1]])


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

    def to_cypher(self):
        if self.size() == 0:
            return ''
        output_var = ', '.join(self.vars)
        b_content, where_clause = self.body.to_cypher()
        ans = 'MATCH ' + b_content
        if where_clause:
             ans += ' WHERE ' + where_clause
        if not output_var:
            ans += ' RETURN "true" LIMIT 1'
        else:
            ans += ' RETURN DISTINCT ' + output_var
        ans += ';'
        return ans

    def translate(self, ql='cypher'):
        if ql == 'cypher':
            return self.to_cypher()
