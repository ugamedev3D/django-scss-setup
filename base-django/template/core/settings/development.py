import os

from .allauth import *

from environ import environ

env = environ.Env(
    DEBUG=(bool, False)
)

env.read_env(BASE_DIR / ".env")

DEBUG = True

ALLOWED_HOSTS = []

# SECURITY WARNING: keep the secret key used in production secret!
# For development stage use a generate a new random key every server run 
# for production check production.py 
SECRET_KEY = env("DJANGO_SECRET_KEY")


# Use install debugger applications  
INSTALLED_APPS += [
    'livereload',
]

MIDDLEWARE += [
    'livereload.middleware.LiveReloadScript', 
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3'
    }
}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'VERIFIED_EMAIL': True,
        'APP': {
            'client_id': env('OAUTH_GOOGLE_CLIENT_ID'),
            'secret':  env('OAUTH_GOOGLE_SECRET'),
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
            'client_id': env('OAUTH_FACEBOOK_CLIENT_ID'),
            'secret':  env('OAUTH_FACEBOOK_SECRET'),
        },
        'SCOPE': {
            'profile',
        },
        'AUTH_PARAMS': {
            'access_type' : 'reauthenticate',
        },
    }
}

STORAGES = {
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
        ),
    }
}

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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


# Email backend 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


COMPRESS_ENABLED = True