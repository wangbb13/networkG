# create time: 2018-04-04
# author: wangbb13
import os
import json
import math
import random
from datetime import timedelta, datetime


def bin_search(vec, key):
    """
    :param vec: search in vec
    :param key: search value
    :return: index i, where vec[i] >= key > vec[i-1] or i == len(vec)
    """
    left = 0
    right = len(vec)
    while left < right:
        mid = int((left + right) / 2)
        if vec[mid] > key:
            right = mid
        elif vec[mid] == key:
            return mid
        else:
            left = mid + 1
    return left


def get_json(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError('%s does not exist' % filename)
    with open(filename, 'r') as f:
        ret = json.load(f)
        return ret


class SomeVar(object):
    max_val = 0xffffffff
    node_var = 'v'
    edge_var = 'e'
    gen_query_max_try = 10


class RandomData(object):
    time_format = '%Y-%m-%d %H:%M:%S.%f'
    character_set = list('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@#_-.')
    character_num = len(character_set)
    unknown = 'null'

    @staticmethod
    def rand_str(length=0):
        leng = int(length)
        if leng < 1:
            leng = random.randint(1, RandomData.character_num)
        random.shuffle(RandomData.character_set)
        return ''.join(RandomData.character_set[:leng])

    @staticmethod
    def rand_time(time_delta=None):
        if time_delta is None:
            time_delta = timedelta(days=365)
        time_now = datetime.now()
        start_time = time_now - time_delta
        days = time_delta.days
        seconds = time_delta.seconds
        if seconds > 0:
            seconds += 86400
        time_rand = timedelta(random.randint(0, days-1), random.randint(0, seconds))
        return start_time + time_rand

    @staticmethod
    def rand_date(time_delta=None):
        # TODO
        pass

    @staticmethod
    def rand_email():
        # TODO
        pass

    @staticmethod
    def rand_lang():
        # TODO
        pass

    @staticmethod
    def rand_attr(one_attr):
        val = one_attr['value']
        if not val['range']:
            return random.choice(val['range'])
        else:
            if val['type'] == 'str':
                return RandomData.rand_str()
            elif val['type'] == 'time':
                return RandomData.rand_time()
            elif val['type'] == 'date':
                return RandomData.rand_date()
            elif val['type'] == 'email':
                return RandomData.rand_email()
            elif val['type'] == 'lang':
                return RandomData.rand_lang()
            else:
                return RandomData.unknown

    @staticmethod
    def rand_attrs(attr):
        return ' '.join([RandomData.rand_attr(one) for one in attr])


def transform(is_even, j, last_j):
    if is_even:
        if j % 2 == 0:
            j = last_j - j
    else:
        if j % 2 == 1:
            j = last_j + 1 - j
    return j


def scale(j, a, b, c, d):
    return int((j-a+1)*(d-c+1)/(b-a+1) + c - 1)


def get_community_size(com_cnt, size_sum):
    if com_cnt == 1:
        return [size_sum]
    avg_size = int(size_sum / com_cnt)
    a = int(avg_size / 2)
    b = avg_size * 2
    ans = [0] * com_cnt
    cur_size = 0
    for i in range(com_cnt-1):
        ans[i] = random.randint(a, b)
        b = int((avg_size + b) / 2)
        cur_size += ans[i]
    ans[-1] = size_sum - cur_size
    if ans[-1] < 0:
        prec = com_cnt - 1
        minus_avg = math.ceil(ans[-1] / prec)
        for i in range(prec):
            ans[i] -= minus_avg
        ans[-1] = 0
        cur_sum = sum(ans)
        ans[-1] = size_sum - cur_sum
        last_two_sum = ans[-1] + ans[-2]
        ans[-2] = int(last_two_sum / 2)
        ans[-1] = last_two_sum - ans[-2]
    return ans


def test_bins():
    a = list(range(1, 20, 2))
    k = [0, 1, 2, 9, 18, 19, 20]
    print(a)
    for i in k:
        j = bin_search(a, i)
        print(j)


def test_get_com_size():
    com_cnt = 1
    size_sum = 10000
    ans = get_community_size(com_cnt, size_sum)
    print(ans)
    print(sum(ans), len(ans))


if __name__ == '__main__':
    # test_bins()
    test_get_com_size()
