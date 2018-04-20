# create time: 2018-04-12
# author: wangbb13
import random
from scheme import JudgeLegal, ConfigError
from utility import RandomData


class Node(object):
    def __init__(self, node, o_stream):
        try:
            JudgeLegal.legal_node(node)
        except ConfigError as e:
            raise e
        self.has_attr = False
        self.label = str(node['label'])
        self.amount = int(node['amount'])
        if 'attr' in node:
            self.has_attr = True
            self.attr = {}
            for elem in node['attr']:
                self.attr[elem['key']] = elem['value']
        self.o_stream = o_stream
        self.node_vec = []

    def get_node(self, i):
        return self.node_vec[i+1]

    def store_in_memory(self):
        self.node_vec = self.generate_simple()

    def get_record(self, i):
        record = str(i)
        if self.has_attr:
            for _, value in self.attr.items():
                if value['range'] is not None:
                    record += ' %s' % str(random.choice(value['range']))
                else:
                    if value['type'] == 'str':
                        record += ' %s' % RandomData.rand_str()
                    elif value['type'] == 'time':
                        record += ' %s' % RandomData.rand_time()
        return record

    def generate_simple(self):
        """
        generate all nodes, and return
        node format:
            0: id   {key1} {key2} ...
            1: {id} {val1} {val2} ...
            ...
        :return: vector of node
        """
        ret = [''] * (self.amount + 1)
        pattern = 'id'
        if self.has_attr:
            for key, _ in self.attr.items():
                pattern += ' %s' % key
        ret[0] = pattern
        for i in range(self.amount):
            record = self.get_record(i)
            ret[i+1] = record
        return ret

    def generate_real_time(self):
        """
        store a node real time
        :return: None
        """
        pattern = 'id'
        if self.has_attr:
            for key, _ in self.attr.items():
                pattern += ' %s' % key
        yield pattern
        for i in range(self.amount):
            record = self.get_record(i)
            yield record

    def generate_batch(self, batch=-1):
        if batch == -1:
            batch = int(self.amount / 10)
        pattern = 'id'
        if self.has_attr:
            for key, _ in self.attr.items():
                pattern += ' %s' % key
        yield [pattern]
        vec = [''] * batch
        times = int(self.amount / batch)
        remain = self.amount % batch
        i = 0
        for _ in range(times):
            for j in range(batch):
                record = self.get_record(i)
                vec[j] = record
                i += 1
            yield vec
        for j in range(remain):
            record = self.get_record(i)
            vec[j] = record
            i += 1
        yield vec[:remain]
