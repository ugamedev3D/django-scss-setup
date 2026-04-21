from django.urls import path
from apps.user.setting.views import *

urlpatterns = [
    path('', Setting_View, name='setting'),
    path('mfa/', MFA_View, name='mfa'),

    path('theme-mode/', Theme_Mode_View, name='theme-mode'),
    path('profile-edit/', Profile_Edit_View, name='profile-edit'),
    path('payment-setting/', Payment_Setting_View, name='payment-setting'),
    path('terms-and-conditions/', Terms_And_Conditions_View, name='terms-and-conditions'),
]
