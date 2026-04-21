from django.shortcuts import redirect, render

def Setting_View(request):
    return render(request, 'setting/setting.html')

def MFA_View(request):
    return redirect('user:mfa_index')

def Theme_Mode_View(request):
    return render(request, 'setting/theme-mode-setting.html')

def Profile_Edit_View(request):
    return render(request, 'setting/profile-edit.html')

def Payment_Setting_View(request):
    return render(request, 'setting/payment-setting.html')

def Terms_And_Conditions_View(request):
    return render(request, 'setting/terms&conditions.html')