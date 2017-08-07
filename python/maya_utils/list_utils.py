# encoding:utf-8

import itertools

def split_list(iterable, size):
    """
    split list
    """
    it = iter(iterable)
    item = list(itertools.islice(it, size))
    while item:
        yield item
        item = list(itertools.islice(it, size))