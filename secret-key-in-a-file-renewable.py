import os
import random
import string
import time
 
########## KEY CONFIGURATION (for threaded server)
def secret_key_gen(path, max_age=86400):
    """
    # Try to load the SECRET_KEY from our SECRET_FILE. If that fails, then generate
    # a random SECRET_KEY and save it into our SECRET_FILE for future loading. If
    # everything fails, then just raise an exception.
 
    # Absolute filesystem path to the secret file which holds this project's
    # SECRET_KEY. Will be auto-generated the first time this file is interpreted.
    """
 
    SECRET_FILE = os.path.join(path, 'random_hash')
    try:
        # for multiserver / distributed setup:
        # VMs should be taken out of order in periodic fashion
 
        _last_modified = os.stat(SECRET_FILE).st_mtime
        lifecycle = (time.time() - _last_modified)

       # update hash if file age is older than allowed
        if (lifecycle / max_age) >= 1: raise IOError
        SECRET_KEY = open(SECRET_FILE).read().strip()

    except (OSError, IOError):
        try:
            with open(SECRET_FILE, 'w') as f:
                SECRET_KEY = ''.join(
                    random.SystemRandom().choice(string.printable) for c in range(32))
                f.write(SECRET_KEY)

        except IOError:
            raise Exception('Cannot open file `%s` for writing.' % SECRET_FILE)

    return SECRET_KEY

 
 
INTERNAL_BRIDGE_PROTOCOL = {

    # update inside senders and verify on receivers
    'source': None,

    'hash': secret_key_gen(
        path=os.path.dirname(__file__),
        max_age=60 * 60 * 24),      # a day
    # 'hash': ''.join(random.SystemRandom().choice(
    #     string.printable) for _ in range(32))
}
 