from allauth.account.forms import LoginForm, ResetPasswordForm, ResetPasswordKeyForm, SignupForm, get_adapter, setup_user_email
from allauth.account.internal import flows
from django.contrib.auth import get_user_model, login as auth_login
from django.core.mail import send_mail
from datetime import timezone
from django import forms
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from apps.user.auth import flow_fix
from core import settings


User = get_user_model()

class MySignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = ""
        self.fields["password1"].label = ""
        self.fields["password2"].label = ""
        self.fields['password1'].help_text = ''

    def save(self, request):
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get("email")
        if self.account_already_exists:
            raise ValueError(email)

        user = super(MySignupForm, self).save(request)
        user.custom_set_password(password, f'{request.resolver_match.namespace}')
        
        return user

    def has_exists_email(self, email):
        return User.objects.filter(email__iexact=email).exists()

class MyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["login"].label = ""
        self.fields["password"].label = ""

    def clean(self):
        data = super().clean()
        if 'login' not in data:
            raise forms.ValidationError("Custom field is required.")
        return data

    def login(self, request, *args, **kwargs):
        password = self.cleaned_data.get('password')

        response = super().login(request, *args, **kwargs)
        user = self.user
    
        user.custom_check_password(password, f'{request.resolver_match.namespace}')
        auth_login(request, user)
        
        return response

    def save(self, request):
        user = super().save(request)

        user.profile.last_login_custom = timezone.now()
        user.profile.save()
        return user
    
class MyResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = ""
        
    def save(self, request, **kwargs):
        default_token_generator = PasswordResetTokenGenerator()

        self.email = self.cleaned_data["email"]
        if settings.PASSWORD_RESET_BY_CODE_ENABLED:
            flows.password_reset_by_code.PasswordResetVerificationProcess.initiate(
                request=request,
                user=(self.users[0] if self.users else None),
                email= self.email,
            )
        else:
            token_generator = kwargs.get("token_generator", default_token_generator)
            flow_fix.request_password_reset(
                request, self.email, self.users, token_generator
            )
        return super().save(request, **kwargs)

class MyResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = ""
        self.fields["password2"].label = ""
        self.fields['password1'].help_text = ''
