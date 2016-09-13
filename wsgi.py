import os
import site
import subprocess
import sys

homepath = os.path.expanduser('~')
pwd = os.path.dirname(os.path.realpath(__file__))

# virtualenv on EC2 and on devserver is named differently.
# let's try to recognize if it's a ec2 instance or something else.
proc = subprocess.Popen(
    stdout=subprocess.PIPE,
    args=('bash',
          '-c',
          """if [ -f /sys/hypervisor/uuid ] && [ `head -c 3 /sys/hypervisor/uuid` == ec2 ];
          then echo "/.virtualenvs/...A"
          else echo "/.virtualenv/...B"
          fi"""))  # TODO: recreate local virtualenv as `...A or ...B`
environment = proc.stdout.read().strip()
proc.terminate()

VIRTUALENV_PATH = homepath + environment

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir(VIRTUALENV_PATH + '/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append(homepath + '...')

os.environ['DJANGO_SETTINGS_MODULE'] = '...settings'

# loading environment variables from a file
env_file = '.environment_variables'
proc = subprocess.Popen(
    stdout=subprocess.PIPE,
    args=('bash',
          '-c',
          'source %s/%s && env | grep SERVER' % (pwd, env_file)))
for line in proc.stdout:
    key, value = line.strip().split("=")
    os.environ[key] = value
proc.communicate()

# Activate your virtual env
activate_env = VIRTUALENV_PATH + "/bin/activate_this.py"

# Python2
execfile(
    activate_env,
    {'__file__': activate_env})

# with Python3, there's no execfile anymore
# exec(open(activate_env).read())
# with open(activate_env) as f:
#     code = compile(f.read(), "activate_this.py", 'exec')
#     exec(code, globals(), locals())


# now when django is available, serve it
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
