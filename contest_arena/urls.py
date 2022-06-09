from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('rank_list', view_rank_list_page, name='rank_list'),
    path('puzzle/<int:pk>/', load_next_puzzle, name='puzzle'),
]
