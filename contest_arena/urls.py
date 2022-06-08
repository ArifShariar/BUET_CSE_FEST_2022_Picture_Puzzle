from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='index'),
    path('ranking', view_ranking_page, name='ranking'),
]
