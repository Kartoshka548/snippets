import itertools
from timeit import timeit


def split(d):
    """
    From multivalue dict structure,
      d = {
        'email': ['e_val1', 'e_val2', 'e_val3', 'e_val4', 'e_val5'],
        'id'   : ['i_val1', 'i_val2', 'i_val3', 'i_val4'],
        'ref'  : ['r_val1', 'r_val2', 'r_val3', 'r_val4']}
    get the following list of individual dicts
      l = [
        {'email': 'e_val1', 'id': 'i_val1', 'ref': 'r_val1'},
        {'email': 'e_val2', 'id': 'i_val2', 'ref': 'r_val2'},
        {'email': 'e_val3', 'id': 'i_val3', 'ref': 'r_val3'},
        {'email': 'e_val4', 'id': 'i_val4', 'ref': 'r_val4'},
        {'email': 'e_val5', 'id': None, 'ref': None}]
    """
    l = []
    longest = max(len(l_) for l_ in d.values())

    for pointer in range(longest):
        r = {}
        for k, v in d.items():
            try:
                r[k] = v[pointer]
            except IndexError:
                # current list is shorter than longest
                r[k] = None
        l.append(r)
    return l

# take two
def split(d):
    """
    With Python < 2.7,
      - itertools.izip_longest(*d.values())
    might be substituted by map with None:
      - map(None, *d.values())
    """
    _zipper = lambda keys: lambda v: dict(zip(keys, v))
    lmb = _zipper(d.keys())
    return map(
        lmb,
        itertools.izip_longest(*d.values()))


# with map
timeit(setup="""
d={'email': ['e_val1', 'e_val2', 'e_val3', 'e_val4', 'e_val5'],
       'id': ['i_val1', 'i_val2', 'i_val3', 'i_val4'],
       'ref': ['r_val1', 'r_val2', 'r_val3', 'i_val4']};
_zipper=lambda keys: lambda v: dict(zip(keys, v))""",
stmt="""
lmb=_zipper(d.keys());
map(lmb, map(None, *d.values()))""")
# 16.14903998374939

# with itertools.izip_longest
timeit(setup="""
d={'email': ['e_val1', 'e_val2', 'e_val3', 'e_val4', 'e_val5'],
   'id': ['i_val1', 'i_val2', 'i_val3', 'i_val4'],
   'ref': ['r_val1', 'r_val2', 'r_val3', 'i_val4']};
_zipper=lambda keys: lambda v: dict(zip(keys, v))""",
stmt="""
lmb=_zipper(d.keys());
map(lmb, izip_longest(*d.values()))""")
# 18.98265790939331