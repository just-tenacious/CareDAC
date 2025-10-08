from django.shortcuts import render

def home_view(request):
    return render(request,'home/home.html')

def login_view(request):
    return render(request, 'home/login.html')

def forgot_password(request):
    return render(request, 'home/forgot_password.html')

def register_view(request):
    return render(request, 'home/register.html')

def otp_view(request):
    return render(request, 'home/otp.html')

def reset_password(request):
    return render(request, 'home/reset_password.html')

def registered_for(request):
    return render(request, 'home/registeredFor.html')

def register_info(request):
    return render(request, 'home/registerInfo.html')

def service_needed(request):
    return render(request, 'home/serviceNeeded.html')

def member_detail(request):
    return render(request, 'home/memberDetail.html')

def patient_detail(request):
    return render(request, 'home/patient_detail.html')