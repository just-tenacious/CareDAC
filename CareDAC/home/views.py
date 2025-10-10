from django.shortcuts import render

# Home & Main Pages
def home_view(request):
    return render(request, 'home/home.html', {'active_nav': 'home'})

def login_view(request):
    return render(request, 'home/login.html', {'active_nav': ''})

def forgot_password(request):
    return render(request, 'home/forgot_password.html', {'active_nav': ''})

def register_view(request):
    return render(request, 'home/register.html', {'active_nav': ''})

def otp_view(request):
    return render(request, 'home/otp.html', {'active_nav': ''})

def reset_password(request):
    return render(request, 'home/reset_password.html', {'active_nav': ''})

# Registration Flow
def registered_for(request):
    return render(request, 'home/registeredFor.html', {'active_nav': ''})

def register_info(request):
    return render(request, 'home/registerInfo.html', {'active_nav': ''})

def service_needed(request):
    return render(request, 'home/serviceNeeded.html', {'active_nav': ''})

# Member & Patient Details
def member_detail(request):
    return render(request, 'home/memberDetail.html', {'active_nav': ''})

def patient_detail(request):
    return render(request, 'home/patient_detail.html', {'active_nav': ''})

# Appointments & Payments
def appointment(request):
    return render(request, 'home/appointment.html', {'active_nav': 'appointment'})

def payment(request):
    return render(request, 'home/payments.html', {'active_nav': 'payment'})

# Caregivers List & Profile
def caregivers_view(request):
    return render(request, 'home/list.html', {'range': range(20), 'active_nav': 'home'})

def caregiver_profile_view(request):
    # Currently static; later you can pass dynamic caregiver info
    return render(request, 'home/caregiver_profile.html', {'active_nav': 'home'})

def booking_history(request):
    return render(request,'home/booking_history.html',{'active_nav':'appointment'})

def user_profile(request):
    return render(request,'home/user_profile.html')