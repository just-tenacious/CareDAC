# home/models.py

from django.db import models

class UserMaster(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    full_name = models.CharField(max_length=255)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Other')
    email = models.EmailField(unique=True)
    phno = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    address_1 = models.CharField(max_length=255, blank=True, null=True)
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    pin_code = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'user_master'
