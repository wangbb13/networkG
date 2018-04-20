# create time: 2018-04-04
# author: wangbb13
import os
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
    plt.scatter(x, y, marker='.', color=get_rand_color(), linewidths=2)
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


def show_matrix_thumbnail(filename, fmt, rows, cols, col_file='', max_col=32):
    if not os.path.exists(filename):
        raise FileNotFoundError('%s is not exist' % filename)
    img_row = min(1000, rows)
    img_col = min(1000, cols)
    row_cr = int(rows / img_row)
    col_cr = int(cols / img_col)
    unit = 1 / (row_cr * col_cr)
    img = np.zeros((img_row, img_col))
    if fmt == 'txt':
        with open(filename, 'r') as f:
            for line in f:
                no = [int(x) for x in line.strip().split()]
                img_i = int(no[0] / row_cr)
                img_j = int(no[1] / col_cr)
                try:
                    img[img_i, img_j] += unit
                except IndexError:
                    img_i -= img_i >= img_row
                    img_j -= img_j >= img_col
                    img[img_i, img_j] += unit
    elif fmt == 'adj':
        with open(filename, 'r') as f:
            for line in f:
                no = [int(x) for x in line.strip().split()]
                img_i = int(no[0] / row_cr)
                for col_j in no[1:]:
                    img_j = int(col_j / col_cr)
                    try:
                        img[img_i, img_j] += unit
                    except IndexError:
                        img_i -= img_i >= img_row
                        img_j -= img_j >= img_col
                        img[img_i, img_j] += unit
    elif fmt == 'csr':
        if not os.path.exists(col_file):
            raise FileNotFoundError('%s is not exists for csr format' % col_file)
        try:
            col_f = open(col_file, 'r')
            row_id = 0
            pre_of = 0
            remain = []
            with open(filename, 'r') as f:
                for line in f:
                    no = [int(x) for x in line.strip().split()]
                    for of in no:
                        cnt = of - pre_of
                        pre_of = of
                        img_i = int(row_id / row_cr)
                        row_id += 1
                        need_l = math.ceil(cnt / max_col)
                        if len(remain) < cnt:
                            record = ''
                            for _ in range(need_l):
                                record += col_f.readline()
                            record = remain + [int(_) for _ in record.strip().split()]
                        else:
                            record = remain
                        for j in range(cnt):
                            img_j = int(record[j] / col_cr)
                            try:
                                img[img_i, img_j] += unit
                            except IndexError:
                                img_i -= img_i >= img_row
                                img_j -= img_j >= img_col
                                img[img_i, img_j] += unit
                        remain = record[cnt:]
        finally:
            if col_f:
                col_f.close()
    plt.imshow(img, cmap='gray')
    plt.show()
