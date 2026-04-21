from apps.user.utils.pathresolver import getname_reversepath

from django.http import HttpRequest
from allauth.core.internal.httpkit import get_frontend_url
from allauth.utils import build_absolute_uri
from django.urls import reverse
from allauth.core.internal.httpkit import headed_redirect_response

from allauth.account.internal.flows import signup, email_verification
from allauth.socialaccount.internal.flows import signup
def custom_get_signup_url(request: HttpRequest) -> str:
    url = get_frontend_url(request, "account_signup")
    if not url:
        url = build_absolute_uri(request, getname_reversepath(request, "account_signup"))
    return url

signup.get_signup_url = custom_get_signup_url

def custom_get_email_verification_url(request: HttpRequest, emailconfirmation) -> str:
    url = get_frontend_url(request, "account_confirm_email", key=emailconfirmation.key)
    if not url:
        url = reverse(getname_reversepath(request, "account_confirm_email"), args=[emailconfirmation.key])
        url = build_absolute_uri(request, url)
    return url

email_verification.get_email_verification_url = custom_get_email_verification_url


# from urllib.parse import quote
# from core import settings
# from utils.pathresolver import getname_reversepath

# from django.http import HttpRequest
# from allauth.core.internal.httpkit import get_frontend_url
# from allauth.utils import build_absolute_uri
# from django.urls import reverse
# from allauth.account import app_settings
# from allauth.account.adapter import get_adapter
# from allauth.account.app_settings import LoginMethod


# def get_reset_password_from_key_url(request: HttpRequest, key: str) -> str:
#     url = get_frontend_url(request, "account_reset_password_from_key", key=key)
#     if not url:
#         path = reverse(f'{request.resolver_match.namespace}:account_reset_password_from_key', 
#                        kwargs={"uidb36": "UID", "key": "KEY"}
#         )
#         path = path.replace("UID-KEY", quote(key))
#         url = build_absolute_uri(request, path)
#     return url

# def get_email_verification_url(request: HttpRequest, emailconfirmation) -> str:

#     url = get_frontend_url(request, "account_confirm_email", key=emailconfirmation.key)
#     if not url:
#         url = reverse(getname_reversepath(request, "account_confirm_email"), args=[emailconfirmation.key])
#         url = build_absolute_uri(request, url)
#     return url

# def send_unknown_account_mail(request: HttpRequest, email: str) -> None:
#     if not app_settings.EMAIL_UNKNOWN_ACCOUNTS:
#         return None
#     signup_url = get_signup_url(request)
#     context = {
#         "request": request,
#         "signup_url": signup_url,
#     }
#     get_adapter().send_mail("account/email/unknown_account", email, context)
# def get_signup_url(request: HttpRequest) -> str:
#     url = get_frontend_url(request, "account_signup")
#     if not url:
#         url = build_absolute_uri(request, getname_reversepath(request,"account_signup"))
#     return url

# def request_password_reset(request, email: str, users, token_generator) -> None:
#     from allauth.account.utils import user_pk_to_url_str, user_username

#     if not users:
#         send_unknown_account_mail(request, email)
#         return
#     adapter = get_adapter()
#     for user in users:
#         temp_key = (
#             token_generator or settings.PASSWORD_RESET_TOKEN_GENERATOR()
#         ).make_token(user)

#         uid = user_pk_to_url_str(user)

#         key = f"{uid}-{temp_key}"
#         url = adapter.get_reset_password_from_key_url(key)
#         context = {
#             "user": user,
#             "password_reset_url": url,
#             "uid": uid,
#             "key": temp_key,
#             "request": request,
#         }

#         if LoginMethod.USERNAME in settings.LOGIN_METHODS:
#             context["username"] = user_username(user)
#         adapter.send_password_reset_mail(user, email, context)

# def send_unknown_account_mail(request: HttpRequest, email: str) -> None:
#     if not app_settings.EMAIL_UNKNOWN_ACCOUNTS:
#         return None
#     signup_url = get_signup_url(request)
#     context = {
#         "request": request,
#         "signup_url": signup_url,
#     }
#     get_adapter().send_mail("account/email/unknown_account", email, context)