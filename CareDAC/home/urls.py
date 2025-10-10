from django.urls import path
from .views import (
    home_view, login_view, forgot_password, register_view,
    otp_view, reset_password, registered_for, register_info,
    service_needed, member_detail, patient_detail, appointment,
    payment, caregivers_view, caregiver_profile_view,booking_history,
    user_profile
)

urlpatterns = [
    path('', login_view, name='login'), 
    path('home/', home_view, name='home'),  
    path('login/', login_view, name='login'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('otp/', otp_view, name='otp'),
    path('reset-password/', reset_password, name='reset_password'),
    path('register/', register_view, name='register'),
    path('registered-for/', registered_for, name='registered_for'),
    path('register-info/', register_info, name='register_info'),
    path('service-needed/', service_needed, name='service_needed'),
    path('member-detail/', member_detail, name='member_detail'),
    path('patient-detail/', patient_detail, name='patient_detail'),
    path('appointment/', appointment, name='appointment'),
    path('payment/', payment, name='payment'),
    path('caregivers/', caregivers_view, name='caregivers'),
    path('caregiver-profile/', caregiver_profile_view, name='caregiver_profile'),
    path('booking-history/',booking_history,name='booking_history'),
    path('user-profile',user_profile,name="user_profile"),
]
