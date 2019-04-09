from vanlevysite.settings.base import *

# local settings
try:
    from vanlevysite.settings.prod import *
except:
    pass

# add overwrites here

DEBUG = True

EMAIL_HOST = auth_dict['smtp_host']
EMAIL_PORT = 587
EMAIL_HOST_USER = auth_dict['smtp_username']
EMAIL_HOST_PASSWORD = auth_dict['smtp_password']
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = 'webmaster@vanlevy.com'
