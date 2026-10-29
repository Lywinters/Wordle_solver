from itertools import groupby

def read_file(path: str):
    """
    Read a text file and return a list of strings
    :param path: relative or absolute path to a file to be read. Expects comma separated words
    :return: list of strings
    """
    f = open(path)
    return f.read().replace('"', '').split(",")

def all_equal(iterable):
    """
    Check if all elements in iterable are equal
    :param iterable:
    :return: true if all elements are equal, false otherwise
    """
    g = groupby(iterable)
    return next(g, True) and not next(g, False)