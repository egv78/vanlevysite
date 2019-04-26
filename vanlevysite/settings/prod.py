from vanlevysite.settings.base import *

# add overwrites here

DEBUG = False

# change ALLOWED_HOSTS on launch
ALLOWED_HOSTS = ['35.175.243.191', 'www.vanlevy.com', '.vanlevy.com']

ADMIN_MEDIA_PREFIX = '/static/admin/'

INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    'vanlevy.apps.VanlevyConfig',
    'swdice.apps.SwdiceConfig',
    'gendice.apps.GendiceConfig',
    'polydice.apps.PolydiceConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'storages',
]

# STATIC FILES
AWS_ACCESS_KEY_ID = auth_dict['aws_access_key_id']
AWS_SECRET_ACCESS_KEY = auth_dict['aws_secret_access_key']

AWS_PROFILE = 's3-full-access-user'
AWS_STORAGE_BUCKET_NAME = 'www.vanlevy.com'
AWS_S3_CUSTOM_DOMAIN = '%s.s3-website.us-east-2.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
AWS_DEFAULT_ACL = None

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'vanlevysite/static'),
]

STATIC_URL = '//www.vanlevy.com.s3-website.us-east-2.amazonaws.com/static/'
STATIC_ROOT = 'http://www.vanlevy.com.s3-website.us-east-2.amazonaws.com/'
# end static files

# DATABASE
DB_USER = auth_dict['db_user']
DB_PASSWORD = auth_dict['db_password']
DB_HOST = auth_dict['db_host']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'alphatesting',
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': 5432,
    }
}
# end database

