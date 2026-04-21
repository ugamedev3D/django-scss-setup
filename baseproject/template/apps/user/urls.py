from django.urls import include, path

from apps.user import views
from apps.user.views import MySignupView, MyLoginView, MyPasswordResetView
from allauth.account.views import PasswordResetView, SignupView

from allauth.urls import build_provider_urlpatterns
from django.conf import settings

app_name = 'user'

urlpatterns = [
   path('account/login/', MyLoginView.as_view(), name='account_login'),
   path("account/signup/", MySignupView.as_view(), name="account_signup"),
   path("account/password/reset/", MyPasswordResetView.as_view(), name="account_reset_password"),
]

urlpatterns += [
   path("account/", include("allauth.account.urls")),
   path('setting/', include('apps.user.setting.urls'))
]

# if settings.MFA_ENABLED:
#    urlpatterns += [path("setting/2fa/", include("allauth.mfa.urls"))]
if settings.SOCIALACCOUNT_ENABLED:
   urlpatterns += [
      path("social/", include("allauth.socialaccount.urls")),
      path("account/", include(build_provider_urlpatterns()))
   ]