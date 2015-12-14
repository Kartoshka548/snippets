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


if __name__ == "__main__":
    if __import__('sys').version_info.major < 3:
        print('Tested with Python 2.7.5')

    print(email_directory[2])
    # >>> do-not-reply@yourdomain.extension

    print(email_directory[3])
    # >>> notifications@yourdomain.extension

    print(email_directory['john'])
    # >>> john.smith@yourdomain.extension


