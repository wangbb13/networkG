# create time : 2018-05-29
# author : wangbb13
import random


class Feature(object):
    def __init__(self, input_file, new_node):
        self.input_file = input_file
        self.new_node = new_node
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

    def get_d(self):
        pass

    def get_j(self):
        pass
