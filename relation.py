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
        """
        yield one line every time
        format: [row_i, col_j]
                type(row_i) = int
                type(col_j) = set
        :return: None
        """
        all_e = 0
        if not self.has_community:
            return
        com_cnt = self.com_amount
        out_max_d = self.rel['out']['max-d']
        # in_max_d = self.rel['in']['max-d']
        param_c = self.noise_param_c
        over_lap = self.overlap
        out_threshold = round(out_max_d * self.noise_threshold)
        row_axis = get_community_size(com_cnt, self.node1)
        col_axis = get_community_size(com_cnt, self.node2)
        const_a = math.exp(-1/param_c)
        const_b = const_a - math.exp(-out_max_d/param_c)
        start_i, start_j = 0, 0
        ul_col, ul_row, lr_col, lr_row = 0, 0, 0, 0
        for i in range(com_cnt):
            out_pl = get_distribution(self.rel['out'], row_axis[i])
            in_pl = get_distribution(self.rel['in'], col_axis[i])
            block_is_even = col_axis[i] % 2 == 1
            # upper left
            if over_lap > 0 and i > 0:
                ul_col = int(col_axis[i-1] * over_lap)
                ul_row = int(row_axis[i-1] * over_lap)
                ul_in_pl = get_distribution(self.rel['in'], ul_col)
                ul_out_pl = get_distribution(self.rel['out'], ul_row)
                ul_is_even = ul_col % 2 == 1
            # lower right
            if over_lap > 0 and i < com_cnt-1:
                lr_col = int(col_axis[i+1] * over_lap)
                lr_row = int(row_axis[i+1] * over_lap)
                lr_in_pl = get_distribution(self.rel['in'], lr_col)
                lr_out_pl = get_distribution(self.rel['out'], lr_row)
                lr_is_even = lr_col % 2 == 1
            for row in range(row_axis[i]):
                a_line_set = set()
                d_out = out_pl.get_d()
                a_i = start_i + row
                for _ in range(d_out):
                    j = in_pl.get_j()
                    j = transform(block_is_even, j, col_axis[i]-1)
                    a_j = start_j + j
                    a_line_set.add(a_j)
                # when d_out > threshold, add noise
                if d_out > out_threshold:
                    y = random.random()
                    d_extra = int(-param_c * math.log(const_a - y * const_b))
                    for _ in range(d_extra):
                        j = in_pl.get_j()
                        j = transform(block_is_even, j, col_axis[i]-1)
                        j = scale(j, 0, col_axis[i]-1, 0, self.node2-col_axis[i]-1)
                        if j > start_j:
                            j += col_axis[i]
                        a_line_set.add(j)
                # add overlap community in upper left
                if over_lap > 0 and i > 0 and row < ul_row:
                    d_over_ul = ul_out_pl.get_d()
                    for _ in range(d_over_ul):
                        j = ul_in_pl.get_j()
                        j = transform(ul_is_even, j, ul_col-1)
                        a_j = start_j - j
                        a_line_set.add(a_j)
                # add overlap community in lower right
                if over_lap > 0 and i < com_cnt-1 and row > (row_axis[i] - lr_row):
                    d_over_lr = lr_out_pl.get_d()
                    for _ in range(d_over_lr):
                        j = lr_in_pl.get_j()
                        j = transform(lr_is_even, j, lr_col-1)
                        a_j = start_j + col_axis[i] + j
                        a_line_set.add(a_j)
                all_e += len(a_line_set)
                yield [a_i, a_line_set]
            start_i += row_axis[i]
            start_j += col_axis[i]
        print('all edges: ', all_e)

    def generate_simple(self):
        """
        generate graph simply
        :return: ret
                 type: list
                 ret[i]: set of column index of line i
        """
        ret = [set()] * self.node1
        for i in range(self.node1):
            d_out = self.out_distribution.get_d()
            for _ in range(d_out):
                j = self.in_distribution.get_j()
                ret[i].add(j)
        return ret

    def generate_one_line(self):
        """
        yield one line during the generate time
        format: [row_i, col_j]
                type(row_i) = int
                type(col_j) = set
        :return: None
        """
        all_e = 0
        for i in range(self.node1):
            ret = set()
            d_out = self.out_distribution.get_d()
            all_e += d_out
            for _ in range(d_out):
                j = self.in_distribution.get_j()
                ret.add(j)
            yield [i, ret]
        print('all edges: ', all_e)

    def generate_batch_line(self, batch=-1):
        """
        yield a batch of lines
        format: [[row_i, col_j], ...]
                type(row_i) = int
                type(col_j) = set
        :param batch: number of lines to yield
        :return: None
        """
        all_e = 0
        if batch == -1:
            batch = int(self.node1 / 10)
        times = int(self.node1 / batch)
        remain = self.node1 % batch
        row = 0
        for _ in range(times):
            ret = [[0, set()] for _ in range(batch)]
            for i in range(batch):
                d_out = self.out_distribution.get_d()
                all_e += d_out
                for x in range(d_out):
                    j = self.in_distribution.get_j()
                    ret[i][1].add(j)
                ret[i][0] = row
                row += 1
            yield ret
        ret = [[0, set()] for _ in range(remain)]
        for i in range(remain):
            d_out = self.out_distribution.get_d()
            all_e += d_out
            for x in range(d_out):
                j = self.in_distribution.get_j()
                ret[i][1].add(j)
            ret[i][0] = row
            row += 1
        yield ret
        print('all edges ', all_e)

    def generate_special(self):
        """
        p: power_law, u: uniform, g: gaussian
        common: p-p, p-u, p-g
                u-p, u-u, u-g
                g-p, g-u, g-g
        special: *-u: min = 1, max = 1
        :return: ret
                 type(ret) = []
                 ret[i] = the degree of node i
                 e.g. ret[0] = 9, then relations are: 0 -> 0, 0 -> 1, ... 0 -> 8
                 and so on
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
