# create time : 2018-04-15
# author : wangbb13
from scheme import JudgeLegal, ConfigError
from node import Node
from relation import Relation
from store import StoreRelation


class Generator(object):
    def __init__(self, scheme):
        self.scheme = scheme
        try:
            JudgeLegal.legal_scheme(scheme)
        except ConfigError as e:
            raise e
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
        pass

    def generate_nodes(self):
        pass
