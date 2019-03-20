"""
Django settings for webapp project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.realpath(os.environ.get(
    'DB_DIR', # try to get dir from environment
    os.path.join(BASE_DIR, 'db') # fallback to db/ in project dir
    ))
DJANGO_DB = os.path.join(DB_DIR, os.environ.get('DJANGO_DB', 'db.sqlite3'))
INTERPRETER_DB = os.path.join(DB_DIR, os.environ.get('INTERPRETER_DB', 'interpreter.sqlite3'))
LOG_DIR = os.path.realpath(os.environ.get('LOG_DIR', 'logs'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
USE_DEBUG = os.environ.get('DJANGO_DEBUG', False)
if USE_DEBUG:
    USE_DEBUG = True
DEBUG = USE_DEBUG

# https://docs.djangoproject.com/en/2.1/ref/settings/#allowed-hosts
# change this for production deployment
ALLOWED_HOSTS = ['*']

# save process ID to file
PID_FILE = os.path.join(LOG_DIR, 'IR-interpreter.pid')
PID = os.getpid()
with open(PID_FILE, "w") as f:
    f.write(str(PID))

# also see these:
# https://docs.djangoproject.com/en/2.1/topics/logging/
# conda/lib/python3.6/site-packages/django/utils/log.py
# conda/pkgs/django-2.1.2-py36_1000/lib/python3.6/site-packages/django/conf/global_settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'datefmt' : '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },
        'custom': {
            'datefmt' : '%Y-%m-%d %H:%M:%S',
            'format': '[%(asctime)s] %(levelname)s (%(name)s:%(module)s:%(funcName)s:%(lineno)d) %(message)s'
        },
        'pid': {
            'datefmt' : '%Y-%m-%d %H:%M:%S',
            'format': ' %(message)s [%(asctime)s]'
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'debug.log'),
            'formatter': 'custom',
        },
        'pid': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'pid'),
            'formatter': 'pid',
        },
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'console_custom' : {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'custom',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        '' : { # catch-all logger
            'handlers': ['file', 'console_custom'],
            'level': 'DEBUG',
            'propagate': True,
            },
        'interpreter.views': {
            'handlers': ['file', 'console_custom'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'pid': {
            'handlers': ['pid'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'interpreter'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webapp.urls'

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
        },
    },
]

WSGI_APPLICATION = 'webapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DJANGO_DB, # os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'interpreter_db': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': INTERPRETER_DB,
    },
}

DATABASE_ROUTERS = ['interpreter.routers.Router']

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
