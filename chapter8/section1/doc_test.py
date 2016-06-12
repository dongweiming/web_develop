# coding=utf-8
def import_object(name):
    """Imports an object by name.
    >>> import os.path
    >>> import_object('os.path') is os.path
    True
    >>> import_object('os.missing_module')
    Traceback (most recent call last):
        ...
    ImportError: No module named missing_module
    """

    parts = name.split('.')
    obj = __import__('.'.join(parts[:-1]), None, None, [parts[-1]], 0)
    try:
        return getattr(obj, parts[-1])
    except AttributeError:
        raise ImportError('No module named {}'.format(parts[-1]))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
