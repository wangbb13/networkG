# create time: 2018-04-13
# author: wangbb13


class OStream(object):
    def __init__(self, filename, disk):
        self.filename = filename
        self.disk = disk

    def get_disk(self):
        return self.disk

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
