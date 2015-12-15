import os
from pprint import pprint as pp

class Conf(dict):
    """
    Returns default configuration for missing environments.
    """
    def __init__(self, dct: dict, env: str) -> None:
        self._d = dct
        self._e = env

    def __call__(self, *args):
        _a = args+(self._e,)
        return self.lookup(self._d, _a)

    def _lookup():
        """
        Recursively looks for default nested value in a dictionary,
        or return default value if defined.

        Using similar idea of decorators, exception-raiser `_key_not_found`
        is accessible only within and by `enclosed`.
        """
        def _key_not_found(*args):
            raise KeyError('%s was not found in %s' % args[::-1])
        def enclosed(_d, keys):
            _k = keys[0]
            if _k not in _d:
                return _d.get('default') or _key_not_found(_d, _k)
            if isinstance(_d[_k], dict):
                _val = enclosed(_d[_k], keys[1:])
            else:
                return _d[_k]
            return _val
        return enclosed
    lookup = staticmethod(_lookup())


def launchpad(env, config):
    """
    Configuration parameters.
    Populates global namespace from within a function.
    """
    _conf = Conf(env=env, dct=config)
    global PROJ_DBHOST, \
        PROJ_USER, \
        PROJ_PASSWORD, \
        PROJ_PORT, \
        PROJ_PROJECT_ROOT

    # setting globals from inside function
    PROJ_DBHOST  = _conf('DATABASE', 'DB_HOST')
    PROJ_USER = _conf('DATABASE', 'DB_USER')
    PROJ_PASSWORD = _conf('DATABASE', 'DB_PASSWORD')
    PROJ_PORT = _conf('DATABASE', 'DB_PORT')
    PROJ_PROJECT_ROOT = _conf('PROJECT_ROOT')

    # for visual representation,
    # globals already populated above
    return {
        'DBHOST': PROJ_DBHOST,
        'USER': PROJ_USER,
        'PASSWORD': PROJ_PASSWORD,
        'PORT': PROJ_PORT,
        'PROJECT_ROOT': PROJ_PROJECT_ROOT}


if __name__ == '__main__':

    if __import__('sys').version_info.major < 3:
        print('Tested with Python 3.5')

    # define environment, 'PYTHONPATH' is used for demo only
    _env = 'PYTHONPATH'
    environment = os.environ.get(_env)
    assert environment, 'No %s found. Aborting execution.' % _env

    config = {
        'PROJECT_ROOT': os.path.dirname(__file__),
        'DATABASE': {
            'DB_USER':     'root',
            'DB_PASSWORD': 'root',
            'DB_PORT':     9999,
            'DB_HOST': {
                'LOCALHOST':    '1.1.1.1',
                'DEV_REMOTE':   '2.2.2.2',
                'STAGING':      '3.3.3.3',
                'PRODUCTION':   '4.4.4.4',
                'default':      '0.0.0.0'}}}
    settings = launchpad(environment, config)

    printable = ('%s=%s' % tpl for tpl in settings.items())
    print(', '.join(printable))
    pp({k: v for (k, v) in globals().items() if k.startswith('PROJ_')})


#################
# PORT=9999, DBHOST=0.0.0.0, PROJECT_ROOT=..., PASSWORD=root, USER=root
#
# {'PROJ_DBHOST': '0.0.0.0',
#  'PROJ_PASSWORD': 'root',
#  'PROJ_PORT': 9999,
#  'PROJ_PROJECT_ROOT': '...',
#  'PROJ_USER': 'root'}
