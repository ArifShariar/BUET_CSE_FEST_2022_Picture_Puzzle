from django.urls import path
from .views import *

urlpatterns = [
    path('register', participant_register, name='register'),
    path('login', participant_login, name='login'),
    path('logout', participant_logout, name='logout'),
]
