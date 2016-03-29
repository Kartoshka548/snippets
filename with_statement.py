# https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers


class OpenRead(object):

    def __init__(self, fname, mode='r'):
        self.f_name = fname
        self.mode = mode
        self.fd = None  # good practice to allocate

    def __enter__(self):
        self.fd = open(self.f_name, self.mode)
        return self.fd

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


if __name__ == '__main__':

    filename = 'userdict-with-__add__-and-__iadd__.py'

    with OpenRead(filename, 'r') as sample_read_fd:
        count = sum([len(line) for line in sample_read_fd], 0)
        555/0  # raise ZeroDivisionException

    print("Counted %d characters in a %s" % (count, filename))
