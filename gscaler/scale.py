# create time : 2018-05-29
# author : wangbb13
import os
import sys


class GScale(object):
    def __init__(self, input_f, output, n, m):
        if not os.path.exists(input_f):
            raise FileNotFoundError('%s is not exists' % output)
        self.n = n
        self.m = m
        self.input_f = input_f
        self.output = output

    def run(self):
        pass


def main():
    if len(sys.argv) != 5:
        print('Usage python %s {input_file} {output_file} n(int) m(int)' % os.path.basename(__file__))
        exit(1)
    input_f = sys.argv[1]
    output = sys.argv[2]
    try:
        n = int(sys.argv[3])
        m = int(sys.argv[4])
    except ValueError:
        print('Usage python %s {input_file} {output_file} n(int) m(int)' % os.path.basename(__file__))
        exit(1)
    scale = GScale(input_f, output, n, m)
    scale.run()


if __name__ == '__main__':
    main()
