# create time : 2018-04-15
# author : wangbb13
from scheme import JudgeLegal, ConfigError


class Generator(object):
    def __init__(self, scheme):
        self.scheme = scheme
        try:
            JudgeLegal.legal_scheme(scheme)
        except ConfigError as e:
            raise e

