# https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers


class OpenRead(object):
    """Return an object to iterate over."""

    def __init__(self, fname, mode='r'):
        self.f_name = fname
        self.mode = mode
        self.fd = None  # good practice to allocate

    def __enter__(self):
        self.fd = open(self.f_name, self.mode)
        return self.fd  # file object which can be iterated over later on

    def __exit__(self, exc_type, exc_value, traceback):
        self.fd.close()

        # The proper procedure is to raise the new exception inside of the __exit__ handler.
        if exc_type:
            # Exception that was passed in, though, should not be re-raised.

            # To allow for context manager chaining,
            # false-y value should be returned from the handler.
            # return False  # re-raise current exception

            return True  # ignore current exception

            # Raising your own exceptions is however perfectly fine.
            # raise Exception('Standard')

        return None


class ItemProcessor:
    """Same thing"""

    def __init__(self, fname, item_start, item_end, mode='r'):
        self.f_name = fname
        self.mode = mode
        self.item_start = item_start
        self.item_end = item_end
        self.empty = ''

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __enter__(self):
        def _generator():
            output = self.empty
            _content = False
            with open(self.f_name, self.mode) as fd:

                for line in fd:
                    if self.item_start in line:
                        output = line  # start collecting
                        _content = True

                    elif self.item_end in line:
                        # flush
                        yield output+line
                        # and reset
                        output = self.empty
                        _content = False

                    elif _content:
                        # collect
                        output += line

        return _generator()


# yes a func!
def content_generator(fname, item_start, item_end):
    with open(fname, 'r') as fd:
        _content = False
        output = empty = ''
        for line in fd:
            if item_start in line:
                _content = True
            elif item_end in line:
                yield output+line
                output = empty
                _content = False
            elif _content:
                output += line


if __name__ == '__main__':

    filename = 'userdict-with-__add__-and-__iadd__.py'
    sep = '='*20
    msg = "-*%s An item %s*-\n%%s" % (sep, sep)


    # example
    try:
        with OpenRead(filename, 'r') as sample_read_fd:
            count = sum([len(line) for line in sample_read_fd], 0)
            555/0  # raise ZeroDivisionError
    except ZeroDivisionError as err:
        print(err)
    else:
        print("Counted %d characters in a %s" % (count, filename))


    # example
    with ItemProcessor(filename, item_start='def', item_end='return') as IProc:
        for item in IProc: # over returned generator
            print(msg % item)


    # example, simplified
    for item in content_generator(filename, 'def', 'return'):
        print(msg % item)
