# create time: 2018-04-15
# author: wangbb13
from power_law import NGPowerLaw
from uniform import NGUniform


def get_distribution(d_dict, node):
    if d_dict['type'] == 'power_law':
        ins = NGPowerLaw(d_dict['lambda'], d_dict['min-d'], d_dict['max-d'], node)
        return ins
    elif d_dict['type'] == 'uniform':
        ins = NGUniform(d_dict['min-d'], d_dict['max-d'], node)
        return ins
    elif d_dict['type'] == 'gaussian':
        return None
    return None
