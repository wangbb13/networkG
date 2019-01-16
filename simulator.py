# -*- coding: utf-8 -*-
# create time: 2.81-12-07 13:44
# author: wangbb13
# function: simulate from data, opera scenario
# user -> status number
# user -> comment on status
# user -> thumb up on comment
import os
import time
import random


class Content(object):
    @staticmethod
    def data():
        return str(random.randint(0, 1000000))


class Interface(object):
    @staticmethod
    def add_user(user_id, password):
        """
        add a user
        :param user_id:
        :param password:
        :return: user_id
        """
        return 0

    @staticmethod
    def add_user_follow(user_s, user_t):
        """
        user_s -> user_t (follow)
        :param user_s: source user
        :param user_t: target user
        :return: None
        """
        pass

    @staticmethod
    def get_community_data(user_id, number):
        """
        get community data
        :param user_id:
        :param number:
        :return: e.g. [{u'comment': [], u'picture': u'', u'word': u'XXXXXXXXXXXX', u'thumbup_num': u'0',
        u'thumbup': 0, u'comment_num': u'0', u'userid': u'100016', u'head_url': u'100016.jpeg',
        u'time': u'1544257360.33', u'nickname': u'\u4eac\u5267\u5c0f\u738b\u5b50', u'id': u'13',
        u'time_str': u'2018-12-08 16:22:40'}]
        """
        pass

    @staticmethod
    def release_feed(user_id, content):
        """
        release status
        :param user_id:
        :param content:
        :return: feed_time, feed_id
        """
        return 0, 0

    @staticmethod
    def add_comment(user_id, feed_userid, feed_time, feed_id, comment):
        """
        comment to a status
        :param user_id:
        :param feed_userid:
        :param feed_time:
        :param feed_id:
        :param comment:
        :return: True or False
        """
        return False

    @staticmethod
    def add_thumb_up(user_id, feed_userid, feed_time):
        """
        thumb up to a status
        :param user_id:
        :param feed_userid:
        :param feed_time:
        :return: True or False
        """
        return False


class Simulate(object):
    def __init__(self, emit_file, comment_file, thumb_file):
        try:
            assert os.path.exists(emit_file)
            assert os.path.exists(comment_file)
            assert os.path.exists(thumb_file)
        except AssertionError:
            print('file not exists')
            exit(0)
        # emit file
        user_max_id = 0
        status_max_id = 0
        with open(emit_file, 'r') as fin:
            for line in fin:
                line = line.strip()
                if line:
                    line = [int(_) for _ in line.split()]
                    user_max_id = max(user_max_id, line[0])
                    status_max_id = max(status_max_id, max(line[1:]) if len(line) > 1 else 0)
        self.user_number = user_max_id + 1
        self.user_emit_status = [[] for _ in range(user_max_id+1)]  # [i]: i: user i, type: list, content: status id
        self.user_has_emitted = [0 for _ in range(user_max_id+1)]  # [i]: i: user i, content: position in above[i]
        self.status_owner = [-1 for _ in range(status_max_id+1)]    # [i]: i: status i, content: owner user id
        with open(emit_file, 'r') as fin:
            for line in fin:
                line = line.strip()
                if line:
                    line = [int(_) for _ in line.split()]
                    self.user_emit_status[line[0]] = line[1:] if len(line) > 1 else []
                    for _ in line[1:]:
                        self.status_owner[_] = line[0]
        # comment file
        self.user_comment_status = [[] for _ in range(user_max_id+1)]  # [i]: user i comment status list
        self.user_has_commented = [0 for _ in range(user_max_id+1)]   # [i]: user i has commented position
        with open(comment_file, 'r') as fin:
            for line in fin:
                line = line.strip()
                if line:
                    line = [int(_) for _ in line.split()]
                    self.user_comment_status[line[0]] = line[1:] if len(line) > 1 else []
        # thumb up file
        self.user_thumb_status = [[] for _ in range(user_max_id+1)]  # [i]: user i thumb up status list
        self.user_has_thumbed = [0 for _ in range(user_max_id+1)]   # [i]: user i has thumbed position
        with open(thumb_file, 'r') as fin:
            for line in fin:
                line = line.strip()
                if line:
                    line = [int(_) for _ in line.split()]
                    self.user_thumb_status[line[0]] = line[1:] if len(line) > 1 else []
        # for simulate
        self.status_map = dict()  # [status_id] : [ feed_time: , feed_id ]
        self.user_follows = [set() for _ in range(self.user_number)]  # set of user following
        self.user_id_func = [0 for _ in range(self.user_number)]  # virtual user id to actual id
        self.add_all_user()

    def add_all_user(self):
        for _ in range(self.user_number):
            uid = Interface.add_user(_, 'a123456')
            self.user_id_func[_] = uid

    def flush(self):
        with open('dump.txt', 'w') as fout:
            fout.write(str(self.user_number) + '\n')
            fout.write(str(self.user_emit_status) + '\n')
            fout.write(str(self.user_has_emitted) + '\n')
            fout.write(str(self.status_owner) + '\n')
            fout.write(str(self.user_comment_status) + '\n')
            fout.write(str(self.user_has_commented) + '\n')
            fout.write(str(self.user_thumb_status) + '\n')
            fout.write(str(self.user_has_thumbed) + '\n')
            fout.write(str(self.status_map) + '\n')
            fout.write(str(self.user_follows) + '\n')
            fout.write(str(self.user_id_func) + '\n')

    def load(self):
        with open('dump.txt', 'r') as fin:
            lines = fin.readlines()
        self.user_number = eval(lines[0].strip())
        self.user_emit_status = eval(lines[1].strip())
        self.user_has_emitted = eval(lines[2].strip())
        self.status_owner = eval(lines[3].strip())
        self.user_comment_status = eval(lines[4].strip())
        self.user_has_commented = eval(lines[5].strip())
        self.user_thumb_status = eval(lines[6].strip())
        self.user_has_thumbed = eval(lines[7].strip())
        self.status_map = eval(lines[8].strip())
        self.user_follows = eval(lines[9].strip())
        self.user_id_func = eval(lines[10].strip())

    def run(self, times, sleep_time):
        """
        :param times: iteration times
        :param sleep_time: seconds
        :return: None
        """
        iter = 0
        func = list(range(self.user_number))
        while iter < times:
            random.shuffle(func)
            # emit status
            counter = [0 for _ in range(self.user_number)]
            for _ in range(self.user_number):
                ratio = (len(self.user_emit_status[_]) - self.user_has_emitted[_]) / (times - iter)
                integer = int(ratio)
                decimal = ratio - integer
                num = integer + 1 if random.random() > decimal else 0
                num = min(num, len(self.user_emit_status[_]) - self.user_has_emitted[_])
                counter[_] = num
            for uid in func:
                uid = self.user_id_func[uid]
                start = self.user_has_emitted[uid]
                end = start + counter[uid]
                for sid in self.user_emit_status[start:end]:
                    """ emit status
                    TODO: get feed id, feed_time
                    """
                    feed_time, feed_id = Interface.release_feed(uid, Content.data())
                    self.status_map[sid] = [feed_time, feed_id]
                self.user_has_emitted[uid] += counter[uid]
            # comment to status
            for _ in range(self.user_number):
                ratio = (len(self.user_comment_status[_]) - self.user_has_commented[_]) / (times - iter)
                integer = int(ratio)
                decimal = ratio - integer
                num = integer + 1 if random.random() > decimal else 0
                num = min(num, len(self.user_comment_status[_]) - self.user_has_commented[_])
                counter[_] = num
            for uid in func:
                __uid = self.user_id_func[uid]
                start = self.user_has_commented[uid]
                end = start + counter[uid]
                pos = start
                for _ in range(start, end):
                    """ comment to status
                    """
                    sid = self.user_comment_status[_]
                    own = self.status_owner[sid]
                    __own = self.user_id_func[own]
                    if own not in self.user_follows[uid]:
                        Interface.add_user_follow(__uid, __own)
                        self.user_follows[uid].add(own)
                    if sid in self.status_map:
                        ftime, fid = self.status_map[sid]
                        res = Interface.add_comment(__uid, __own, ftime, fid, Content.data())
                        if res:
                            tmp = self.user_comment_status[pos]
                            self.user_comment_status[pos] = sid
                            self.user_comment_status[_] = tmp
                            pos += 1
                self.user_has_commented[uid] = pos
            # thumb up to status
            for _ in range(self.user_number):
                ratio = (len(self.user_thumb_status[_]) - self.user_has_thumbed[_]) / (times - iter)
                integer = int(ratio)
                decimal = ratio - integer
                num = integer + 1 if random.random() > decimal else 0
                num = min(num, len(self.user_thumb_status[_]) - self.user_has_emitted[_])
                counter[_] = num
            for uid in func:
                __uid = self.user_id_func[uid]
                start = self.user_has_thumbed[uid]
                end = start + counter[uid]
                pos = start
                for _ in range(start, end):
                    """ thumb up to status
                    """
                    sid = self.user_thumb_status[_]
                    own = self.status_owner[sid]
                    __own = self.user_id_func[own]
                    if own not in self.user_follows[uid]:
                        Interface.add_user_follow(__uid, __own)
                        self.user_follows[uid].add(own)
                    if sid in self.status_map:
                        ftime, _ = self.status_map[sid]
                        res = Interface.add_thumb_up(__uid, __own, ftime)
                        if res:
                            tmp = self.user_thumb_status[pos]
                            self.user_thumb_status[pos] = sid
                            self.user_thumb_status[_] = tmp
                            pos += 1
                self.user_has_thumbed[uid] = pos
            # sleep
            time.sleep(sleep_time)
            iter += 1


if __name__ == '__main__':
    iters = 1000
    space = 1000
    emit_file = './emit/data.adj'
    comment_file = './comment/data.adj'
    thumb_file = './thumb_up/data.adj'
    simulate = Simulate(emit_file, comment_file, thumb_file)
    try:
        simulate.run(iters, space)
    except Exception:
        simulate.flush()
