# create time: 2018-04-04
# author: wangbb13
import os
import json
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


class RandomData(object):
    time_format = '%Y-%m-%d %H:%M:%S.%f'
    character_set = list('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@#_-.')
    character_num = len(character_set)

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


def test_bins():
    a = list(range(1, 20, 2))
    k = [0, 1, 2, 9, 18, 19, 20]
    print(a)
    for i in k:
        j = bin_search(a, i)
        print(j)


if __name__ == '__main__':
    test_bins()