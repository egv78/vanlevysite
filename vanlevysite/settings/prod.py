from vanlevysite.settings.base import *

# add overwrites here

DEBUG = False
# change ALLOWED_HOSTS on launch
ALLOWED_HOSTS = ['3.16.166.171']

# local settings
try:
    from vanlevysite.settings.local import *
except:
    pass

