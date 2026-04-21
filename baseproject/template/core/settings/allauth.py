from .base import *

INSTALLED_APPS += [
    #allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #allauth MFA
    
    #allauth providers app
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
]
MIDDLEWARE += [
    'allauth.account.middleware.AccountMiddleware',
]

SITE_ID = 1

AUTH_USER_MODEL = 'user.User'

ACCOUNT_ADAPTER = 'apps.user.adapter.CustomAccountAdapter'

ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']

PASSWORD_RESET_BY_CODE_ENABLED = True


LOGIN_REDIRECT_URL = '/'

SOCIALACCOUNT_ADAPTER = 'apps.user.socialaccount.adapters.CustomSocialAccountAdapter'
SOCIALACCOUNT_ENABLED = True
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True


# User avatar compress setting
AVATAR_SIZE = (100, 100)
AVATAR_QUALITY = 80

# to get DEFAULT_FROM_EMAIL
DEFAULT_FROM_EMAIL = ""