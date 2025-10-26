from django.db import models

# Table 1
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

# Table 2
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

# Table 3
class UserDetail(models.Model):
    user_id = models.AutoField(primary_key=True)
    emergency_contact = models.CharField(max_length=255)
    user_condition = models.TextField()
    user_needs = models.TextField()
    user_services = models.TextField()
    uid = models.ForeignKey(UserMaster, on_delete=models.CASCADE)

# Table 4
class UserPaymentDetail(models.Model):
    payment_id = models.AutoField(primary_key=True)
    card_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=20)
    expiry_date = models.CharField(max_length=10)
    cvv = models.CharField(max_length=5)
    uid = models.ForeignKey(UserMaster, on_delete=models.CASCADE)

# Table 5
class ServicesNeeded(models.Model):
    service_id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(UserMaster, on_delete=models.CASCADE)
    member_id = models.ForeignKey(UserMemberDetail, on_delete=models.CASCADE, blank=True, null=True)
    help = models.TextField()
    services = models.TextField()

# Table 6
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

# Table 7
class CaregiverDetail(models.Model):
    cid = models.AutoField(primary_key=True)
    highlights = models.TextField()
    functionality = models.TextField()
    caregiver_id = models.ForeignKey(CaregiverMaster, on_delete=models.CASCADE)

# Table 8
class CaregiverReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    reviewer_name = models.CharField(max_length=255)
    comment = models.TextField()
    rating = models.IntegerField()
    cid = models.ForeignKey(CaregiverDetail, on_delete=models.CASCADE)
