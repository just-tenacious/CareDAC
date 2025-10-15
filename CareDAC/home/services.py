from .models import UserMaster
from django.core.mail import send_mail
from django.conf import settings
# from twilio.rest import Client  # Commented out since SMS is disabled
from django.contrib.auth.hashers import make_password
import random


def generate_otp(length=4):
    """Generate a numeric OTP of given length."""
    return ''.join(str(random.randint(0, 9)) for _ in range(length))


# def format_phone_number(phone_number):
#     """
#     Format the phone number to E.164 format for Twilio.
#     Assumes Indian numbers if no country code present.
#     """
#     phone_number = phone_number.strip()
#     if not phone_number.startswith('+'):
#         # Prepend country code +91 for India; adjust as needed
#         phone_number = '+91' + phone_number
#     return phone_number


# def send_otp_sms(phone_number, otp):
#     """Send OTP SMS using Twilio API."""
#     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#     formatted_phone = format_phone_number(phone_number)
#     message = client.messages.create(
#         body=f"Your CareDAC OTP is {otp}",
#         from_=settings.TWILIO_PHONE_NUMBER,
#         to=formatted_phone
#     )
#     return message.sid


def send_otp_email(email, otp):
    """Send OTP email."""
    subject = "Your CareDAC OTP Code"
    message = f"Your OTP code is {otp}. Please do not share it with anyone."
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])


def register_new_user(post_data, request):
    """Register user and send OTP via email only."""
    fullname = post_data.get('fullname')
    dob = post_data.get('dob')
    gender = post_data.get('gender')
    email = post_data.get('email')
    mobile = post_data.get('mobile')  # still collected but not used for SMS
    password = post_data.get('password')
    confirm_password = post_data.get('confirm_password')

    # Validate passwords match
    if password != confirm_password:
        return False, "Passwords do not match."

    # Check if email already exists
    if UserMaster.objects.filter(email=email).exists():
        return False, "Email is already registered."

    otp = generate_otp()

    try:
        # send_otp_sms(mobile, otp)  # Disabled SMS sending
        send_otp_email(email, otp)

        # Save OTP and user data in session for verification
        request.session['otp'] = otp
        request.session['user_data'] = {
            'full_name': fullname,
            'dob': dob,
            'gender': gender,
            'email': email,
            'phno': mobile,  # stored but SMS not sent
            'password': make_password(password),
        }
        request.session['flow_type'] = 'register'

        return True, "OTP sent to email. Please verify."

    except Exception as e:
        return False, f"Error during registration: {str(e)}"


def verify_otp(entered_otp, request):
    """Verify the OTP entered by the user."""
    session_otp = request.session.get('otp')
    flow_type = request.session.get('flow_type')
    user_data = request.session.get('user_data')

    if not session_otp or not flow_type:
        return False, "Session expired. Please try again."

    if entered_otp != session_otp:
        return False, "Invalid OTP. Please try again."

    try:
        if flow_type == 'register':
            # Create new user
            UserMaster.objects.create(**user_data)
            request.session.flush()
            return True, "Registration successful!"

        elif flow_type == 'forgot_password':
            # Mark OTP as verified for password reset
            request.session['otp_verified'] = True
            return True, "OTP verified. You may now reset your password."

        else:
            return False, "Unknown verification flow."

    except Exception as e:
        return False, f"Error verifying OTP: {str(e)}"


def initiate_forgot_password(email, request):
    """Start forgot password process by sending OTP to email only."""
    try:
        user = UserMaster.objects.get(email=email)
        otp = generate_otp()

        # send_otp_sms(user.phno, otp)  # Disabled SMS sending
        send_otp_email(user.email, otp)

        request.session['otp'] = otp
        request.session['user_email'] = email
        request.session['flow_type'] = 'forgot_password'

        return True, "OTP sent to your email."

    except UserMaster.DoesNotExist:
        return False, "No account found with that email."

    except Exception as e:
        return False, f"Failed to send OTP: {str(e)}"


def reset_user_password(new_password, request):
    """Reset the user's password after OTP verification."""
    if not request.session.get('otp_verified') or not request.session.get('user_email'):
        return False, "OTP not verified or session expired."

    try:
        email = request.session['user_email']
        user = UserMaster.objects.get(email=email)
        user.password = make_password(new_password)
        user.save()
        request.session.flush()

        return True, "Password reset successful."

    except Exception as e:
        return False, f"Error resetting password: {str(e)}"
