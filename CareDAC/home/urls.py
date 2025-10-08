# from django.urls import path
# from .views import home_view,login_view,forgot_password,register_view

# urlpatterns = [
#     path('', home_view, name='home'),
#     path('login',login_view,name='login'),
#     path('forgot-password',forgot_password,name='forgot_password'),
#     path('register',register_view,name='register')
# ]

from django.urls import path
from .views import home_view, login_view, forgot_password, register_view , otp_view,reset_password

urlpatterns = [
    path('', login_view, name='login'), 
    path('home/', home_view, name='home'),  
    path('login/', login_view, name='login'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('otp',otp_view,name='otp'),
    path('reset-password',reset_password,name='reset_password'),
    path('register/', register_view, name='register'),
]
