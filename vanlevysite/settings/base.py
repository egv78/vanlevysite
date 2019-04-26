import os
import csv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open(os.path.join(BASE_DIR, 'vanlevysite/settings/auth.csv'), mode='r') as infile:
    reader = csv.reader(infile)
    auth_dict = {rows[0]:rows[1] for rows in reader}

SECRET_KEY = auth_dict['secret_key']

# with open(os.path.join(BASE_DIR, 'vanlevysite/settings/secret_key.txt')) as f:
#     SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = []


# Application definition

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
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.middleware.LoginRequiredMiddleware'
]

ROOT_URLCONF = 'vanlevysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['vanlevy/templates', 'accounts/templates', 'swdice/templates', 'gendice/templates',
                 'polydice/templates'
                 ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'vanlevysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = ''
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static/'), )

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'vanlevysite/media/')

LOGIN_REDIRECT_URL = '/portal/'

LOGIN_URL = '/accounts/login/'
LOGIN_REQUIRED_URL = '/accounts/login_required/'

LOGIN_EXEMPT_URLS = (
    # Admin login pages
    '/admin/',
    '/admin/login/'
    # VanLevy pages - all but Portal
    '',
    '/',
    '/about/',
    '/cool-stuff/',
    '/home/',
    '/resources/',
    '/dice-rollers/',
    '/terms/',
    # Accounts pages - About and necessary to login/logout, register, reset password
    # Accounts login is handled explicitly in middleware
    LOGIN_REQUIRED_URL,
    '/accounts/',
    '/accounts/logout/',
    '/accounts/register/',
    '/accounts/register/success/',
    '/accounts/password-reset/',
    '/accounts/password-reset/done/',
    '/accounts/password-reset/confirm/',
    '/accounts/password-reset/complete/',
    # Dice Rollers - only About pages
    '/swdice/',
    '/gendice/',
    '/polydice/',
)


# User substitution
AUTH_USER_MODEL = 'accounts.VanLevyUser'

# Email as authentication backend
AUTHENTICATION_BACKENDS = ['vanlevysite.settings.emailbackend.CustomBackend']
