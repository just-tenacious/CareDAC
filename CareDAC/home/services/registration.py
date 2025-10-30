from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.db import IntegrityError
from datetime import datetime
from ..models import UserMaster, OTPVerification
from .otp_service import send_otp_email
import hashlib

# ------------------ UTILS ------------------
def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

# ------------------ REGISTRATION ------------------
def register_user(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        phone = request.POST.get('mobile')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        gender = request.POST.get('gender')

        # Basic validation
        if not all([fullname, dob, email, phone, password, confirm_password, gender]):
            messages.error(request, "Please fill all required fields.")
            return render(request, 'home/register.html', {'active_nav': ''})

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'home/register.html', {'active_nav': ''})

        if UserMaster.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'home/register.html', {'active_nav': ''})

        if UserMaster.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already registered.")
            return render(request, 'home/register.html', {'active_nav': ''})

        try:
            user = UserMaster.objects.create(
                full_name=fullname,
                dob=datetime.strptime(dob, "%Y-%m-%d").date(),
                gender=gender,
                email=email,
                phone=phone,
                password=hash_password(password),
                address1="", address2="", city="", state="", country="", pincode=""
            )

            # Generate OTP and send email
            otp_record = OTPVerification.create_otp(email=email, purpose='register')
            request.session['otp_email'] = email
            send_otp_email(email, otp_record.otp, 'register')

            messages.success(request, "Registration successful! Please verify your email with the OTP sent.")
            return redirect('/otp/?source=register')

        except IntegrityError:
            messages.error(request, "A user with this email or phone already exists.")
        except Exception as e:
            messages.error(request, f"Unexpected error: {str(e)}")

    return render(request, 'home/register.html', {'active_nav': ''})

# ------------------ LOGIN ------------------
def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Please provide both email and password.")
            return render(request, 'home/login.html', {'active_nav': ''})

        user = UserMaster.objects.filter(email=email).first()
        if not user or user.password != hash_password(password):
            messages.error(request, "Invalid email or password.")
            return render(request, 'home/login.html', {'active_nav': ''})

        otp_record = OTPVerification.create_otp(email=email, purpose='login')
        request.session['otp_email'] = email
        send_otp_email(email, otp_record.otp, 'login')

        messages.success(request, "OTP sent to your email for verification.")
        return redirect('/otp/?source=login')

    return render(request, 'home/login.html', {'active_nav': ''})

# ------------------ FORGOT PASSWORD ------------------
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if not email:
            messages.error(request, "Please provide your email.")
            return render(request, 'home/forgot_password.html', {'active_nav': ''})

        user = UserMaster.objects.filter(email=email).first()
        if not user:
            messages.error(request, "Email not registered.")
            return render(request, 'home/forgot_password.html', {'active_nav': ''})

        otp_record = OTPVerification.create_otp(email=email, purpose='forgot_password')
        request.session['otp_email'] = email
        send_otp_email(email, otp_record.otp, 'password reset')

        messages.success(request, "OTP sent to your email for password reset.")
        return redirect('/otp/?source=forgot_password')

    return render(request, 'home/forgot_password.html', {'active_nav': ''})

# ------------------ RESET PASSWORD ------------------
def reset_password(request):
    """
    Reset user password after OTP verification.
    """
    email = request.session.get('otp_email')
    if not email:
        messages.error(request, "Session expired. Please request a new password reset.")
        return redirect('/forgot-password/')

    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not password or not confirm_password:
            messages.error(request, "Please fill both password fields.")
            return render(request, 'home/reset_password.html', {'active_nav': ''})

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'home/reset_password.html', {'active_nav': ''})

        user = UserMaster.objects.filter(email=email).first()
        if not user:
            messages.error(request, "No user found with this email.")
            return redirect('/forgot-password/')

        user.password = hash_password(password)
        user.save()
        del request.session['otp_email']

        messages.success(request, "Password reset successful! You can now log in.")
        return redirect('/login/')

    return render(request, 'home/reset_password.html', {'active_nav': ''})

# ------------------ VERIFY OTP ------------------
def verify_otp(request):
    source = request.GET.get("source")
    email = request.session.get("otp_email")

    if request.method == "POST":
        otp_input = request.POST.get("otp") or "".join([
            request.POST.get(f"otp{i}", "") for i in range(1, 5)
        ])

        if not email or not otp_input:
            messages.error(request, "OTP or email missing.")
            return render(request, "home/otp.html", {'active_nav': '', 'source': source})

        otp_record = OTPVerification.objects.filter(email=email, purpose=source).order_by('-created_at').first()
        if not otp_record:
            messages.error(request, "OTP not found. Please resend.")
            return render(request, "home/otp.html", {'active_nav': '', 'source': source})

        if otp_record.expires_at < timezone.now():
            messages.error(request, "OTP expired. Please resend.")
            return render(request, "home/otp.html", {'active_nav': '', 'source': source})

        if otp_record.otp == otp_input:
            messages.success(request, "OTP verified successfully!")
            del request.session['otp_email']

            if source == "login":
                return redirect("/home/")
            elif source == "register":
                return redirect("/registered-for/")
            elif source == "forgot_password":
                return redirect("/reset-password/")
        else:
            messages.error(request, "Invalid OTP. Try again.")

    return render(request, "home/otp.html", {'active_nav': '', 'source': source})

# ------------------ RESEND OTP ------------------
def resend_otp(request):
    email = request.session.get('otp_email')
    source = request.GET.get('source', '')

    if email:
        otp_record = OTPVerification.create_otp(email=email, purpose=source)
        send_otp_email(email, otp_record.otp, source)
        messages.success(request, "New OTP sent successfully.")

    return redirect(f'/otp/?source={source}')
