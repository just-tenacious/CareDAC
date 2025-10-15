from django.shortcuts import render, redirect
from django.contrib import messages
from .services import (
    register_new_user,
    verify_otp,
    initiate_forgot_password,
)

# ------------------- Home & Auth Pages -------------------

def home_view(request):
    """Render the home page."""
    return render(request, 'home/home.html', {'active_nav': 'home'})

def login_view(request):
    """Render the login page."""
    return render(request, 'home/login.html', {'active_nav': ''})

def forgot_password(request):
    """Handle forgot password form submission."""
    if request.method == 'POST':
        email = request.POST.get('email')
        success, msg = initiate_forgot_password(email, request)
        if success:
            request.session['flow_type'] = 'forgot_password'
            messages.success(request, msg)
            return redirect('otp')
        else:
            messages.error(request, msg)
    return render(request, 'home/forgot_password.html', {'active_nav': ''})

def register_view(request):
    """Handle user registration form submission."""
    if request.method == 'POST':
        success, msg = register_new_user(request.POST, request)
        if success:
            request.session['flow_type'] = 'register'
            messages.success(request, msg)
            return redirect('otp')
        else:
            messages.error(request, msg)
            return render(request, 'home/register.html', {
                'form_data': request.POST
            })
    return render(request, 'home/register.html')

# ------------------- OTP Verification -------------------

def otp_view(request):
    """Render OTP input page with current flow type."""
    flow_type = request.session.get('flow_type', 'register')
    return render(request, 'home/otp.html', {
        'flow_type': flow_type,
        'active_nav': ''
    })

def verify_otp_view(request):
    """Verify entered OTP and proceed accordingly."""
    if request.method == 'POST':
        otp = ''.join([
            request.POST.get('otp1', ''),
            request.POST.get('otp2', ''),
            request.POST.get('otp3', ''),
            request.POST.get('otp4', ''),
        ])
        success, msg = verify_otp(otp, request)
        flow_type = request.session.get('flow_type', 'register')

        if success:
            messages.success(request, msg)
            if flow_type == 'register':
                return redirect('login')
            elif flow_type == 'forgot_password':
                return redirect('reset_password')
            elif flow_type == 'login':
                return redirect('home')
        else:
            messages.error(request, msg)
            return redirect('otp')

    return redirect('otp')

# ------------------- Password Reset Page -------------------

def reset_password(request):
    """Render password reset page."""
    return render(request, 'home/reset_password.html', {'active_nav': ''})

# ------------------- Registration Flow Pages -------------------

def registered_for(request):
    """Render registered_for page."""
    return render(request, 'home/registeredFor.html', {'active_nav': ''})

def register_info(request):
    """Render register_info page."""
    return render(request, 'home/registerInfo.html', {'active_nav': ''})

def service_needed(request):
    """Render service_needed page."""
    return render(request, 'home/serviceNeeded.html', {'active_nav': ''})

# ------------------- Member & Patient Details -------------------

def member_detail(request):
    """Render member_detail page."""
    return render(request, 'home/memberDetail.html', {'active_nav': ''})

def patient_detail(request):
    """Render patient_detail page."""
    return render(request, 'home/patient_detail.html', {'active_nav': ''})

# ------------------- Appointments & Payments -------------------

def appointment(request):
    """Render appointment page."""
    return render(request, 'home/appointment.html', {'active_nav': 'appointment'})

def payment(request):
    """Render payments page."""
    return render(request, 'home/payments.html', {'active_nav': 'payment'})

# ------------------- Caregivers -------------------

def caregivers_view(request):
    """Render list of caregivers."""
    return render(request, 'home/list.html', {
        'range': range(20),
        'active_nav': 'home'
    })

def caregiver_profile_view(request):
    """Render caregiver profile page."""
    return render(request, 'home/caregiver_profile.html', {'active_nav': 'home'})

# ------------------- User Profile & History -------------------

def booking_history(request):
    """Render booking history page."""
    return render(request, 'home/booking_history.html', {'active_nav': 'appointment'})

def user_profile(request):
    """Render user profile page."""
    return render(request, 'home/user_profile.html')
