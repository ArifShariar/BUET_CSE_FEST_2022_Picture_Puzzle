from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('leaderboard', view_leaderboard_page, name='leaderboard'),
    path('admin_leaderboard', view_admin_leaderboard_page, name='admin_leaderboard'),
    path('puzzle/<int:pk>/', load_next_puzzle, name='puzzle'),
    path('hackerman', hack, name='hackerman'),
    path('banned', banned, name='banned'),
]
