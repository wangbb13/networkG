# create time : 2018-05-05
# author : wangbb13
import random
from utility import bin_search
from headers import Label, Disjunct, Conjunct, Body, Query
from utility import SomeVar


class Workload(object):
    def __init__(self, node_list, rel_list, workload):
        """
        :param node_list: [node_type, ...] list of string
        :param rel_list:  [rel_type, ...] list of string
        :param workload:  dict, config info
        """
        self.workload = workload
        self.node_list = list(set(node_list))
        self.rel_list = list(set(rel_list))
        self.node_type = {}
        self.edge_type = {}
        node_num = len(self.node_list)
        edge_num = len(self.rel_list)
        for i in range(node_num):
            self.node_type[node_list[i]] = i
        for i in range(edge_num):
            self.edge_type[rel_list[i][2]] = i
        self.matrix = [[0 for _ in range(node_num)] for _ in range(node_num)]
        self.origin_aut = [{} for _ in range(node_num)]
        for r in rel_list:
            a = self.node_type[r[0]]
            b = self.node_type[r[1]]
            c = self.edge_type[r[2]]
            d = -c - 1
            self.matrix[a][b] = 1
            self.matrix[b][a] = 1
            if c in self.origin_aut[a]:
                self.origin_aut[a][c].add(b)
            else:
                self.origin_aut[a][c] = {b}
            if d in self.origin_aut[b]:
                self.origin_aut[b][d].add(a)
            else:
                self.origin_aut[b][d] = {a}
        Workload.floyd(self.matrix)
        self.graph = Workload.get_adj(self.matrix, self.workload['length']['max'])

    @staticmethod
    def floyd(matrix):
        max_val = SomeVar.max_val
        size = len(matrix)
        for i in range(size):
            for j in range(size):
                if matrix[i][j] == 0:
                    matrix[i][j] = max_val
        while True:
            flag = True
            t_mat = matrix.copy()
            for i in range(size):
                for j in range(size):
                    x = t_mat[i][j]
                    for k in range(size):
                        if t_mat[i][k] < max_val and t_mat[k][j] < max_val:
                            x = min(x, t_mat[i][k] + t_mat[k][j])
                    if x != matrix[i][j]:
                        flag = False
                        matrix[i][j] = x
            if flag:
                break

    @staticmethod
    def get_adj(matrix, threshold):
        size = len(matrix)
        g = [[] for _ in range(size)]
        for i in range(size):
            for j in range(size):
                if matrix[i][j] <= threshold:
                    g[i].append(j)
        return g

    def number_of_paths(self, n):
        g = self.graph
        size = len(g)
        matrix = [[0 for _ in range(size)] for _ in range(n+1)]
        for j in range(size):
            matrix[0][j] = 1
        for i in range(1, n+1):
            for j in range(size):
                for k in g[j]:
                    matrix[i][j] += matrix[i-1][k]
        return matrix

    def generate_random_path(self, matrix, first_node, length, star):
        g = self.graph
        current_node = first_node
        path = [0 for _ in range(2*length + 1)]
        if current_node < 0:
            size = len(g)
            t_l = [0 for _ in range(size)]
            t_l[0] = matrix[length][0]
            for i in range(1, size):
                t_l[i] = t_l[i-1] + matrix[length][i]
            current_node = bin_search(t_l, random.randint(1, t_l[size-1]))
        idx = 0
        path[idx] = current_node
        idx += 1
        for i in range(length, 0, -1):
            if current_node in g[current_node] and random.random() <= star:
                path[idx] = 1
                path[idx+1] = current_node
                idx += 2
            else:
                rand_num = random.randint(1, matrix[i][current_node])
                acc = 0
                for j in g[current_node]:
                    acc += matrix[i-1][j]
                    if acc >= rand_num:
                        current_node = j
                        path[idx] = 0
                        path[idx+1] = current_node
                        idx += 2
                        break
        return path

    def calc_paths(self, n, end_node):
        aut = self.origin_aut
        m = len(aut)
        mat = [[0 for _ in range(m)] for _ in range(n+1)]
        mat[0][end_node] = 1
        for i in range(1, n+1):
            for j in range(m):
                for _, s in aut[j].items():
                    for t in s:
                        mat[i][j] += mat[i-1][t]
        return mat

    def generate_random_path_2(self, mat, start_node, leng, max_leng):
        aut = self.origin_aut
        path = []
        cur_node = start_node
        i = leng
        while i <= max_leng and mat[i][cur_node] == 0:
            i += 1
        if i > max_leng:
            i = leng
            while i > 0 and mat[i][cur_node] == 0:
                i -= 1
        if i == 0:
            return path
        while i > 0:
            rand_num = random.randint(1, mat[i][cur_node])
            acc = 0
            for e, s in aut[cur_node].items():
                flag = False
                for t in s:
                    acc += mat[i-1][t]
                    if acc >= rand_num:
                        cur_node = t
                        path.append(e)
                        flag = True
                        break
                if flag:
                    break
            i -= 1
        return path

    def generate_random_disjunct(self, source, target, leng, max_leng):
        mat = self.calc_paths(max_leng, target)
        path = self.generate_random_path_2(mat, source, leng, max_leng)
        if not path:
            return None
        ret = Disjunct()
        for e in path:
            if e < 0:
                x = Label(e, self.rel_list[-e - 1])
                ret.add(x)
            else:
                x = Label(e, self.rel_list[e])
                ret.add(x)
        return ret

    def generate_random_conjunct(self, source, target):
        disj = self.workload['disjunct']
        leng = self.workload['length']
        ret = Conjunct()
        for i in range(SomeVar.gen_query_max_try):
            n_disj = random.randint(disj['min'], disj['max'])
            flag = False
            for _ in range(n_disj):
                length = random.randint(leng['min'], leng['max'])
                x = self.generate_random_disjunct(source, target, length, leng['max'])
                if not x:
                    flag = True
                    break
                ret.add(x)
            if not flag:
                break
            if flag and i == SomeVar.gen_query_max_try-1:
                return None
        return ret

    @staticmethod
    def generate_more_arity(query, arity, not_cycle):
        n_conj = query.body.size()
        arity = min(arity, n_conj + not_cycle)
        seq = list(range(arity))
        random.shuffle(seq)
        for v in seq:
            query.add(SomeVar.node_var + str(v))

    def generate_chain(self):
        prefix = SomeVar.node_var
        query = Query(Body())
        n_conjs = random.randint(self.workload['conjunct']['min'], self.workload['conjunct']['max'])
        path_mat = self.number_of_paths(n_conjs)
        path = self.generate_random_path(path_mat, -1, n_conjs, self.workload['multiplicity'])

        for i in range(n_conjs):
            conj = self.generate_random_conjunct(path[2*i], path[2*i + 2])
            conj.set_source(prefix + str(i))
            conj.set_target(prefix + str(i+1))
            conj.set_star(path[2*i + 1])
            query.add(conj)

        ar = random.randint(self.workload['arity']['min'], self.workload['arity']['max'])
        if ar == 1:
            query.add(prefix + '0')
        elif ar == 2:
            query.add(prefix + '0')
            query.add(prefix + str(n_conjs))
        elif ar > 2:
            Workload.generate_more_arity(query, ar, True)

        return query

    def generate_star(self):
        prefix = SomeVar.node_var
        mult = self.workload['multiplicity']
        query = Query(Body())
        n_conjs = random.randint(self.workload['conjunct']['min'], self.workload['conjunct']['max'])
        path_mat = self.number_of_paths(1)

        path = self.generate_random_path(path_mat, -1, 1, mult)
        conj = self.generate_random_conjunct(path[0], path[2])
        conj.set_source(prefix + '0')
        conj.set_target(prefix + '1')
        conj.set_star(path[1])
        query.add(conj)

        c_e = path[0]
        for i in range(1, n_conjs):
            path_ = self.generate_random_path(path_mat, c_e, 1, mult)
            conj = self.generate_random_conjunct(c_e, path_[2])
            conj.set_source(prefix + '0')
            conj.set_target(prefix + str(i+1))
            conj.set_star(path_[1])
            query.add(conj)

        ar = random.randint(self.workload['arity']['min'], self.workload['arity']['max'])
        if ar == 1:
            query.add(prefix + '0')
        elif ar == 2:
            query.add(prefix + '0')
            query.add(prefix + '1')
        elif ar > 2:
            self.generate_more_arity(query, ar, True)

        return query

    def generate_cycle(self):
        prefix = SomeVar.node_var
        mult = self.workload['multiplicity']
        query = Query(Body())
        n_conjs = random.randint(self.workload['conjunct']['min'], self.workload['conjunct']['max'])

        n1 = int(n_conjs / 2)
        n2 = n_conjs - n1

        path_mat1 = self.number_of_paths(n1)
        path1 = self.generate_random_path(path_mat1, -1, n1, mult)
        for i in range(n1):
            conj = self.generate_random_conjunct(path1[2*i], path1[2*i+2])
            conj.set_source(prefix + str(i))
            conj.set_target(prefix + str(i+1))
            conj.set_star(path1[2*i + 1])
            query.add(conj)

        path_mat2 = self.number_of_paths(n2)
        path2 = self.generate_random_path(path_mat2, path1[0], n2, mult)
        for i in range(n2):
            conj = self.generate_random_conjunct(path2[2*i], path2[2*i+2])
            if i == 0:
                conj.set_source(prefix + '0')
            else:
                conj.set_source(prefix + str(n1+i))
            if i == n2-1:
                conj.set_target(prefix + str(n1))
            else:
                conj.set_target(prefix + str(n1+i+1))
            conj.set_star(path2[2*i + 1])
            query.add(conj)

        ar = random.randint(self.workload['arity']['min'], self.workload['arity']['max'])
        if ar == 1:
            query.add(prefix + '0')
        elif ar == 2:
            query.add(prefix + '0')
            query.add(prefix + str(n1))
        elif ar > 2:
            Workload.generate_more_arity(query, ar, False)

        return query

    def generate_starchain(self):
        prefix = SomeVar.node_var
        mult = self.workload['multiplicity']
        query = Query(Body())
        n_conjs = random.randint(self.workload['conjunct']['min'], self.workload['conjunct']['max'])

        n1 = int(n_conjs / 3)
        n2 = int((n_conjs - n1) / 2)
        n3 = n_conjs - n1 - n2

        path_mat1 = self.number_of_paths(n1)
        path1 = self.generate_random_path(path_mat1, -1, n1, mult)
        for i in range(n1):
            conj = self.generate_random_conjunct(path1[2*i], path1[2*i + 2])
            conj.set_source(prefix + str(i))
            conj.set_target(prefix + str(i+1))
            conj.set_star(path1[2*i + 1])
            query.add(conj)

        path_mat2 = self.number_of_paths(1)
        for i in range(n2):
            path_ = self.generate_random_path(path_mat2, path1[0], 1, mult)
            conj = self.generate_random_conjunct(path_[0], path_[2])
            conj.set_source(prefix + '0')
            conj.set_target(prefix + str(n1+i+1))
            conj.set_star(path_[1])
            query.add(conj)
        for i in range(n3):
            path_ = self.generate_random_path(path_mat2, path1[2*n1], 1, mult)
            conj = self.generate_random_conjunct(path_[0], path_[2])
            conj.set_source(prefix + str(n1))
            conj.set_target(prefix + str(n1+n2+i))
            conj.set_star(path_[1])
            query.add(conj)

        ar = random.randint(self.workload['arity']['min'], self.workload['arity']['max'])
        if ar == 1:
            query.add(prefix + '0')
        elif ar == 2:
            query.add(prefix + '0')
            query.add(prefix + str(n1))
        elif ar > 2:
            Workload.generate_more_arity(query, ar, True)

        return query

    def generate_query(self):
        shapes = [k for k, v in self.workload['shape'].items() if v == 1]
        s = random.choice(shapes)
        return eval('self.generate_' + s + '()')

    def generate_workload(self):
        return [self.generate_query() for _ in range(self.workload['amount'])]
