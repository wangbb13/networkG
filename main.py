# create time: 2018-03-27
# author     : wangbb13
import os
import sys
import json
import time
from generator import Generator

from scale import Scale


def main():
    if len(sys.argv) < 2:
        print('Usage: python %s {scheme.json}' % os.path.basename(__file__))
        exit(-1)
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        scheme = json.load(f)
    gen = Generator(scheme)
    start_time = time.time()
    # do something: generate node, relation and queries
    gen.generate_relations()
    end1 = time.time()
    gen.generate_nodes()
    end2 = time.time()
    gen.generate_query()
    # end
    end_time = time.time()
    secs = end_time - start_time
    mins = secs / 60
    hour = mins / 60
    print('total run time: %.3f seconds [%.3f minutes, %.3f hours]' % (secs, mins, hour))
    print('generate relation time: %.3f seconds ' % (end1 - start_time))
    print('generate node time: %.3f seconds ' % (end2 - end1))
    print('generate query time: %.3f seconds ' % (end_time - end2))
    # gen.statistic_relation_data()


def main2():
    if len(sys.argv) < 4:
        print('Usage: python %s input N output' % os.path.basename(__file__))
        exit(-1)
    input_f = sys.argv[1]
    new_node = int(sys.argv[2])
    output = sys.argv[3]
    scaler = Scale(input_f, new_node, output)
    scaler.run()


if __name__ == '__main__':
    main()
    # main2()
