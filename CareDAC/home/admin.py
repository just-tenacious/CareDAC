from django.contrib import admin
from .models import (
    UserMaster,
    UserMemberDetail,
    UserDetail,
    UserPaymentDetail,
    ServicesNeeded,
    CaregiverMaster,
    CaregiverDetail,
    CaregiverReview,
    OTPVerification
)

# Option 1: Register them manually
admin.site.register(UserMaster)
admin.site.register(UserMemberDetail)
admin.site.register(UserDetail)
admin.site.register(UserPaymentDetail)
admin.site.register(ServicesNeeded)
admin.site.register(CaregiverMaster)
admin.site.register(CaregiverDetail)
admin.site.register(CaregiverReview)
admin.site.register(OTPVerification)
