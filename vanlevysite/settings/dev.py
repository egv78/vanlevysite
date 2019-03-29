from vanlevysite.settings.base import *

# add overwrites here

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# local settings
try:
    from vanlevysite.settings.local import *
except:
    pass

