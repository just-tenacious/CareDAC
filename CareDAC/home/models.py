from django.db import models
from datetime import datetime, timedelta , date
import random

# ============================================================
# 🧑‍💼 USER-RELATED MODELS
# ============================================================

# ------------------ Table 1 ------------------
class UserMaster(models.Model):
    uid = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'user_master'


# ------------------ Table 2 ------------------
class UserMemberDetail(models.Model):
    member_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    relation = models.CharField(max_length=50)
    uid = models.ForeignKey(UserMaster, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_member_detail'


# ------------------ Table 3 ------------------
class UserDetail(models.Model):
    user_id = models.AutoField(primary_key=True)
    emergency_contact = models.CharField(max_length=255)
    user_condition = models.TextField()
    user_needs = models.TextField()
    user_services = models.TextField()
    uid = models.ForeignKey(UserMaster, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_detail'


# ------------------ Table 4 ------------------
class UserPaymentDetail(models.Model):
    payment_id = models.AutoField(primary_key=True)
    card_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=20)
    expiry_date = models.CharField(max_length=10)
    cvv = models.CharField(max_length=5)
    uid = models.ForeignKey(UserMaster, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_payment_detail'


# ============================================================
# 🧾 SERVICE-RELATED MODELS
# ============================================================

# ------------------ Table 5 ------------------
class ServicesNeeded(models.Model):
    service_id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(UserMaster, on_delete=models.CASCADE)
    member_id = models.ForeignKey(UserMemberDetail, on_delete=models.CASCADE, blank=True, null=True)
    help = models.TextField()
    services = models.TextField()

    class Meta:
        db_table = 'services_needed'


# ============================================================
# 👩‍⚕️ CAREGIVER-RELATED MODELS
# ============================================================

# ------------------ Table 6 ------------------
class CaregiverMaster(models.Model):
    caregiver_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    dob = models.DateField()
    year_of_joining = models.IntegerField()
    gender = models.CharField(max_length=10)
    desc = models.TextField()
    language = models.CharField(max_length=255)
    start_hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    end_hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    time_sitter = models.CharField(max_length=255)
    background = models.TextField()
    check_status = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='caregiver_photos/', blank=True, null=True)

    class Meta:
        db_table = 'caregiver_master'
    
    @property
    def age(self):
        today = date.today()
        return (
            today.year
            - self.dob.year
            - ((today.month, today.day) < (self.dob.month, self.dob.day))
        )

    @property
    def years_of_experience(self):
        current_year = date.today().year
        return current_year - self.year_of_joining


# ------------------ Table 7 ------------------
class CaregiverDetail(models.Model):
    cid = models.AutoField(primary_key=True)
    highlights = models.TextField()
    functionality = models.TextField()
    caregiver_id = models.ForeignKey(CaregiverMaster, on_delete=models.CASCADE,db_column='caregiver_id',null=True, blank=True)

    class Meta:
        db_table = 'caregiver_detail'


# ------------------ Table 8 ------------------
class CaregiverReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    reviewer_name = models.CharField(max_length=255)
    comment = models.TextField()
    rating = models.IntegerField()
    caregiver_id = models.ForeignKey(CaregiverMaster, on_delete=models.CASCADE,db_column='caregiver_id',null=True, blank=True)

    class Meta:
        db_table = 'caregiver_review'


# ============================================================
# 🔐 OTP VERIFICATION SYSTEM
# ============================================================

class OTPVerification(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    purpose = models.CharField(max_length=20, choices=[
        ('register', 'Register'),
        ('login', 'Login'),
        ('forgot_password', 'Forgot Password'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'otp_verification'

    def __str__(self):
        return f"{self.email} - {self.purpose} - {self.otp}"

    @staticmethod
    def generate_otp():
        """Generate a random 4-digit OTP"""
        return str(random.randint(1000, 9999))

    @classmethod
    def create_otp(cls, email, purpose):
        """Create and save OTP"""
        otp = cls.generate_otp()
        expires_at = datetime.now() + timedelta(minutes=5)
        return cls.objects.create(
            email=email,
            otp=otp,
            purpose=purpose,
            expires_at=expires_at
        )
