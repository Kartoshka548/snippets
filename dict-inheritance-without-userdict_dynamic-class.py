import pprint


email_directory = type('event2email', (dict,), {
    'get': lambda _, *__: __[0] in _ and _[__[0]] or len(__) == 2 and __[1] or None,
    '__getitem__': lambda *_: dict.__getitem__(*_) % _[0]})({
        '_domain':           '@yourdomain.extension',

        # actual email addresses to use per event type
        'no-reply':         'do-not-reply%(_domain)s',
        'info':             'info%(_domain)s',
        'notifications':    'notifications%(_domain)s',
        'john':             'john.smith%(_domain)s',

        # existing event types, which can be expanded live
        # with regular dictionary methods
        1: '%(john)s',
        2: '%(no-reply)s',
        3: '%(notifications)s',
        4: '%(info)s',
        # ...
})


def tester(keys, dct, prefix='_'):
    """
    1. Get a key from a dict with implicit .__getitem__
    2. Set into the dict another pair with a prefix prepended
        to both key and the value,
    3. then get new additions with .get

    As dct is a mutable type, unless copied new values will be preserved after
    function has finished running. If this behaviour is not desired,
    .copy must be used before calling this function.
    """
    _prefix = prefix
    original_dct = dct.copy()
    for event_id in keys:

        # __getitem__
        val = dct[event_id]
        print(val)

        # inherited __setitem__
        new_key = '%s%s' % (_prefix, event_id)
        dct[new_key] = '%s%s' % (_prefix, val)

        # __get__
        print(dct.get(new_key))
        print()
    else:
        #### sets are nice but overkill with conversions for this case
        # diff = set(dct.keys()) - set(original_dct.keys())
        # from functools import reduce
        # diff = reduce(set.difference, (set(d.keys()) for d in (dct, original_dct)))
        # diff = set.difference(*(set(dct.keys()), set(original_dct.keys())))

        diff = {k: v for (k, v) in dct.items() if k not in original_dct}

        print('Original email_directory:')
        pprint.pprint(original_dct, indent=4)
        print('\nNew values added:')
        pprint.pprint(diff, indent=4)


if __name__ == "__main__":
    if __import__('sys').version_info.major < 3:
        print('Tested with Python 2.7.5')


    keys = 2, 3, 'john'
    tester(keys, email_directory, prefix='___')


# do-not-reply@yourdomain.extension
# ___do-not-reply@yourdomain.extension
#
# notifications@yourdomain.extension
# ___notifications@yourdomain.extension
#
# john.smith@yourdomain.extension
# ___john.smith@yourdomain.extension
#
# Original email_directory:
# {   1: '%(john)s',
#     2: '%(no-reply)s',
#     3: '%(notifications)s',
#     4: '%(info)s',
#     '_domain': '@yourdomain.extension',
#     'info': 'info%(_domain)s',
#     'john': 'john.smith%(_domain)s',
#     'no-reply': 'do-not-reply%(_domain)s',
#     'notifications': 'notifications%(_domain)s'}
#
# New values added:
# {   '___2': '___do-not-reply@yourdomain.extension',
#     '___3': '___notifications@yourdomain.extension',
#     '___john': '___john.smith@yourdomain.extension'}
