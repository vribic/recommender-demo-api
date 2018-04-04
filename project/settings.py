"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import datetime
import os
import django_heroku
import dj_database_url
from decouple import config, Csv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Disable Django's own staticfiles handling in favour of WhiteNoise, for
    # greater consistency between gunicorn and `./manage.py runserver`. See:
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    #'whitenoise.runserver_nostatic',


    'django.contrib.staticfiles', # TODO uncomment


    'storages',     # Needed for AWS S3
    'django_extensions',  # Needed for running django-jupyter notebooks
    'rest_framework',
    'corsheaders',  # Needed when calling API from different domain (CORS requests)
    'app',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(default=config('DATABASE_URL'))
}

# Email
# Setting up the email server
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# EMAIL_USE_TLS = True
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
# EMAIL_PORT = config('EMAIL_PORT')


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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# REST framework configuration

#LOGIN_REDIRECT_URL = '/api' # TODO what's this?
import project.project_config as project_config

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS' : 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': project_config.GALLERY_IMG_NUM
}


JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=60*30) # 30 minutes of token time
}

# Needed for CORS requests ( front and back end served from same domain, different port)
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    '.herokuapp.com',
)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# Uncomment when using AWS storage
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/'),
]


# # Running ./manage.py collectstatic will go into /static/ as defined in STATICFILES_DIRS
# # And collect all data to new STATIC_ROOT in /staticfiles/. It is
# # possible to access that data from localhost:8000/static/v1/full/path/to/resource/only/file.txt.
# # No half way paths are allowed.
# STATIC_URL='/static/v1/'
# STATIC_ROOT ='staticfiles/'

# Also if you define STATICFILES_DIR & STATIC_URL or
# STATIC_ROOT & STATIC_URL you can access the files from browser.
# Third option is to remove 'django.contrib.staticfiles' from apps and
# add the URL and ROOT manually to urls via static.

# If you are fetching images from localhost keep this value.
# If you're testing AWS storage, uncomment the other one.
# STATIC_URL='/static/'
# STATIC_ROOT ='static/'


if DEBUG:
    # Media config
    MEDIA_URL = '/media/'
    MEDIA_ROOT = 'media/'

# AWS S3 service configuration

# Most importat part are the access keys ane secret
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME =config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN ='%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_QUERYSTRING_AUTH = False # This will make sure that the file URL does not have unnecessary parameters like your access key.
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}


# AWS file structure configuration
AWS_LOCATION = 'static' # From the root of the AWS service, this is the path to which the static files will be stored on service
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage' # The collectstatic executor storage engine
DEFAULT_FILE_STORAGE = 'project.storage_backends.MediaStorage'

# # Activate Django-Heroku.
# # TODO this line messes up the S3 upload :/
# #django_heroku.settings(locals())
