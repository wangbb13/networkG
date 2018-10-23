# create time : 2018-05-29
# author : wangbb13
import random
from utility import bin_search

from store import StoreRelation
from visualization import get_degree_list, show_plot


class Scale(object):
    def __init__(self, input_file, new_node, output):
        self.input_file = input_file
        self.new_node = new_node
        self.output = output
        self.node_count = 0
        self.edge_count = 0
        self.in_degree_freq = {}  # in-degree: frequency
        self.out_degree_freq = {}  # out-degree: frequency
        self.in_degree_list = []
        self.out_degree_list = []
        self.min_ind = 0xffffff
        self.max_ind = 0
        self.min_outd = 0xffffff
        self.max_outd = 0

        self.extract_from_file()

        self.new_out_degree_list = self.scale(self.out_degree_list)
        self.cdf_d = self.get_cdf_d()

        self.new_in_degree_list = self.scale(self.in_degree_list)
        self.cdf_j, self.idx_j = self.get_cdf_j()

    def extract_from_file(self):
        file = self.input_file
        in_degree = {}
        out_degree = {}
        node_set = set()
        with open(file, 'r') as f:
            for line in f:
                edge = line.strip().split()
                node_set.add(edge[0])
                node_set.add(edge[1])
                self.edge_count += 1
                if edge[0] in out_degree:
                    out_degree[edge[0]] += 1
                else:
                    out_degree[edge[0]] = 1
                if edge[1] in in_degree:
                    in_degree[edge[1]] += 1
                else:
                    in_degree[edge[1]] = 1
        self.node_count = len(node_set)
        for _, v in out_degree.items():
            if v in self.out_degree_freq:
                self.out_degree_freq[v] += 1
            else:
                self.out_degree_freq[v] = 1
            self.min_outd = min(self.min_outd, v)
            self.max_outd = max(self.max_outd, v)
        for _, v in in_degree.items():
            if v in self.in_degree_freq:
                self.in_degree_freq[v] += 1
            else:
                self.in_degree_freq[v] = 1
            self.min_ind = min(self.min_ind, v)
            self.max_ind = max(self.max_ind, v)
        outd_len = self.max_outd - self.min_outd + 1
        ind_len = self.max_ind - self.min_ind + 1
        self.out_degree_list = [0 for _ in range(outd_len)]
        self.in_degree_list = [0 for _ in range(ind_len)]
        for k, v in self.out_degree_freq.items():
            self.out_degree_list[k-self.min_outd] = v
        for k, v in self.in_degree_freq.items():
            self.in_degree_list[k-self.min_ind] = v

    def scale(self, degree_list):
        new_node_count = self.new_node
        factor = new_node_count / self.node_count
        leng = len(degree_list)
        ans_degree_list = [0 for _ in range(leng)]
        for i in range(leng):
            ans_degree_list[i] = int(factor * degree_list[i])
        diff = new_node_count - sum(ans_degree_list)
        if diff > 0:
            zeros = 0
            for i in range(leng):
                if ans_degree_list[i] == 0:
                    zeros += 1
            part = max(int(diff/zeros), 1)
            for i in range(leng):
                if ans_degree_list[i] == 0:
                    if i == 0:
                        ans_degree_list[i] = part
                    else:
                        a = int(random.random() / 5 * ans_degree_list[i-1])
                        ans_degree_list[i] = a + part
                        ans_degree_list[i-1] -= a
        else:
            for i in range(leng):
                if ans_degree_list[i] == 0:
                    ans_degree_list[i] = 1
        return ans_degree_list

    def get_cdf_d(self):
        deno = sum(self.new_out_degree_list)
        leng = len(self.new_out_degree_list)
        ans = [0 for _ in range(leng)]
        ans[0] = self.new_out_degree_list[0] / deno
        for i in range(1, leng):
            ans[i] = ans[i-1] + self.new_out_degree_list[i] / deno
        return ans

    def get_cdf_j(self):
        deno = 0
        leng = len(self.new_in_degree_list)
        for i in range(leng):
            deno = self.new_in_degree_list[i] * (i + self.min_ind)

        ans_j = [0 for _ in range(leng + 1)]
        idx_j = [0 for _ in range(leng + 1)]

        for i in range(leng):
            ans_j[i+1] = ans_j[i] + self.new_in_degree_list[i] * (i + self.min_ind) / deno
            idx_j[i+1] = idx_j[i] + self.new_in_degree_list[i]
        ans_j[0] = self.min_ind / deno
        return ans_j, idx_j

    def get_d(self):
        y = random.random()
        i = bin_search(self.cdf_d, y)
        return i + self.min_outd

    def get_j(self):
        y = max(random.random(), self.cdf_j[0])
        i = bin_search(self.cdf_j, y)
        if self.cdf_j[i] > y:
            a = self.idx_j[i-1]
            b = self.idx_j[i]
            c = self.cdf_j[i-1]
            d = self.cdf_j[i]
            try:
                return a + int((y - c) * (b - a) / (d - c))
            except ZeroDivisionError:
                return a
        else:
            return self.idx_j[i]

    def statistic(self, filename, n, fmt):
        out_degree_list, in_degree_list = get_degree_list(filename, fmt, n, n)
        show_plot(out_degree_list, lambda x: x, self.min_outd, self.max_outd, 'out-degree distribution')
        show_plot(in_degree_list, lambda x: x, self.min_ind, self.max_ind, 'in-degree distribution')

    def deal_lfr(self):
        edges = []
        with open(self.input_file, 'r') as f:
            for line in f:
                num = line.strip().split()
                edges.append([str(int(num[0]) - 1), str(int(num[1]) - 1)])
        with open(self.input_file, 'w') as f:
            for line in edges:
                f.write(' '.join(line) + '\n')

    def run(self):
        output = self.output
        new_node = self.new_node
        o_stream = StoreRelation(output, 'ADJ')
        for i in range(new_node):
            ret = set()
            d_out = self.get_d()
            for _ in range(d_out):
                j = self.get_j()
                ret.add(j)
            o_stream.writeln([i, ret])
        o_stream.close()
        # statistic
        self.deal_lfr()
        self.statistic(self.input_file, self.node_count, 'TSV')
        self.statistic(self.output, new_node, 'ADJ')
