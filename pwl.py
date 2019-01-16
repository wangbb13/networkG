# -*- coding: utf-8 -*-
# author: wangbb13
# create time: 2018-12-04 14:12
import random
from utility import bin_search


class NGPowerLaw(object):
    def __init__(self, lmd, dmin, dmax, nodes, edges):
        self.lmd = -abs(lmd)
        self.dmin = dmin
        self.dmax = dmax
        self.nodes = nodes
        self.edges = edges
        self.select_p = 0
        self.pre_processing()
        # for out-degree in memory
        __temp = [_ ** self.lmd for _ in range(self.dmin, self.dmax + 1)]
        __c = self.nodes / sum(__temp)
        self.simple_mf = [int(__c * _) for _ in __temp]
        print('For Out Nodes =', sum(self.simple_mf))
        self.d_index, self.d_number = 0, 0

        # for in-degree in memory
        self.dnum = self.dmax - self.dmin + 1
        self.inj_cdf = [0] * (self.dnum + 1)
        self.inj_idx = [-1] * (self.dnum + 1)
        for _ in range(1, self.dnum + 1):
            __num = self.simple_mf[_-1]
            self.inj_idx[_] = self.inj_idx[_-1] + __num
            self.inj_cdf[_] = self.inj_cdf[_-1] + __num * (_ - 1 + self.dmin)
        self.inj_cdf[0] = self.dmin
        self.inj_idx[0] = 0
        self.inj_idx[-1] = self.nodes - 1
        for _ in range(self.dnum + 1):
            self.inj_cdf[_] = self.inj_cdf[_] / self.inj_cdf[-1]
        self.inj_cdf[-1] = 0.999
        # print('inj_cdf', self.inj_cdf)
        # print('inj_idx', self.inj_idx)

    def number_of_dmax(self):
        """
        :return: number of nodes with maximum degree
        """
        __bbs = self.dmax ** self.lmd
        __sum = sum([_ ** self.lmd for _ in range(self.dmin, self.dmax)]) + __bbs
        return self.nodes * (__bbs / __sum)

    def current_edges(self):
        """
        :return: number of edges with current parameters
        """
        __temp = [_ ** self.lmd for _ in range(self.dmin, self.dmax+1)]
        __c = self.nodes / sum(__temp)
        return __c * sum([_ * __ for _, __ in zip(__temp, list(range(self.dmin, self.dmax+1)))])

    def pre_processing(self):
        """
        0. reduce dmax s.t. number_of_dmax() >= 1
        1. calculate current edges c_e
        case 1: c_e < edges
            extend dmax
            case 1.1: stop when number_of_dmax() < 1
            case 1.2: stop when c_e >= edges
        case 2: c_e > edges
            edges -> c
            c -> nodes'
            select_p = nodes' / node
        :return:
        """
        while self.number_of_dmax() < 1:
            self.dmax -= 1
        __edges = self.current_edges()
        print('current edges =', __edges, ' expected edges =', self.edges)
        if __edges < self.edges:
            __temp = self.dmax
            __l = self.dmax
            self.dmax *= 2
            __r = self.dmax
            while self.number_of_dmax() >= 1 and __r < self.nodes:
                __l = __r
                self.dmax *= 2
                __r = self.dmax
            while __l < __r:
                self.dmax = int((__l + __r) / 2)
                if self.number_of_dmax() < 1:
                    __r = self.dmax
                else:
                    __l = self.dmax + 1
            self.dmax = __l - 1
            __edges = self.current_edges()
            if __edges > self.edges:
                __l = __temp
                __r = self.dmax
                while __l < __r:
                    self.dmax = int((__l + __r) / 2)
                    __edges = self.current_edges()
                    if __edges > self.edges:
                        __r = self.dmax
                    else:
                        __l = self.dmax + 1
                self.dmax = __l - 1
            print('adjust dmax =', self.dmax, ' edges =', int(__edges))
        elif __edges > self.edges:
            __temp1 = [_ ** self.lmd for _ in range(self.dmin, self.dmax + 1)]
            __temp2 = [_ * __ for _, __ in zip(__temp1, list(range(self.dmin, self.dmax+1)))]
            c = self.edges / sum(__temp2)
            n = c * sum(__temp1)
            self.select_p = n / self.nodes
            print('reduce select p =', self.select_p)

    def get_d(self):
        if self.select_p > 0:
            if random.random() > self.select_p:
                return 0
        if self.d_index < self.dnum:
            if self.d_number < self.simple_mf[self.d_index]:
                self.d_number += 1
            else:
                self.d_number = 1
                self.d_index += 1
            return self.d_index + self.dmin
        else:
            return self.d_index + self.dmin - 1

    def get_j(self):
        y = max(random.random(), self.inj_cdf[0])
        i = bin_search(self.inj_cdf, y)
        i = min(i, self.dnum)
        if self.inj_cdf[i] > y:
            a = self.inj_idx[i - 1]
            b = self.inj_idx[i]
            c = self.inj_cdf[i - 1]
            d = self.inj_cdf[i]
            try:
                ans = a + int((y - c) * (b - a) / (d - c))
            except ZeroDivisionError:
                ans = a
        else:
            ans = self.inj_idx[i]
        return ans

    def need_extend(self):
        return 0

    def is_special(self):
        return False
