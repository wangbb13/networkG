# create time: 2018-03-28
# author: wangbb13


class ConfigError(Exception):
    def __init__(self, msg):
        self.message = msg


class JudgeLegal(object):
    attr_value_type = {'str', 'time', 'date', 'email', 'lang'}
    distribution_type = {'power_law', 'uniform', 'gaussian'}
    shape_type = {'chain', 'star', 'cycle', 'starchain'}

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
            if not JudgeLegal.legal_attr_val_type(one['value']['type']):
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
            a = int(node['amount'])
            assert a > 0
        except Exception:
            raise ConfigError('The amount value should be int type and must more than 0')
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
                mi = int(d['min-d'])
                mx = int(d['max-d'])
                assert mi > 0
                assert mx > 0
                assert mx >= mi
            except Exception:
                raise ConfigError('The min and max degree should be int type and must more than 0. max-d >= min-d')
            try:
                a = float(d['lambda'])
                assert a >= 1.0
            except Exception:
                raise ConfigError('The lambda value should be float type and must more or equal than 1.0')
        elif d['type'] == 'uniform':
            if not ('min-d' in d and 'max-d' in d):
                raise ConfigError('Lack of parameters in uniform distribution: min or max')
            try:
                mi = int(d['min-d'])
                mx = int(d['max-d'])
                assert mi >= 0
                assert mx > 0
                assert mx >= mi
            except Exception:
                raise ConfigError('The min and max degree should be int type and must more than 0. max-d >= min-d')
        elif d['type'] == 'gaussian':
            if not ('mu' in d and 'sigma' in d):
                raise ConfigError('Lack of parameters in gaussian distribution: mu or sigma')
            try:
                mu = float(d['mu'])
                sig = float(d['sigma'])
                assert mu > 0
                assert sig > 0
            except Exception:
                raise ConfigError('The type of mu and sigma should be float and they must more than 0')

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
                raise ConfigError('The type of amount should be int and more than 0')
            # JudgeLegal.legal_distribution(com['distribution'])
            noise = com['noise']
            if not isinstance(noise, dict):
                raise ConfigError('The type of noise in community should be dict')
            if not ('threshold' in noise and 'param-c' in noise):
                raise ConfigError('Lack of fields in community noise: threshold or param-c')
            try:
                c = float(noise['param-c'])
                assert 0 <= c <= 1
                t = float(noise['threshold'])
                assert 0 <= t <= 1
            except Exception:
                raise ConfigError('Threshold and param-c in noise can not be converted to float. \
                 And the they should be in [0,1]')
            try:
                over = float(com['overlap'])
                assert 0 <= over <= 1
            except Exception:
                raise ConfigError('Overlap in community can not be converted to float. \
                 And the overlap should be in [0,1]')

    @staticmethod
    def legal_workload(wl):
        if not isinstance(wl, dict):
            raise ConfigError("The workload config should be a dict")
        if "amount" not in wl:
            raise ConfigError("Lack of a field in workload: amount")
        try:
            a = int(wl['amount'])
            assert a > 0
        except Exception:
            raise ConfigError('The amount value in workload should be int type and more than 0')

        def interval(attr):
            if attr not in wl:
                raise ConfigError('Lack of a field in workload: %s' % attr)
            attr_v = wl[attr]
            if not isinstance(attr_v, dict):
                raise ConfigError('The type of %s should be dict' % attr)
            if 'min' not in attr_v or 'max' not in attr_v:
                raise ConfigError('Lack of fields in workload %s: min or max' % attr)
            try:
                mi = int(attr_v['min'])
                mx = int(attr_v['max'])
                assert mi >= 0
                assert mx > 0
                assert mx >= mi
            except Exception:
                raise ConfigError('The min and max value in workload %s should be int type. \
                min >= 0 and max > 0. max >= min' % attr)

        interval('conjunct')
        interval('disjunct')
        interval('length')
        interval('arity')
        if 'multiplicity' not in wl:
            raise ConfigError('Lack of a field in workload: multiplicity')
        try:
            a = float(wl['multiplicity'])
            assert 0 <= a <= 1
        except Exception:
            raise ConfigError('The multiplicity value in workload should be float type and in [0,1]')
        if 'shape' not in wl:
            raise ConfigError('Lack of a field in workload: shape')
        shape_v = wl['shape']
        if not isinstance(shape_v, dict):
            raise ConfigError('The type of shape value in workload should be dict')
        for k, v in shape_v.items():
            try:
                assert k in JudgeLegal.shape_type
                assert v == 0 or v == 1
            except AssertionError:
                raise ConfigError('%s is not a legal shape in workload. And the value should be 0 or 1.' % k)

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
