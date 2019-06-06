from vanlevysite.settings.base import *

# local settings
# normal settings
DEBUG = True

# testing when out of Debug
# DEBUG = False
# ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

# add overwrites here

# https://stackoverflow.com/questions/5802189/django-errno-111-connection-refused
# python -m smtpd -n -c DebuggingServer localhost:1025
# run in separate command prompt - admin mode
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
DEFAULT_FROM_EMAIL = 'webmaster@vanlevy.com'

