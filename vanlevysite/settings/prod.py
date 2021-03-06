from vanlevysite.settings.base import *

# add overwrites here

DEBUG = False

# change ALLOWED_HOSTS on launch
ALLOWED_HOSTS = ['184.73.138.122', 'www.vanlevy.com', '.vanlevy.com']
# 35.175.146.205

ADMIN_MEDIA_PREFIX = '/static/admin/'

INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    'vanlevy.apps.VanlevyConfig',
    'swdice.apps.SwdiceConfig',
    'gendice.apps.GendiceConfig',
    'polydice.apps.PolydiceConfig',
    'myzdice.apps.MyzdiceConfig',
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


# STATIC_URL = 'http://www.vanlevy.com.s3-website.us-east-2.amazonaws.com/static/'
# STATIC_ROOT = 'http://www.vanlevy.com.s3-website.us-east-2.amazonaws.com/'
STATIC_URL = 'https://d10yucgh4c5knj.cloudfront.net/static/'
STATIC_ROOT = 'https://d10yucgh4c5knj.cloudfront.net/'
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

# trying something
# CONN_MAX_AGE = 1800
# end database

# Email Settings
EMAIL_HOST = auth_dict['smtp_host']
EMAIL_PORT = 587
EMAIL_HOST_USER = auth_dict['smtp_username']
EMAIL_HOST_PASSWORD = auth_dict['smtp_password']
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = 'webmaster@vanlevy.com'

