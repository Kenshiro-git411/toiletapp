from django.urls import path
from . import views

app_name = 'toilet'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('search_toilet/', views.search_toilet, name='search_toilet'),
    path('suggest_station/', views.suggest_station, name='suggest_station'),
    path('suggest_toilet/', views.suggest_toilet, name='suggest_toilet'),
]