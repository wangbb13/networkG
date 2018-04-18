# create time: 2018-04-04
# author: wangbb13
import math
import random
import numpy as np
import matplotlib.pyplot as plt


def get_rand_color():
    ans = '#'
    for _ in range(3):
        c = hex(random.randint(0, 255))[2:]
        if len(c) == 1:
            c = '0' + c
        ans = ans + c
    return ans


def show_log_plot(degree_list, dmin=-1, dmax=-1, title='degree distribution chart'):
    mind = min(degree_list)
    maxd = max(degree_list)
    leng = maxd - mind + 1
    dgre = [_ for _ in range(mind, maxd+1)]
    freq = [0] * leng
    for d in degree_list:
        freq[d-mind] += 1
    # actual
    actual_dgre = []
    actual_freq = []
    for i in range(leng):
        if dgre[i] > 0 and freq[i] > 0:
            actual_dgre.append(dgre[i])
            actual_freq.append(freq[i])
    # print("actual x and y: ")
    # print(actual_dgre)
    # print(actual_freq)
    x = np.asarray([math.log(x) for x in actual_dgre])
    y = np.asarray([math.log(x) for x in actual_freq])
    # plt.scatter(x, y, marker='.', color=get_rand_color(), linewidths=2)
    # expected
    if dmin > 0 and dmax > 0:
        expect_dgre = []
        expect_freq = []
        for i in range(leng):
            # if dgre[i] >= dmin and dgre[i] <= dmax and freq[i] > 0:
            if dmin <= dgre[i] <= dmax and freq[i] > 0:
                expect_dgre.append(dgre[i])
                expect_freq.append(freq[i])
        # print("expected x and y: ")
        # print(expect_dgre)
        # print(expect_freq)
        x = np.asarray([math.log(x) for x in expect_dgre])
        y = np.asarray([math.log(x) for x in expect_freq])
        plt.scatter(x, y, marker='x', color=get_rand_color(), linewidths=2)
    plt.title(title)
    plt.show()
