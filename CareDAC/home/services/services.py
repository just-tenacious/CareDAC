from .models import UserMaster
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
import random
import requests

def generate_otp(length=4):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def send_otp_sms(phone_number, otp):
    url = "https://www.fast2sms.com/dev/bulkV2"
    headers = {
        'authorization': settings.FAST2SMS_API_KEY,
        'Content-Type': "application/json"
    }
    params = {
        'variables_values': otp,
        'route': 'v3',
        'numbers': phone_number,
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    if data.get('return'):
        return True
    else:
        raise Exception(data.get('message', 'Failed to send SMS via Fast2SMS'))

def send_otp_email(email, otp):
    subject = "Your CareDAC OTP Code"
    message = f"Your OTP code is {otp}. Please do not share it with anyone."
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

def register_new_user(post_data, request):
    fullname = post_data.get('fullname')
    dob = post_data.get('dob')
    gender = post_data.get('gender')
    email = post_data.get('email')
    mobile = post_data.get('mobile')
    password = post_data.get('password')
    confirm_password = post_data.get('confirm_password')

    if password != confirm_password:
        return False, "Passwords do not match."

    if UserMaster.objects.filter(email=email).exists():
        return False, "Email is already registered."

    otp = generate_otp()

    try:
        mobile_10 = mobile[-10:]
        send_otp_sms(mobile_10, otp)
    except Exception:
        send_otp_email(email, otp)

    request.session['otp'] = otp
    request.session['user_data'] = {
        'full_name': fullname,
        'dob': dob,
        'gender': gender,
        'email': email,
        'phone': mobile,
        'password': make_password(password),
    }
    request.session['flow_type'] = 'register'
    request.session['user_email'] = email

    return True, "OTP sent. Please verify."

def authenticate_user_and_send_otp(email, password, request):
    try:
        user = UserMaster.objects.get(email=email)
    except UserMaster.DoesNotExist:
        return False, "Invalid email or password."

    if not check_password(password, user.password):
        return False, "Invalid email or password."

    otp = generate_otp()

    try:
        mobile_10 = user.phno[-10:]
        send_otp_sms(mobile_10, otp)
    except Exception:
        send_otp_email(user.email, otp)

    request.session['otp'] = otp
    request.session['user_email'] = email
    request.session['flow_type'] = 'login'

    return True, "OTP sent to your registered contact."

def verify_otp(entered_otp, request):
    session_otp = request.session.get('otp')
    flow_type = request.session.get('flow_type')
    user_data = request.session.get('user_data')
    user_email = request.session.get('user_email')

    if not session_otp or not flow_type:
        return False, "Session expired. Please try again."

    if entered_otp != session_otp:
        return False, "Invalid OTP. Please try again."

    try:
        if flow_type == 'register':
            UserMaster.objects.create(**user_data)
            for key in ['otp', 'user_data', 'flow_type']:
                request.session.pop(key, None)
            return True, "Registration successful!"

        elif flow_type == 'forgot_password':
            request.session['otp_verified'] = True
            request.session.pop('otp', None)
            return True, "OTP verified. You may now reset your password."

        elif flow_type == 'login':
            request.session['logged_in_user'] = user_email
            for key in ['otp', 'flow_type']:
                request.session.pop(key, None)
            return True, "Login successful!"

        else:
            return False, "Unknown verification flow."

    except Exception as e:
        return False, f"Error verifying OTP: {str(e)}"

def initiate_forgot_password(email, request):
    try:
        user = UserMaster.objects.get(email=email)
        otp = generate_otp()

        try:
            mobile_10 = user.phno[-10:]
            send_otp_sms(mobile_10, otp)
        except Exception:
            send_otp_email(user.email, otp)

        request.session['otp'] = otp
        request.session['user_email'] = email
        request.session['flow_type'] = 'forgot_password'

        return True, "OTP sent. Please check your phone or email."

    except UserMaster.DoesNotExist:
        return False, "No account found with that email."

    except Exception as e:
        return False, f"Failed to send OTP: {str(e)}"

def reset_user_password(new_password, request):
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

def resend_otp(email, flow_type):
    try:
        user = UserMaster.objects.get(email=email)
        otp = generate_otp()

        try:
            mobile_10 = user.phno[-10:]
            send_otp_sms(mobile_10, otp)
        except Exception:
            send_otp_email(user.email, otp)

        return True, otp

    except UserMaster.DoesNotExist:
        return False, "User not found."

    except Exception as e:
        return False, f"Failed to resend OTP: {str(e)}"

def update_patient_details(email, form_data):
    required_fields = {
        'Address Line 1': form_data.get('address_1', '').strip(),
        'Country': form_data.get('country', '').strip(),
        'State': form_data.get('state', '').strip(),
        'City': form_data.get('city', '').strip(),
        'Pin Code': form_data.get('pin_code', '').strip(),
    }
    missing_fields = [name for name, value in required_fields.items() if not value]
    if missing_fields:
        return False, f"Please fill in all required fields: {', '.join(missing_fields)}."

    try:
        user = UserMaster.objects.get(email=email)
        user.address_1 = form_data.get('address_1')
        user.address_2 = form_data.get('address_2')
        user.country = form_data.get('country')
        user.state = form_data.get('state')
        user.city = form_data.get('city')
        user.pin_code = form_data.get('pin_code')
        user.save()
        return True, "Member details updated successfully!"
    except UserMaster.DoesNotExist:
        return False, "User not found."
    except Exception as e:
        return False, f"Error updating member details: {str(e)}"

from .models import UserMaster, UserMemberDetail
from datetime import datetime

def save_member_detail(post_data, user_email):
    try:
        user = UserMaster.objects.get(email=user_email)

        member_type = post_data.get('type', '').strip()
        full_name = post_data.get('full_name', '').strip()
        dob_str = post_data.get('dob', '').strip()
        phone = post_data.get('phone', '').strip()
        gender = post_data.get('gender', '').strip()
        address_type = post_data.get('address_type', '').strip()
        address_1 = post_data.get('address_1', '').strip()
        address_2 = post_data.get('address_2', '').strip()
        country = post_data.get('country', '').strip()
        state = post_data.get('state', '').strip()
        city = post_data.get('city', '').strip()
        pin_code = post_data.get('pin_code', '').strip()

        # Validate required fields
        required_fields = {
            "Full Name": full_name,
            "Date of Birth": dob_str,
            "Phone": phone,
            "Gender": gender,
            "Member Type": member_type,
        }
        missing_fields = [name for name, val in required_fields.items() if not val]
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"

        try:
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        except ValueError:
            return False, "Invalid date format for DOB. Use YYYY-MM-DD."

        member_detail = UserMemberDetail.objects.create(
            user=user,
            type=member_type,
            full_name=full_name,
            dob=dob,
            phone=phone,
            gender=gender,
            address_type=address_type or 'Manual Entry',
            address_1=address_1 or None,
            address_2=address_2 or None,
            country=country or None,
            state=state or None,
            city=city or None,
            pin_code=pin_code or None,
        )

        return True, "Member details saved successfully."

    except Exception as e:
        return False, f"Failed to save member details: {str(e)}"
