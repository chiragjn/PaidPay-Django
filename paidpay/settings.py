"""
Django settings for paidpay project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import dj_database_url

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

STATIC_PATH = os.path.join(BASE_DIR,'static')

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    TEMPLATE_PATH,
)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b#1+y@tmjjte4$oicu=b-jhdsz4itt$_vtpz!qqu@(+acsuf3&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'paidpay.urls'

WSGI_APPLICATION = 'paidpay.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
#
#
# DATABASES['default'] = dj_database_url.config()

if os.environ.get('DATABASE_URL') is None:
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
       },
#        'salesforce': {
#     'ENGINE': 'salesforce.backend',
#     'CONSUMER_KEY': '3MVG9ZL0ppGP5UrBFABDgyW7nFdPAMpJYPxTd8BI4duHmySFYiXqh_bWAt6YRL7Wc2I27zawFWWfHXdWXLagV',
#     'CONSUMER_SECRET': '832106117558823016',
#     'USER': 'monik',
#     'PASSWORD': 'kickass911',
#     'HOST': 'https://test.salesforce.com',
# }
   }
   # DATABASES = {
   #     "default": {
   #         "ENGINE": "django.db.backends.postgresql_psycopg2",
   #         "NAME": "diskus",
   #         "USER": "",
   #         "PASSWORD": "pass",
   #         "HOST": "localhost",
   #         "PORT": "",
   #     }
   # }
else:
   DATABASES = {
       'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
#        'salesforce': {
#     'ENGINE': 'salesforce.backend',
#     'CONSUMER_KEY': '3MVG9ZL0ppGP5UrBFABDgyW7nFdPAMpJYPxTd8BI4duHmySFYiXqh_bWAt6YRL7Wc2I27zawFWWfHXdWXLagV',
#     'CONSUMER_SECRET': '832106117558823016',
#     'USER': 'monik@etiole.com',
#     'PASSWORD': 'kickass911',
#     'HOST': 'https://login.salesforce.com',
# }
   }

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# DATABASE_ROUTERS = [
#     "salesforce.router.ModelRouter"
# ]

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    STATIC_PATH,
)
