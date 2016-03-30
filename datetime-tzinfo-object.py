import datetime
# datetime to unix timestamp utility

class UTC(datetime.tzinfo):
    """
    UTC tzinfo object

    oneliner:
        UTC = type(
            'UTC',
            (datetime.tzinfo,),
            {'utcoffset': lambda *_: datetime.timedelta(0)})

    (almost) proper OO;
        # utcoffset = lambda *args: _ZERO
        # tzname = lambda *args: "UTC"
        # dst = utcoffset
    """
    __getattribute__ = lambda self, attr: (
        (lambda *_: self.__class__.__name__)
            if attr in ('tzname',) else
        (lambda *_: datetime.timedelta(0)))


EPOCH = datetime.datetime(1970, 1, 1, tzinfo=UTC())
to_timestamp = lambda dtobj: int((dtobj - EPOCH).total_seconds())