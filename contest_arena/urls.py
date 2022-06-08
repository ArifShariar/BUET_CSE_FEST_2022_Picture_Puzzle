from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('rank_list', view_rank_list_page, name='rank_list'),
]
