from itertools import groupby

def read_file(path: str):
    f = open(path)
    return f.read().replace('"', '').split(",")

def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)