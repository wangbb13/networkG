# create time: 2018-04-13
# author: wangbb13
from scheme import JudgeLegal, ConfigError
from distribution import get_distribution


class Relation(object):
    def __init__(self, rel, node1, node2):
        try:
            JudgeLegal.legal_relation(rel)
        except ConfigError as e:
            raise e
        self.label = rel['label']
        self.source = rel['source']
        self.target = rel['target']
        self.node1 = node1
        self.node2 = node2
        self.in_distribution = get_distribution(rel['in'], node1)
        self.out_distribution = get_distribution(rel['out'], node2)
        self.has_middle = False
        if 'middle' in rel:
            self.middle = rel['middle']
            self.has_middle = True
        self.has_community = False
        if 'community' in rel:
            commu = rel['community']
            self.com_amount = commu['amount']
            self.com_distribution = get_distribution(commu['distribution'], self.com_amount)
            self.noise_threshold = commu['noise']['threshold']
            self.noise_param_c = commu['noise']['param-c']
            self.overlap = commu['overlap']
            self.has_community = True
        self.has_attr = False
        if 'attr' in rel:
            self.has_attr = True
            self.attr = {}
            for elem in rel['attr']:
                self.attr[elem['key']] = elem['value']

    def generate_simple(self):
        ret = set()
        for i in range(self.node1):
            d_out = self.out_distribution.get_d()
            for _ in range(d_out):
                j = self.in_distribution.get_j()
                ret.add((i, j))
        return ret
