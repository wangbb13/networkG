# create time : 2018-04-15
# author : wangbb13
import os
import math
from scheme import JudgeLegal, ConfigError
from node import Node
from relation import Relation
from store import StoreRelation
from visualization import get_degree_list, show_plot, show_matrix_thumbnail


class Generator(object):
    def __init__(self, scheme):
        self.scheme = scheme
        try:
            JudgeLegal.legal_scheme(scheme)
        except ConfigError as e:
            raise e
        self.format = scheme['store-format']
        self.base_dir = 'data'
        if not os.path.exists(self.base_dir):
            os.mkdir(self.base_dir)
        self.node_labels = set()
        self.relation_labels = set()
        self.node_amount = {}
        self.node_ins = []
        self.relation_ins = []
        try:
            for one in scheme['node']:
                node = Node(one)
                assert node.label not in self.node_labels
                self.node_labels.add(node.label)
                self.node_amount[node.label] = node.amount
                self.node_ins.append(node)
        except ConfigError as e:
            raise e
        except AssertionError:
            raise ConfigError('The node label can not be duplicate')
        try:
            for one in scheme['relation']:
                assert one['label'] not in self.relation_labels
                assert one['source'] in self.node_labels
                assert one['target'] in self.node_labels
                self.relation_labels.add(one['label'])
                node1 = self.node_amount[one['source']]
                node2 = self.node_amount[one['target']]
                rel = Relation(one, node1, node2)
                self.relation_ins.append(rel)
        except ConfigError as e:
            raise e
        except AssertionError:
            raise ConfigError('The relation label can not be duplicate. \
             And the source (or target, middle) should be in node labels.')

    def generate_relations(self):
        """
        just generate data
        :return: None
        """
        for rel in self.relation_ins:
            rel_path = os.path.join(self.base_dir, rel.label)
            if not os.path.exists(rel_path):
                os.mkdir(rel_path)
            if self.format == 'CSR':
                row_name = 'row_offset.csr'
                col_name = 'col_index.csr'
                row_file = os.path.join(self.base_dir, rel.label, row_name)
                col_file = os.path.join(self.base_dir, rel.label, col_name)
                o_stream = StoreRelation(row_file, 'CSR', col_file)
            else:
                data_name = 'data.' + self.format.lower()
                data_file = os.path.join(self.base_dir, rel.label, data_name)
                o_stream = StoreRelation(data_file, self.format)
            if rel.has_community:
                for line in rel.generate_with_com():
                    pass
                    # o_stream.writeln(line)
            else:
                for batch in rel.generate_batch_line():
                    pass
                    # o_stream.write_batch(batch)
                # for line in rel.generate_one_line():
                    # pass
                    # o_stream.writeln(line)

    def statistic_relation_data(self):
        """
        show plot & show matrix thumbnail
        :return:
        """
        for rel in self.relation_ins:
            if self.format == 'CSR':
                row_name = 'row_offset.csr'
                col_name = 'col_index.csr'
                row_file = os.path.join(self.base_dir, rel.label, row_name)
                col_file = os.path.join(self.base_dir, rel.label, col_name)
                # show degree distribution
                out_degree_list, in_degree_list = get_degree_list(row_file, 'CSR', rel.node1, rel.node2, col_file)
                if rel.out_distribution.get_d_type() == 'power_law':
                    show_plot(out_degree_list, math.log, rel.out_distribution.dmin, \
                              rel.out_distribution.dmax, 'out-degree distribution')
                else:
                    show_plot(out_degree_list, lambda x: x, rel.out_distribution.dmin, \
                              rel.out_distribution.dmax, 'out-degree distribution')
                if rel.in_distribution.get_d_type() == 'power_law':
                    show_plot(in_degree_list, math.log, rel.in_distribution.dmin, \
                              rel.in_distribution.dmax, 'in-degree distribution')
                else:
                    show_plot(in_degree_list, lambda x: x, rel.in_distribution.dmin, \
                              rel.in_distribution.dmax, 'in-degree distribution')
                # show matrix thumbnail
                show_matrix_thumbnail(row_file, 'CSR', rel.node1, rel.node2, col_file)
            else:
                data_name = 'data.' + self.format.lower()
                data_file = os.path.join(self.base_dir, rel.label, data_name)
                # show degree distribution
                out_degree_list, in_degree_list = get_degree_list(data_file, self.format, rel.node1, rel.node2)
                if rel.out_distribution.get_d_type() == 'power_law':
                    show_plot(out_degree_list, math.log, rel.out_distribution.dmin, \
                              rel.out_distribution.dmax, 'out-degree distribution')
                else:
                    show_plot(out_degree_list, lambda x: x, rel.out_distribution.dmin, \
                              rel.out_distribution.dmax, 'out-degree distribution')
                if rel.in_distribution.get_d_type() == 'power_law':
                    show_plot(in_degree_list, math.log, rel.in_distribution.dmin, \
                              rel.in_distribution.dmax, 'in-degree distribution')
                else:
                    show_plot(in_degree_list, lambda x: x, rel.in_distribution.dmin, \
                              rel.in_distribution.dmax, 'in-degree distribution')
                # show matrix thumbnail
                show_matrix_thumbnail(data_file, self.format, rel.node1, rel.node2)

    def generate_nodes(self):
        pass
