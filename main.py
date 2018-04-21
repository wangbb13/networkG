# create time: 2018-03-27
# author     : wangbb13
import os
import sys
import json
from generator import Generator


def main():
    if len(sys.argv) < 2:
        print('Usage: python %s {scheme.json}' % os.path.basename(__file__))
        exit(-1)
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        scheme = json.load(f)
    gen = Generator(scheme)
    gen.generate_relations()
    gen.statistic_relation_data()


if __name__ == '__main__':
    main()
