# -*- coding: utf-8 -*-
import os
import sys
import networkx as nx


def transform(filename):
    sl = filename.split('.')
    body = ''.join(sl[:-1])
    fmt = sl[-1]
    #newname = body + 'TSV.' + fmt
    adjname = body + 'ADJ.' + fmt
    #tf = open(newname, 'w')
    af = open(adjname, 'w')
    source = ''
    first = True
    g = nx.Graph()
    with open(filename, 'r') as f:
        for line in f:
            num = line.strip().split()
            #tf.write(' '.join([num[0], num[-1]]) + '\n')
            g.add_edge(int(num[0]), int(num[-1]))
            if num[0] != source:
                if not first:
                    af.write('\n')
                else:
                    first = False
                af.write(' '.join([num[0], num[-1]]))
                source = num[0]
            else:
                af.write(' ' + num[-1])
    #tf.close()
    af.close()
    os.system('./property/diameter %s' % adjname)
    print('avg cluster coefficient: ', nx.average_clustering(g))


def main():
    if len(sys.argv) != 2:
        print(sys.argv)
        print('Usage python %s {filename}' % os.path.basename(__file__))
        exit(1)
    transform(sys.argv[1])
    print('done')


if __name__ == '__main__':
    main()

