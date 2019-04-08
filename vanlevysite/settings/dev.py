from vanlevysite.settings.base import *

# local settings
try:
    from vanlevysite.settings.prod import *
except:
    pass

# add overwrites here

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

