from collections import UserDict


class CustomDict(UserDict):
    """
    In case of UserDict, unpacking `self` is the same as unpacking `self.data`
    """
    def __init__(self, dct={}):
        self.data = dct

    def __add__(self, other={}):
        """
        Returning new object of the same type
        """
        return __class__({**self.data, **other})

    def __iadd__(self, other={}):
        """
        Returning same object, modified in-place
        """
        self.update(other)
        return self


# >>> d = CustomDict({'key': 'value', 'key2': 'value2'})
# >>> d, d.data, type(d), id(d)
# ({'key': 'value', 'key2': 'value2'}, {'key': 'value', 'key2': 'value2'}, <class '__main__.CustomDict'>, 4320232616)

# Adding other dict (or any mapping type) to it will call __add__, returning new object:
# >>> mixin = {'a': 'aaa', 'b': 'bbb'} # plain dict
# >>> d_new = d + mixin # __add__
# >>> d_new, type(d_new), id(d_new)
# ({'key': 'value', 'key2': 'value2', 'a': 'aaa', 'b': 'bbb'}, <class '__main__.CustomDict'>, 4320232728)
# >>> d, id(d)
# ({'key': 'value', 'key2': 'value2'}, 4320232616)

# In-place modification with __iadd__ will return the same object (same id in memory)
# >>> d += {'a': 'aaa', 'b': 'bbb'} # __iadd__
# >>> d, type(d), id(d)
# ({'key': 'value', 'key2': 'value2', 'a': 'aaa', 'b': 'bbb'}, <class '__main__.CustomDict'>, 4320232616)


# --------------------------------------------------------
def unpack(**kwargs):
    """
    Collect all keyword arguments under one hood
    and print them as 'key: value' pairs
    """
    for key_value in kwargs.items():
       print('key: %s, value: %s' % key_value)


class MyMapping(object):
    """
    Class that acts as `mapping` for **unpacking
    """
    def keys(self):
        return ['a', 'b']

    def __getitem__(self, key):
        return key.upper()


# >>> unpack(**MyMapping())
# key: a, value: A
# key: b, value: B
