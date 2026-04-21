from apps.user.utils.pathresolver import getname_reversepath
from django.urls import reverse_lazy

from django.shortcuts import redirect, render
from allauth.account.views import LoginView, PasswordResetFromKeyView, SignupView, PasswordResetView, login_not_required, method_decorator
from django.urls import reverse

from django_htmx.http import retarget
from apps.user.forms import MyResetPasswordKeyForm, MyLoginForm, MyResetPasswordForm, MySignupForm

from allauth import app_settings as allauth_app_settings
from allauth.account import app_settings
from django.contrib.sites.shortcuts import get_current_site

def authenticated_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.session.get(request.user.username, 'guest'):
                return view_func(request, *args, **kwargs)
            else:
                return redirect('/access_denied/')  # Custom message
        else:
            if request.method == 'POST':
                response = render(request, "users/requiredLogin.html")
            else:
                response = redirect("user:login")
            return retarget(response, "#login")
    return _wrapped_view

class MyLoginView(LoginView):
    template_name = 'account/login.html'
    form_class = MyLoginForm

    def get_context_data(self, **kwargs):

        passkey_login_enabled = False
        if allauth_app_settings.MFA_ENABLED:
            from allauth.mfa import app_settings as mfa_settings

            passkey_login_enabled = mfa_settings.PASSKEY_LOGIN_ENABLED
        ret = super(LoginView, self).get_context_data(**kwargs)
        signup_url = None
        if not allauth_app_settings.SOCIALACCOUNT_ONLY:
            signup_url = self.passthrough_next_url(getname_reversepath(self.request,"account_signup"))
        site = get_current_site(self.request)

        ret.update(
            {
                "signup_url": signup_url,
                "site": site,
                "SOCIALACCOUNT_ENABLED": allauth_app_settings.SOCIALACCOUNT_ENABLED,
                "SOCIALACCOUNT_ONLY": allauth_app_settings.SOCIALACCOUNT_ONLY,
                "LOGIN_BY_CODE_ENABLED": app_settings.LOGIN_BY_CODE_ENABLED,
                "PASSKEY_LOGIN_ENABLED": passkey_login_enabled,
            }
        )
        if app_settings.LOGIN_BY_CODE_ENABLED:
            request_login_code_url = self.passthrough_next_url(
                reverse("account_request_login_code")
            )
            ret["request_login_code_url"] = request_login_code_url
        return ret

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
class MySignupView(SignupView):
    template_name = 'account/signup.html'
    form_class = MySignupForm
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ret = super(SignupView, self).get_context_data(**kwargs)
        self.login_url = self.passthrough_next_url(getname_reversepath(self.request, "account_login"))
        self.signup_url = self.passthrough_next_url(getname_reversepath(self.request, "account_signup"))

        passkey_signup_enabled = False
        if allauth_app_settings.MFA_ENABLED:
            from allauth.mfa import app_settings as mfa_settings

            passkey_signup_enabled = mfa_settings.PASSKEY_SIGNUP_ENABLED
        form = ret["form"]
        email = self.request.session.get("account_verified_email")
        if email:
            email_keys = ["email"]
            if "email2" in app_settings.SIGNUP_FIELDS:
                email_keys.append("email2")
            for email_key in email_keys:
                form.fields[email_key].initial = email
        login_url = self.passthrough_next_url(getname_reversepath(self.request, "account_login"))
        signup_url = self.passthrough_next_url(getname_reversepath(self.request, "account_signup"))
        signup_by_passkey_url = None
        if passkey_signup_enabled:
            signup_by_passkey_url = self.passthrough_next_url(
                reverse("account_signup_by_passkey")
            )
        site = get_current_site(self.request)
        ret.update(
            {
                "login_url": login_url,
                "signup_url": signup_url,
                "signup_by_passkey_url": signup_by_passkey_url,
                "site": site,
                "SOCIALACCOUNT_ENABLED": allauth_app_settings.SOCIALACCOUNT_ENABLED,
                "SOCIALACCOUNT_ONLY": allauth_app_settings.SOCIALACCOUNT_ONLY,
                "PASSKEY_SIGNUP_ENABLED": passkey_signup_enabled,
            }
        )
        return ret
    
@method_decorator(login_not_required, name="dispatch")
class MyPasswordResetView(PasswordResetView):    
    form_class = MyResetPasswordForm
    success_url = reverse_lazy("user:account_reset_password_done")
    
    def get_context_data(self, **kwargs):
        ret = super(PasswordResetView, self).get_context_data(**kwargs)
        self.login_url = self.passthrough_next_url(getname_reversepath(self.request, "account_login"))
        return ret
    
    def get_success_url(self):
        if not app_settings.PASSWORD_RESET_BY_CODE_ENABLED:
            return super().get_success_url()
        return self.passthrough_next_url(getname_reversepath(self.request, "account_confirm_password_reset_code"))




    
