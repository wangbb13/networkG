# create time : 2018-05-17
# author : wangbb13
import os
import sys
max_val = 0xffffffff


def get_matrix(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError('%s file not found' % filename)
    m_row = 0
    n_col = 0
    adj = []
    with open(filename, 'r') as f:
        for line in f:
            number = [int(x) for x in line.strip().split()]
            m_row = max(m_row, number[0])
            if len(number) > 1:
                adj.append(number)
                n_col = max(n_col, max(number[1:]))
    m_row += 1
    n_col += 1

    n = max(m_row, n_col)

    rtn = [[max_val for _ in range(n)] for _ in range(n)]
    for line in adj:
        i = line[0]
        for j in line[1:]:
            rtn[i][j] = 1

    return rtn, n


def graph_diameter(mat, n):
    rtn = 0
    for k in range(n):
        for i in range(n):
            for j in range(n):
                mat[i][j] = min(mat[i][k] + mat[k][j], mat[i][j])
    for i in range(n):
        for j in range(n):
            if mat[i][j] < max_val and i != j:
                rtn = max(rtn, mat[i][j])
    return rtn


def main():
    if len(sys.argv) != 2:
        print('Function : calculate the diameter of a graph (adj format)\n'
              'Usage : python %s {filename}' % os.path.basename(__file__))
    mat, n = get_matrix(sys.argv[1])
    print('The diameter: ', graph_diameter(mat, n))


if __name__ == '__main__':
    main()
