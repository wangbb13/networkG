# create time: 2018-03-27
# author     : wangbb13
import os
import sys
import json
import time
from generator import Generator


def main():
    if len(sys.argv) < 2:
        print('Usage: python %s {scheme.json}' % os.path.basename(__file__))
        exit(-1)
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        scheme = json.load(f)
    gen = Generator(scheme)
    start_time = time.time()
    gen.generate_relations()
    end_time = time.time()
    secs = end_time - start_time
    mins = secs / 60
    hour = mins / 60
    print('run time: %.3f seconds [%.3f minutes, %.3f hours]' % (secs, mins, hour))
    # gen.statistic_relation_data()


if __name__ == '__main__':
    main()
