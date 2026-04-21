from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from allauth.account.internal.flows.signup import get_frontend_url
from allauth.utils import HttpRequest, build_absolute_uri
from django.urls import reverse
from urllib.parse import urlencode


def custom_get_login_url(self, request, next_url=None, **kwargs):
    url = reverse(f'{request.resolver_match.app_name}:{self.id}'  + "_login")
    if kwargs:
        url = f"{url}?{urlencode(kwargs)}"
    
    return url

OAuth2Provider.get_login_url = custom_get_login_url

def custom_get_callback_url(self, request, app):
    callback_url = reverse(f'{request.resolver_match.app_name}:{self.provider_id}_callback')
    protocol = self.redirect_uri_protocol
    return build_absolute_uri(request, callback_url, protocol)

OAuth2Adapter.get_callback_url = custom_get_callback_url


def custom_get_signup_url(request: HttpRequest) -> str:
    url = get_frontend_url(request, "account_signup")
    if not url:
        url = build_absolute_uri(request, reverse("account_signup"))
    return url