# home/models.py

from django.db import models

class UserMaster(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    full_name = models.CharField(max_length=255)
    dob = models.DateField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    phno = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)  
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.email})"
