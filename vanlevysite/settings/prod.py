from vanlevysite.settings.base import *

# add overwrites here

DEBUG = True

# change ALLOWED_HOSTS on launch
ALLOWED_HOSTS = ['18.191.142.81']

# local settings
try:
    from vanlevysite.settings.local import *
except:
    pass


# these handle STATIC FILES
STATIC_URL = '//www.vanlevy.com.s3-website.us-east-2.amazonaws.com/static/'
STATIC_ROOT = 'http://www.vanlevy.com.s3-website.us-east-2.amazonaws.com/'
# end static files


# MEDIA FILES
# INSTALLED_APPS += 'storages'
# DEFAULT_FILE_STORAGE = 'mysite.storage_backends.MediaStorage'
# MEDIA_URL = '//vanlevysite/media/'

# DATABASE
