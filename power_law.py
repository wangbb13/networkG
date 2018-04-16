# create time: 2018-04-04
# author: wangbb13
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from utility import bin_search
from visualization import show_log_plot


class NGPowerLaw(object):
    def __init__(self, lmd, dmin, dmax, node):
        """
        :param lmd:  use -lmd, i.e. when lmd=1, we use lmd=-1
        :param dmin: min degree
        :param dmax: max degree
        """
        self.lmd = -lmd
        self.dmin = dmin
        self.dmax = dmax
        self.node = node
        self.cdf_d = []
        self.cdf_j = []
        self.idx_j = []
        self.d_exp_r = [d ** self.lmd for d in range(dmin, dmax+1)]
        self.sigma = sum(self.d_exp_r)
        self.c = 1 / self.sigma
        self.C = node / self.sigma

    def integrate(self):
        if self.lmd == -1:
            return math.log(self.dmax / self.dmin)
        else:
            i = self.lmd + 1
            return (self.dmax ** i - self.dmin ** i) / i

    def get_cdf(self, c, flag=True):
        dmin = self.dmin
        dmax = self.dmax
        dnum = dmax - dmin + 1
        if flag:
            cdf = [0] * dnum
            cdf[0] = c * self.d_exp_r[0]
            for i in range(1, dnum):
                cdf[i] = cdf[i-1] + c * self.d_exp_r[i]
            return cdf
        else:
            cdf = [0] * (dnum + 1)
            idx = [-1] * (dnum + 1)
            for i in range(1, dnum + 1):
                num = int(c * self.d_exp_r[i-1])
                idx[i] = idx[i-1] + num
                cdf[i] = cdf[i-1] + num * (i+dmin-1)
            cdf[0] = dmin
            idx[0] = 0
            idx[-1] = self.node - 1
            for i in range(dnum + 1):
                cdf[i] = cdf[i] / cdf[-1]
            return cdf, idx

    def get_d(self):
        if not self.cdf_d:
            self.cdf_d = self.get_cdf(self.c)
        y = random.random()
        i = bin_search(self.cdf_d, y)
        return i + self.dmin

    def get_j(self):
        if (not self.cdf_j) and (not self.idx_j):
            self.cdf_j, self.idx_j = self.get_cdf(self.C, False)
        y = max(random.random(), self.cdf_j[0])
        i = bin_search(self.cdf_j, y)
        if self.cdf_j[i] > y:
            a = self.idx_j[i-1]
            b = self.idx_j[i]
            c = self.cdf_j[i-1]
            d = self.cdf_j[i]
            return a + int((y - c) * (b - a) / (d - c))
        else:
            return self.idx_j[i]


def test():
    node = 1000
    lmd = 1.2
    dmin = 1
    dmax = 40
    import time
    t0 = time.time()
    power_law = NGPowerLaw(lmd, dmin, dmax, node)
    t1 = time.time()
    d_list = [0] * node
    j_list = [0] * node
    for i in range(node):
        d_list[i] = power_law.get_d()
    t2 = time.time()
    show_log_plot(d_list, dmin, dmax, title='out degree distribution')
    total_degree = 0
    img = np.zeros((node, node))
    is_even = node % 2 == 1
    t3 = time.time()
    for i in range(node):
        for _ in range(d_list[i]):
            j = power_law.get_j()
            j = transform(is_even, j, node-1)
            if img[i, j] == 0:
                img[i, j] = 0.9
                total_degree += 1
                j_list[j] += 1
    t4 = time.time()
    show_log_plot(j_list, dmin, dmax, title='in degree distribution')
    plt.imshow(img, cmap='gray')
    plt.show()
    print('total edges: ', total_degree)
    print('initial class time: ', t1-t0, ' seconds')
    print('calc out degree time: ', t2-t1, ' seconds')
    print('calc in  degree time: ', t4-t3, ' seconds')


def transform(is_even, j, last_j):
    if is_even:
        if j % 2 == 0:
            j = last_j - j
    else:
        if j % 2 == 1:
            j = last_j + 1 - j
    return j


def scale(j, a, b, c, d):
    return int((j-a+1)*(d-c+1)/(b-a+1) + c - 1)


def test_community():
    node = 1000
    lmd = 1.23
    dmin = 1
    dmax = 20
    power_law = NGPowerLaw(lmd, dmin, dmax, node)
    # two communities
    d_list = [0] * node
    i_list = [0] * node
    j_list = [0] * node
    for i in range(node):
        d_list[i] = power_law.get_d()
    img = np.zeros((node, node))
    is_even = node % 2 == 1
    step0 = int(node / 2)
    size = int(node / 2)
    for i in range(step0):
        if d_list[i] >= size:
            extra = d_list[i] - size
            for j in range(size):
                img[i, j] = 0.5
                j_list[j] += 1
            i_list[i] += size
            for _ in range(extra):
                j = power_law.get_j()
                j = transform(is_even, j, node-1)
                j = scale(j, 0, node-1, size, node-1)
                if img[i, j] == 0:
                    i_list[i] += 1
                img[i, j] = 0.5
                j_list[j] += 1
        else:
            for _ in range(d_list[i]):
                j = power_law.get_j()
                j = transform(is_even, j, node-1)
                j = scale(j, 0, node-1, 0, size-1)
                if img[i, j] == 0:
                    i_list[i] += 1
                img[i, j] = 0.5
                j_list[j] += 1
    for i in range(step0, node):
        if d_list[i] >= size:
            extra = d_list[i] - size
            for j in range(step0, node):
                img[i, j] = 0.5
                j_list[j] += 1
            i_list[i] += size
            for _ in range(extra):
                j = power_law.get_j()
                j = transform(is_even, j, node-1)
                j = scale(j, 0, node-1, 0, size-1)
                if img[i, j] == 0:
                    i_list[i] += 1
                img[i, j] = 0.5
                j_list[j] += 1
        else:
            for _ in range(d_list[i]):
                j = power_law.get_j()
                j = transform(is_even, j, node-1)
                j = scale(j, 0, node-1, step0, node-1)
                if img[i, j] == 0:
                    i_list[i] += 1
                img[i, j] = 0.5
                j_list[j] += 1
    show_log_plot(i_list, dmin, dmax, title='out degree distribution')
    show_log_plot(j_list, dmin, dmax, title='in  degree distribution')
    plt.imshow(img, cmap='gray')
    plt.show()


def test_community_1():
    node = 1000
    lmd = 1.2
    dmin = 1
    dmax = 40
    comu = 2
    com_size = [int(node / comu) for _ in range(comu)]
    com_size[-1] += node - sum(com_size)
    i_list = [0] * node
    j_list = [0] * node
    total_edges = 0
    img = np.zeros((node, node))
    start_i, start_j = 0, 0
    for size in com_size:
        is_even = size % 2 == 1
        power_law = NGPowerLaw(lmd, dmin, dmax, size)
        for i in range(size):
            d_out = power_law.get_d()
            for _ in range(d_out):
                j = power_law.get_j()
                j = transform(is_even, j, size-1)
                a_i = start_i + i
                a_j = start_j + j
                if img[a_i, a_j] == 0:
                    total_edges += 1
                    i_list[a_i] += 1
                    j_list[a_j] += 1
                    img[a_i, a_j] = 0.9
        start_i += size
        start_j += size
    print('total edges: ', total_edges)
    show_log_plot(i_list, dmin, dmax, title='out degree distribution')
    show_log_plot(j_list, dmin, dmax, title='in  degree distribution')
    plt.imshow(img, cmap='gray')
    plt.show()


def test_add_noise():
    node = 1000
    lmd = 1.2
    dmin = 1
    dmax = 40
    comu = 3
    threshold = 0.5
    com_size = [int(node / comu) for _ in range(comu)]
    com_size[-1] += node % comu
    i_list = [0] * node
    j_list = [0] * node
    total_edges = 0
    extra_edges = 0
    expect_edges = 0
    img = np.zeros((node, node))
    start_i, start_j = 0, 0
    threshold *= dmax
    e1 = math.exp(1)
    ed = math.exp(dmax)
    for size in com_size:
        is_even = size % 2 == 1
        power_law = NGPowerLaw(lmd, dmin, dmax, size)
        for i in range(size):
            d_out = power_law.get_d()
            expect_edges += d_out
            a_i = start_i + i
            for _ in range(d_out):
                j = power_law.get_j()
                j = transform(is_even, j, size-1)
                a_j = start_j + j
                if img[a_i, a_j] == 0:
                    total_edges += 1
                    i_list[a_i] += 1
                    j_list[a_j] += 1
                    img[a_i, a_j] = 0.9
            if d_out > threshold:
                y = random.random()
                d_extra = int(-math.log((1-y)/e1 + y/ed))
                extra_edges += d_extra
                for _ in range(d_extra):
                    j = power_law.get_j()
                    j = transform(is_even, j, size-1)
                    j = scale(j, 0, size-1, 0, node-size-1)
                    if j > start_j:
                        j = j + size
                    if img[a_i, j] == 0:
                        total_edges += 1
                        i_list[a_i] += 1
                        j_list[j] += 1
                        img[a_i, j] = 0.9
        start_i += size
        start_j += size
    print('total edges: ', total_edges)
    print('extra edges: ', extra_edges)
    print('expect edges: ', expect_edges)
    show_log_plot(i_list, dmin, dmax, title='out degree distribution')
    show_log_plot(j_list, dmin, dmax, title='in  degree distribution')
    plt.imshow(img, cmap='gray')
    plt.show()


def test_overlap_community():
    node = 1000
    lmd = 1.2
    dmin = 1
    dmax = 40
    comu = 3
    threshold = 0.5
    overlap = 0.1
    param_c = 0.1
    overlap_size = int(node * overlap / 2)
    com_size = [int(node / comu) for _ in range(comu)]
    com_size[-1] += node % comu
    i_list = [0] * node
    j_list = [0] * node
    total_edges = 0
    extra_edges = 0
    expect_edges = 0
    img = np.zeros((node, node))
    start_i, start_j = 0, 0
    threshold = round(threshold * dmax)
    const_a = math.exp(-1/param_c)
    const_b = const_a - math.exp(-dmax/param_c)
    overlap_pl = NGPowerLaw(lmd*2, 1, int((dmin+dmax)/4), overlap_size)
    ol_even = overlap_size % 2 == 1
    for size in com_size:
        is_even = size % 2 == 1
        power_law = NGPowerLaw(lmd, dmin, dmax, size)
        for i in range(size):
            d_out = power_law.get_d()
            expect_edges += d_out
            a_i = start_i + i
            for _ in range(d_out):
                j = power_law.get_j()
                j = transform(is_even, j, size - 1)
                a_j = start_j + j
                if img[a_i, a_j] == 0:
                    total_edges += 1
                    i_list[a_i] += 1
                    j_list[a_j] += 1
                    img[a_i, a_j] = 0.9
            if d_out > threshold:
                y = random.random()
                d_extra = int(-param_c * math.log(const_a - y * const_b))
                extra_edges += d_extra
                for _ in range(d_extra):
                    j = power_law.get_j()
                    j = transform(is_even, j, size - 1)
                    j = scale(j, 0, size - 1, 0, node - size - 1)
                    if j > start_j:
                        j = j + size
                    if img[a_i, j] == 0:
                        total_edges += 1
                        i_list[a_i] += 1
                        j_list[j] += 1
                        img[a_i, j] = 0.9
        if start_j > overlap_size and overlap_size < size:
            o_start_i = start_i
            o_start_j = start_j - overlap_size
            for _i in range(overlap_size):
                d_over = overlap_pl.get_d()
                expect_edges += d_over
                a_i = _i + o_start_i
                for _ in range(d_over):
                    j = overlap_pl.get_j()
                    j = transform(ol_even, j, overlap_size-1)
                    a_j = j + o_start_j
                    if img[a_i, a_j] == 0:
                        total_edges += 1
                        img[a_i, a_j] = 0.9
                        i_list[a_i] += 1
                        j_list[a_j] += 1
        if start_i > overlap_size and overlap_size < size:
            o_start_i = start_i - overlap_size
            o_start_j = start_j
            for _i in range(overlap_size):
                d_over = overlap_pl.get_d()
                expect_edges += d_over
                a_i = _i + o_start_i
                for _ in range(d_over):
                    j = overlap_pl.get_j()
                    j = transform(ol_even, j, overlap_size-1)
                    a_j = j + o_start_j
                    if img[a_i, a_j] == 0:
                        total_edges += 1
                        img[a_i, a_j] = 0.9
                        i_list[a_i] += 1
                        j_list[a_j] += 1
        start_i += size
        start_j += size
    print('total edges: ', total_edges)
    print('extra edges: ', extra_edges)
    print('expect edges: ', expect_edges)
    show_log_plot(i_list, dmin, dmax, title='out degree distribution')
    show_log_plot(j_list, dmin, dmax, title='in  degree distribution')
    plt.imshow(img, cmap='gray')
    plt.show()


if __name__ == '__main__':
    # test()
    # test_community_1()
    # test_add_noise()
    test_overlap_community()
