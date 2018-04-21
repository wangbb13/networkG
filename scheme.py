# create time: 2018-03-28
# author: wangbb13


class ConfigError(Exception):
    def __init__(self, msg):
        self.message = msg


class JudgeLegal(object):
    attr_value_type = {'str', 'time'}
    distribution_type = {'power_law', 'uniform', 'gaussian'}

    def __init__(self):
        pass

    @staticmethod
    def legal_attr_val_type(val_t):
        return val_t in JudgeLegal.attr_value_type

    @staticmethod
    def legal_distribution_type(distr_t):
        return distr_t in JudgeLegal.distribution_type

    @staticmethod
    def legal_attr(attr_val):
        if not isinstance(attr_val, list):
            raise ConfigError('The type of attr value should be list')
        for one in attr_val:
            if not isinstance(one, dict):
                raise ConfigError('The type of elements in attr should be dict')
            if not ('key' in one and 'value' in one):
                raise ConfigError('Lack of fields in elements of attr: key or value')
            if not isinstance(one['value'], dict):
                raise ConfigError('The type of value should be dict')
            if not ('type' in one['value'] and 'range' in one['value']):
                raise ConfigError('Lack of fields in value: type or range')
            if JudgeLegal.legal_attr_val_type(one['value']['type']):
                raise ConfigError('Legal value type is: %s' % str(JudgeLegal.attr_value_type))
            if not (isinstance(one['value']['range'], list) or one['value']['range'] is None):
                raise ConfigError('The range of value should be a list or null')

    @staticmethod
    def legal_node(node):
        if not isinstance(node, dict):
            raise ConfigError('The Node Config should be a dict')
        if 'label' not in node:
            raise ConfigError('Lack of a field in Node: label')
        if 'amount' not in node:
            raise ConfigError('Lack of a field in Node: amount')
        try:
            assert int(node['amount'])
        except AssertionError:
            raise ConfigError('The amount value can not convert to int')
        if 'attr' in node:
            JudgeLegal.legal_attr(node['attr'])

    @staticmethod
    def legal_distribution(d):
        if not isinstance(d, dict):
            raise ConfigError('The type of distribution should be dict')
        if not JudgeLegal.legal_distribution_type(d['type']):
            raise ConfigError('Legal distribution type is: %s' % str(JudgeLegal.distribution_type))
        if d['type'] == 'power_law':
            if 'lambda' not in d:
                raise ConfigError('Lack of parameters in power law distribution: lambda')
            if not ('min-d' in d and 'max-d' in d):
                raise ConfigError('Lack of parameters in power law distribution: mid-d and max-d')
            try:
                assert float(d['lambda'])
            except AssertionError:
                raise ConfigError('The type of lambda should be float')
        elif d['type'] == 'uniform':
            if not ('min-d' in d and 'max-d' in d):
                raise ConfigError('Lack of parameters in uniform distribution: min or max')
            try:
                assert int(d['min'])
                assert int(d['max'])
            except AssertionError:
                raise ConfigError('The type of min and max should be int')
        elif d['type'] == 'gaussian':
            if not ('mu' in d and 'sigma' in d):
                raise ConfigError('Lack of parameters in gaussian distribution: mu or sigma')
            try:
                assert float(d['mu'])
                assert float(d['sigma'])
            except AssertionError:
                raise ConfigError('The type of mu and sigma should be float')

    @staticmethod
    def legal_relation(rel):
        if not isinstance(rel, dict):
            raise ConfigError('The relation config should be a dict')
        if not ('source' in rel and 'target' in rel and 'in' in rel and 'out' in rel):
            raise ConfigError('Lack of fields: source, target, in or out')
        if 'label' not in rel:
            raise ConfigError('Lack of fields of Relation: label')
        JudgeLegal.legal_distribution(rel['in'])
        JudgeLegal.legal_distribution(rel['out'])
        if 'community' in rel:
            com = rel['community']
            if 'amount' not in com:
                raise ConfigError('Lack of fields in community: amount')
            if 'noise' not in com:
                raise ConfigError('Lack of fields in community: noise')
            if 'overlap' not in com:
                raise ConfigError('Lack of fields in community: overlap')
            try:
                assert int(com['amount'])
            except AssertionError:
                raise ConfigError('The type of amount should be int')
            # JudgeLegal.legal_distribution(com['distribution'])
            noise = com['noise']
            if not isinstance(noise, dict):
                raise ConfigError('The type of noise in community should be dict')
            if not ('threshold' in noise and 'param-c' in noise):
                raise ConfigError('Lack of fields in community noise: threshold or param-c')
            try:
                assert float(noise['threshold'])
                assert float(noise['param-c'])
                c = float(noise['param-c'])
                assert 0 <= c <= 1
                t = float(noise['threshold'])
                assert 0 <= t <= 1
            except AssertionError:
                raise ConfigError('Threshold and param-c in noise can not be converted to float. \
                 And the they should be in [0,1]')
            try:
                assert float(com['overlap'])
                over = float(com['overlap'])
                assert 0 <= over <= 1
            except AssertionError:
                raise ConfigError('Overlap in community can not be converted to float. \
                 And the overlap should be in [0,1]')

    @staticmethod
    def legal_scheme(scheme):
        if not ('gdb' in scheme and 'node' in scheme and 'relation' in scheme):
            raise ConfigError('Lack of fields in scheme: gdb, node or relation')
        if not (isinstance(scheme['node'], list) and isinstance(scheme['relation'], list)):
            raise ConfigError('The type of node and relation should be list')
        if "store-format" not in scheme:
            raise ConfigError('Lack of a field in scheme: store-format')
        if scheme['store-format'] not in ['TSV', 'ADJ', 'CSR']:
            raise ConfigError('%s is not a supported format (TSV, ADJ, CSR)' % scheme['store-format'])


'''
class Scheme(object):
    def __init__(self, config):
        self.config = config
        try:
            self.legal_scheme(config)
        except ConfigError as e:
            raise e
        self.node_labels = set()
        self.relation_labels = set()
        self.nodes = {}
        self.relations = {}
        try:
            for one in config['node']:
                node = Node(one)
                if node.has_label:
                    assert node.label not in self.node_labels
                self.nodes[node.label] = node
                self.node_labels.add(node.label)
        except ConfigError as e:
            raise e
        except AssertionError:
            raise ConfigError('The node label can not be duplicate')
        try:
            for one in config['relation']:
                rel = Relation(one)
                assert rel.label not in self.relation_labels
                assert rel.source in self.node_labels
                assert rel.target in self.node_labels
                if rel.has_middle:
                    assert rel.middle in self.node_labels
                self.relations[rel.label] = rel
                self.relation_labels.add(rel.label)
        except ConfigError as e:
            raise e
        except AssertionError:
            raise ConfigError('The relation label can not be duplicate. \
             And the source (or target, middle) should be in node labels.')

    @staticmethod
    def legal_scheme(scheme):
        if not ('gdb' in scheme and 'node' in scheme and 'relation' in scheme):
            raise ConfigError('Lack of fields in scheme: gdb, node or relation')
        if not (isinstance(scheme['node'], list) and isinstance(scheme['relation'], list)):
            raise ConfigError('The type of node and relation should be list')
'''
