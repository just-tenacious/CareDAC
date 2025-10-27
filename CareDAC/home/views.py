from django.shortcuts import render, redirect
from . import service_loader

# ------------------ HOME ------------------
def home_view(request):
    return render(request, 'home/home.html', {'active_nav': 'home'})

# ------------------ LOGIN ------------------
def login_view(request):
    return service_loader.registration.login_user(request)

# ------------------ FORGOT PASSWORD ------------------
def forgot_password(request):
    return service_loader.registration.forgot_password(request)

# ------------------ REGISTER ------------------
def register_view(request):
    return service_loader.registration.register_user(request)

# ------------------ OTP ------------------
def otp_view(request):
    return service_loader.registration.verify_otp(request)

def resend_otp_view(request):
    return service_loader.registration.resend_otp(request)

# def reset_password(request):
#     return render(request, 'home/reset_password.html', {'active_nav': ''})

# ------------------ RESET PASSWORD ------------------
def reset_password_view(request):
    return service_loader.registration.reset_password(request)

# ------------------ REGISTRATION FLOW ------------------
def registered_for(request):
    return render(request, 'home/registeredFor.html', {'active_nav': ''})

def register_info(request):
    return render(request, 'home/registerInfo.html', {'active_nav': ''})

def service_needed(request):
    return render(request, 'home/serviceNeeded.html', {'active_nav': ''})

# ------------------ MEMBER & PATIENT DETAILS ------------------
def member_detail(request):
    return render(request, 'home/memberDetail.html', {'active_nav': ''})

def patient_detail(request):
    return render(request, 'home/patient_detail.html', {'active_nav': ''})

# ------------------ APPOINTMENTS & PAYMENTS ------------------
def appointment(request):
    return render(request, 'home/appointment.html', {'active_nav': 'appointment'})

def payment(request):
    return render(request, 'home/payments.html', {'active_nav': 'payment'})

# ------------------ CAREGIVERS ------------------
def caregivers_view(request):
    return render(request, 'home/list.html', {'range': range(20), 'active_nav': 'home'})

def caregiver_profile_view(request):
    return render(request, 'home/caregiver_profile.html', {'active_nav': 'home'})

# ------------------ BOOKING HISTORY & PROFILE ------------------
def booking_history(request):
    return render(request, 'home/booking_history.html', {'active_nav': 'appointment'})

def user_profile(request):
    return render(request, 'home/user_profile.html')

# ------------------ TEST ------------------
def test_services_import(request):
    result = service_loader.test_imports()
    from django.http import HttpResponse
    return HttpResponse(result)
