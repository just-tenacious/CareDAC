from django.utils import timezone
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect, render
from django.conf import settings
from ..models import OTPVerification

# ------------------ HELPER FUNCTIONS ------------------

def send_otp_email(email, otp, purpose):
    """Send an OTP email."""
    subject = f"Your CareDAC OTP for {purpose.capitalize()}"
    message = f"Your OTP is {otp}. It will expire in 5 minutes."
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@caredac.com')

    try:
        send_mail(subject, message, from_email, [email], fail_silently=False)
        print(f"[DEBUG] OTP sent to {email}: {otp}")
    except Exception as e:
        print(f"[ERROR] Could not send OTP email: {e}")


# ------------------ VERIFY OTP ------------------

def verify_otp(request):
    """
    Verify OTP for login, register, or forgot password.
    """
    source = request.GET.get('source', '')
    context = {'active_nav': '', 'source': source}

    if request.method == "POST":
        entered_otp = ''.join([
            request.POST.get('otp1', ''),
            request.POST.get('otp2', ''),
            request.POST.get('otp3', ''),
            request.POST.get('otp4', '')
        ])
        email = request.session.get('otp_email')

        if not email:
            messages.error(request, "Session expired. Please start again.")
            return redirect(f'/{source}/')

        try:
            otp_record = OTPVerification.objects.filter(
                email=email, purpose=source, is_verified=False
            ).latest('created_at')
        except OTPVerification.DoesNotExist:
            messages.error(request, "No OTP record found. Please request a new one.")
            return redirect(f'/resend-otp/?source={source}')

        if timezone.now() > otp_record.expires_at:
            messages.error(request, "OTP expired. Please request a new one.")
            return redirect(f'/resend-otp/?source={source}')

        if otp_record.otp == entered_otp:
            otp_record.is_verified = True
            otp_record.save()
            messages.success(request, "OTP verified successfully!")

            if source == "register":
                return redirect('/registered-for/')
            elif source == "login":
                return redirect('/home/')
            elif source == "forgot_password":
                return redirect('/reset-password/')
            else:
                return redirect('/home/')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'home/otp.html', context)


# ------------------ RESEND OTP ------------------

def resend_otp(request):
    """
    Generate and resend a new OTP.
    """
    source = request.GET.get('source', '')
    email = request.session.get('otp_email')

    if not email:
        messages.error(request, "Session expired. Please start again.")
        return redirect(f'/{source}/')

    # Create and send a new OTP
    otp_record = OTPVerification.create_otp(email=email, purpose=source)
    send_otp_email(email, otp_record.otp, purpose=source)

    messages.success(request, f"A new OTP has been sent to {email}.")
    return redirect(f'/otp/?source={source}')
