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
    'whitenoise.middleware.WhiteNoiseMiddleware',   # this is the new bit
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'static'))
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'vanlevy/'),
                    os.path.join(BASE_DIR, 'swdice/'),
                    os.path.join(BASE_DIR, 'accounts/'),
                    ]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# end static files

