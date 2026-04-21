from .allauth import *
import os
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = []

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Email backend 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'example@email.com'
EMAIL_HOST_PASSWORD = 'host_password'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'VERIFIED_EMAIL': True,
        'APP': {
            'client_id': os.environ.get('OAUTH_GOOGLE_CLIENT_ID'),
            'secret':  os.environ.get('OAUTH_GOOGLE_SECRET'),
        },
        'SCOPE': {
            'profile',
            'email'
        },
        'AUTH_PARAMS': {
            'access_type' : 'online',
            'prompt' : 'consent'
        },
    },
    'facebook': {
         'APP': {
            'client_id': os.environ.get('OAUTH_FACEBOOK_CLIENT_ID'),
            'secret':  os.environ.get('OAUTH_FACEBOOK_SECRET'),
        },
        'SCOPE': {
            'profile',
        },
        'AUTH_PARAMS': {
            'access_type' : 'reauthenticate',
        },
    }
}

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True