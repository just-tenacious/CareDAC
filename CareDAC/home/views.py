from django.shortcuts import render, redirect
from . import service_loader

# ------------------ HOME ------------------
def home_view(request):
    """
    Home page view.
    Fetch all caregivers and pass them to the template.
    """
    caregivers = service_loader.caregiver.get_all_caregivers()
    return render(request, 'home/home.html', {
        'active_nav': 'home',
        'caregivers': caregivers
    })

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
# def caregivers_view(request):
#     """
#     Fetch all caregivers from the service and render the list template.
#     """
#     caregivers = service_loader.caregiver.get_all_caregivers()
#     return render(request, 'home/list.html', {
#         'caregivers': caregivers,
#         'active_nav': 'home'
#     })

def caregivers_view(request):
    caregivers = service_loader.caregiver.get_all_caregivers()

    for caregiver in caregivers:
        avg = service_loader.caregiver.get_average_rating_for_caregiver(caregiver.caregiver_id)
        caregiver.average_rating = avg if avg is not None else 0

    return render(request, 'home/list.html', {
        'caregivers': caregivers,
        'active_nav': 'home'
    })


def caregiver_profile_view(request, caregiver_id=None):
    """
    Fetch a single caregiver by ID for profile view.
    Includes reviews, average rating, highlights, and functionality.
    """
    caregiver = None
    dynamic_fields = []
    reviews = []
    average_rating = None
    highlights = []
    functionality = []

    if caregiver_id:
        # Fetch caregiver master record
        caregiver = service_loader.caregiver.get_caregiver_by_id(caregiver_id)

        # Fetch dynamic fields (optional)
        excluded = [
            'caregiver_id', 'profile_photo', 'full_name', 'dob', 'gender', 
            'language', 'start_hourly_rate', 'end_hourly_rate', 'check_status',
            'year_of_joining', 'desc', 'background', 'time_sitter'
        ]
        dynamic_fields = [
            (f.verbose_name.title(), getattr(caregiver, f.name))
            for f in caregiver.__class__._meta.get_fields()
            if f.concrete and f.name not in excluded
        ]

        # Fetch reviews and average rating
        reviews = service_loader.caregiver.get_reviews_for_caregiver(caregiver_id)
        average_rating = service_loader.caregiver.get_average_rating_for_caregiver(caregiver_id)

        # Fetch highlights and functionality from caregiver_detail
        details = service_loader.caregiver.get_caregiver_dynamic_details(caregiver_id)
        highlights = details.get('highlights', [])
        functionality = details.get('functionality', [])

    return render(request, 'home/caregiver_profile.html', {
        'caregiver': caregiver,
        'dynamic_fields': dynamic_fields,
        'reviews': reviews,
        'average_rating': average_rating,
        'highlights': highlights,
        'functionality': functionality,
        'active_nav': 'home'
    })


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
