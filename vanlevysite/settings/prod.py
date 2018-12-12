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


# these handle static files
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# end static files

