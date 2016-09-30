import collections


# class Thing(collections.Mapping):
    # must define: __getitem__, __iter__, __len__
    # has mixins: __contains__, keys, items, values, get, __eq__, and __ne__

class Thing(object):

    def __init__(self):
        self.mode = 'abc'

    def __iter__(self):
        if self.mode == 'abc':
            yield 'a'
            yield 'b'
            yield 'c'
            self.mode = 'def'

        elif self.mode == 'def':
            yield 'd'
            yield 'e'
            yield 'f'
            self.mode = 'xyz'

        elif self.mode == 'xyz':
            yield 'hello world'

    def __getitem__(self, item):
        return 'I am a potato!!'

    def __len__(self):
        pass

    def keys(self):
        return iter(self.mode)


class _AWS(object):
    """
    A little different from others: unpackable
    """
    _KEYS = 'aws_access_key_id', 'aws_secret_access_key'
    _CREDENTIALS = {
        'A': ('A', 'B'),
        'AA': ('AA', 'BB'),
        'AAA': ('AAA', 'BBB')}
    __iter__ = lambda self: iter(self._.keys())
    __len__ = lambda self: len(self._.keys())
    __getitem__ = lambda self, key: self._[key]
    __init__ = lambda self, env: setattr(
        self, '_', dict(zip(self._KEYS, self._CREDENTIALS[env])))
    keys = lambda self: list(self._.keys())


if __name__ in ('__main__',):
    thing = Thing()

    # a b c
    print(*thing)

    # d e f
    print(*(x for x in thing))

    # {'hello world': 'I am a potato!!'}
    print(dict(**thing))

    AWS = _AWS('AA')
    # aws_access_key_id aws_secret_access_key
    print(*AWS)
    # {'aws_access_key_id': 'AA', 'aws_secret_access_key': 'BB'}
    print(dict(AWS))