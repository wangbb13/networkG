# create time: 2018-04-13
# author: wangbb13


class OStream(object):
    def __init__(self, filename):
        self.filename = filename
        self.f_handler = open(filename, 'w')

    def close(self):
        self.f_handler.close()

    def get_filename(self):
        return self.filename

    def write(self, an_item):
        """
        write operation
        :param an_item: literal meaning
        :return: None
        """
        pass

    def writeln(self, a_line):
        """
        store one record
        :param a_line: one record
        :return: None
        """
        pass

    def write_batch(self, item_vec):
        """
        store a batch of records
        :param item_vec: list of records
        :return: None
        """
        pass


class StoreQuery(OStream):
    def __init__(self, filename):
        super(StoreQuery, self).__init__(filename)

    def writeln(self, a_line):
        self.f_handler.write(a_line)


class StoreNode(OStream):
    """
    storage format:
    node type: file name
    node id  : line no.
    0: attr0 attr1 ...
    1: val00 val01 ...
    2: val10 val11 ...
    ...
    e.g.
    user.txt
    0: name nickname city
    1: ming alpha beijing
    2: hone beta shanghai
    ...
    """
    def __init__(self, filename):
        super(StoreNode, self).__init__(filename)


class StoreRelation(OStream):
    """
    relation type(or label): directory name
    storage format: TSV
    directory
    |---data.txt
    |---attr.txt
    data.txt:
    0: source_node_id_x target_node_id_y
    1: ...
    attr.txt:
    0: attr0 attr1 ...
    1: val_x_y_0 val_x_y_1 ...
    2: ...

    storage format: ADJ
    directory
    |---data.adj
    |---attr.txt
    data.txt:
    0: source_node_id_0 target_node_id_y00 target_node_id_y01 ...
    1: source_node_id_1 ...
    attr.txt:
    0: attr0 attr1 ... attr_n
    1: val_0_y00_0 ... val_0_y00_n val_0_y01_0 ... val_0_y01_n ...

    storage format: CSR
    directory:
    |---row_offset.csr
    |---col_index.csr
    |---attr.txt
    p.s. there are at most {max_col} numbers(or attr group) per line.
    row_offset.csr:
    number ...
    col_index.csr:
    number ...
    attr.txt:
    0: attr0 attr1 ...
    1: val_group ...
    """
    # TODO: generate attr and store them simultaneously
    def __init__(self, filename, fmt, col_f='', max_col=128):
        super(StoreRelation, self).__init__(filename)
        self.fmt = fmt
        if fmt not in ['TSV', 'ADJ', 'CSR']:
            raise Exception('%s is not a supported format (TSV, ADJ, CSR)' % fmt)
        if fmt == 'CSR' and col_f == '':
            raise Exception('There should be two files for storing data in CSR fmt.')
        if fmt == 'CSR':
            self.col_f_handler = open(col_f, 'w')
        self.row_line_cnt = 0
        self.col_line_cnt = 0
        self.store_max_col = max_col
        self.cur_col_sum = 0

    def write_txt_ln(self, a_line):
        try:
            src = str(a_line[0])
            self.f_handler.write('\n'.join([src + ' ' + str(t) for t in a_line[1]]) + '\n')
        except Exception as e:
            self.close()
            raise e

    def write_adj_ln(self, a_line):
        try:
            self.f_handler.write(str(a_line[0]) + ' ' + ' '.join(list(map(lambda x: str(x), a_line[1]))) + '\n')
        except Exception as e:
            self.close()
            raise e

    def write_csr_ln(self, a_line):
        try:
            self.cur_col_sum += len(a_line[1])
            self.f_handler.write(str(self.cur_col_sum) + ' ')
            self.row_line_cnt += 1
            if self.row_line_cnt == self.store_max_col:
                self.f_handler.write('\n')
                self.row_line_cnt = 0
            num = len(a_line[1])
            ite = (str(x) for x in a_line[1])
            first = min(self.store_max_col - self.col_line_cnt, num)
            self.col_f_handler.write(' '.join([next(ite) for _ in range(first)]) + ' ')
            if self.col_line_cnt + first == self.store_max_col:
                self.col_f_handler.write('\n')
            num -= first
            second = int(num / self.store_max_col)
            self.col_f_handler.write('\n'.join([' '.join([next(ite) for _ in range(self.store_max_col)])\
                                                for _ in range(second)]))
            if second:
                self.col_f_handler.write('\n')
            last = num % self.store_max_col
            self.col_f_handler.write(' '.join([next(ite) for _ in range(last)]) + ' ')
            self.col_line_cnt = (self.col_line_cnt + first + last) % self.store_max_col
        except StopIteration:
            pass
        except Exception as e:
            self.f_handler.close()
            self.col_f_handler.close()
            raise e

    def writeln(self, a_line):
        """
        :param a_line: [row_i, col_j]
                       type(row_i) = int
                       type(col_j) = set
        :return: None
        """
        if self.fmt == 'TSV':
            self.write_txt_ln(a_line)
        elif self.fmt == 'ADJ':
            self.write_adj_ln(a_line)
        else:
            self.write_csr_ln(a_line)

    def write_batch(self, item_vec):
        """
        :param item_vec: [[row_i, col_j], ...]
                         type(row_i) = int
                         type(col_j) = set
        :return: None
        """
        if self.fmt == 'TSV':
            for a_line in item_vec:
                self.write_txt_ln(a_line)
        elif self.fmt == 'ADJ':
            for a_line in item_vec:
                self.write_adj_ln(a_line)
        else:
            for a_line in item_vec:
                self.write_csr_ln(a_line)
