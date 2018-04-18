# create time: 2018-04-13
# author: wangbb13
import math
import random
from scheme import JudgeLegal, ConfigError
from distribution import get_distribution
from utility import get_community_size, scale, transform


class Relation(object):
    def __init__(self, rel, node1, node2):
        try:
            JudgeLegal.legal_relation(rel)
        except ConfigError as e:
            raise e
        self.label = rel['label']
        self.source = rel['source']
        self.target = rel['target']
        self.rel = rel
        self.node1 = node1
        self.node2 = node2
        self.in_distribution = get_distribution(rel['in'], node2)
        self.out_distribution = get_distribution(rel['out'], node1)
        self.has_middle = False
        if 'middle' in rel:
            self.middle = rel['middle']
            self.has_middle = True
        self.has_community = False
        if 'community' in rel:
            commu = rel['community']
            self.com_amount = commu['amount']
            # self.com_distribution = get_distribution(commu['distribution'], self.com_amount)
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

    def generate_with_com(self):
        if not self.has_community:
            return
        com_cnt = self.com_amount
        out_max_d = self.rel['out']['max-d']
        in_max_d = self.rel['in']['max-d']
        param_c = self.noise_param_c
        out_threshold = round(out_max_d * self.noise_threshold)
        row_axis = get_community_size(com_cnt, self.node1)
        col_axis = get_community_size(com_cnt, self.node2)
        const_a = math.exp(-1/param_c)
        const_b = const_a - math.exp(-out_max_d/param_c)
        start_i, start_j = 0, 0
        for i in range(com_cnt):
            out_pl = get_distribution(self.rel['out'], row_axis[i])
            in_pl = get_distribution(self.rel['in'], col_axis[i])
            for row in range(row_axis[i]):
                a_line_set = set()
                d_out = out_pl.get_d()
                a_i = start_i + row
                for _ in range(d_out):
                    j = in_pl.get_j()
                    a_j = start_j + j
                    a_line_set.add((a_i, a_j))
                # when d_out > threshold, add noise
                if d_out > out_threshold:
                    y = random.random()
                    d_extra = int(-param_c * math.log(const_a - y * const_b))
                    for _ in range(d_extra):
                        j = in_pl.get_j()
                        j = scale(j, 0, col_axis[i]-1, 0, self.node2-col_axis[i]-1)
                        if j > start_j:
                            j += col_axis[i]
                        a_line_set.add((a_i, j))
                yield a_line_set
            # add overlap community
            start_i += row_axis[i]
            start_j += col_axis[i]

    def generate_simple(self):
        ret = set()
        for i in range(self.node1):
            d_out = self.out_distribution.get_d()
            for _ in range(d_out):
                j = self.in_distribution.get_j()
                ret.add((i, j))
        return ret

    def generate_one_line(self):
        for i in range(self.node1):
            ret = set()
            d_out = self.out_distribution.get_d()
            for _ in range(d_out):
                j = self.in_distribution.get_j()
                ret.add((i, j))
            yield ret

    def generate_batch_line(self, batch=-1):
        if batch == -1:
            batch = int(self.node1 / 10)
        times = int(self.node1 / batch)
        remain = self.node1 % batch
        row = 0
        for _ in range(times):
            ret = [set() for _ in range(batch)]
            for i in range(batch):
                d_out = self.out_distribution.get_d()
                for x in range(d_out):
                    j = self.in_distribution.get_j()
                    ret[i].add((row, j))
                row += 1
            yield ret
        ret = [set() for _ in range(remain)]
        for i in range(remain):
            d_out = self.out_distribution.get_d()
            for x in range(d_out):
                j = self.in_distribution.get_j()
                ret[i].add((row, j))
            row += 1
        yield ret

    def generate_special(self):
        """
        p: power_law, u: uniform, g: gaussian
        common: p-p, p-u, p-g
                u-p, u-u, u-g
                g-p, g-u, g-g
        special: *-u: min = 1, max = 1
        :return:
        """
        ret = [0] * self.node1
        for i in range(self.node1):
            d_out = self.out_distribution.get_d()
            ret.append(d_out)
        return ret

    def generate_special_batch(self, batch=-1):
        if batch == -1:
            batch = int(self.node1 / 10)
        times = int(self.node1 / batch)
        remain = self.node1 % batch
        ret = [0] * batch
        for _ in range(times):
            for i in range(batch):
                ret[i] = self.out_distribution.get_d()
            yield ret
        for i in range(remain):
            ret[i] = self.out_distribution.get_d()
        yield ret[:remain]
