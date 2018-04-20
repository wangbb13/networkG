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


def show_plot(degree_list, func, dmin=-1, dmax=-1, title='degree distribution chart'):
    mind = min(degree_list)
    maxd = max(degree_list)
    leng = maxd - mind + 1
    freq = [0] * leng
    for d in degree_list:
        freq[d-mind] += 1
    df_zip = list(zip([_ for _ in range(mind, maxd+1)], freq))
    # actual
    actual_zip = list(filter(lambda t: t[0] > 0 and t[1] > 0, df_zip))
    x = np.asarray([func(t[0]) for t in actual_zip])
    y = np.asarray([func(t[1]) for t in actual_zip])
    plt.scatter(x, y, marker='.', color=get_rand_color(), linewidths=2)
    # expected
    if dmin > 0 and dmax > 0:
        expect_zip = list(filter(lambda t: dmin <= t[0] <= dmax and t[1] > 0, df_zip))
        x = np.asarray([func(t[0]) for t in expect_zip])
        y = np.asarray([func(t[1]) for t in expect_zip])
        plt.scatter(x, y, marker='x', color=get_rand_color(), linewidths=2)
    plt.title(title)
    plt.show()


def get_degree_list(filename, fmt, rows, cols, col_file=''):
    """
    :param filename: data file name
    :param fmt: txt, adj, or csr
    :param rows: the count of source node
    :param cols: the count of target node
    :param col_file: parsing csr format data
    :return: out_degree_list, in_degree_list
             {]_degree_list[i]: {} degree of node i
    """
    if not os.path.exists(filename):
        raise FileNotFoundError('%s is not exist' % filename)
    if fmt not in ['txt', 'adj', 'csr']:
        raise Exception('%s is not a supported format (txt, adj, csr)' % fmt)
    out_degree_list = [0] * rows
    in_degree_list = [0] * cols
    if fmt == 'txt':
        with open(filename, 'r') as f:
            for line in f:
                no = [int(x) for x in line.strip().split()]
                out_degree_list[no[0]] += 1
                in_degree_list[no[1]] += 1
    elif fmt == 'adj':
        with open(filename, 'r') as f:
            for line in f:
                no = [int(x) for x in line.strip().split()]
                out_degree_list[no[0]] += len(no) - 1
                for j in no[1:]:
                    in_degree_list[j] += 1
    else:   # csr
        if not os.path.exists(col_file):
            raise FileNotFoundError('%s is not exists for csr format' % col_file)
        pre_of = 0
        row_id = 0
        with open(filename, 'r') as f:
            for line in f:
                for c in line.strip().split():
                    out_degree_list[row_id] += int(c) - pre_of
                    pre_of = int(c)
                    row_id += 1
        with open(col_file, 'r') as f:
            for line in f:
                for c in line.strip().split():
                    in_degree_list[int(c)] += 1
    return out_degree_list, in_degree_list


def show_matrix_thumbnail(filename, fmt, rows, cols, col_file='', max_col=128):
    if not os.path.exists(filename):
        raise FileNotFoundError('%s is not exist' % filename)
    if fmt not in ['txt', 'adj', 'csr']:
        raise Exception('%s is not a supported format (txt, adj, csr)' % fmt)
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
    else:   # csr
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
