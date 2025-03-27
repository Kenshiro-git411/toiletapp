from django.urls import path
from . import views

app_name = 'toilet'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('search_toilet/', views.search_toilet, name='search_toilet'),
    path('suggest_station/', views.suggest_station, name='suggest_station'),
    path('male_toilet_info/<int:male_pk>/', views.male_toilet_info, name='male_toilet_info'),
    path('female_toilet_info/<int:female_pk>/', views.female_toilet_info, name='female_toilet_info'),
    path('multifunctional_toilet_info/<int:multi_pk>/', views.multifunctional_toilet_info, name='multifunctional_toilet_info'),
    path('change_toilet_data/<int:toilet_pk>/<int:gender_num>/', views.change_toilet_data, name='change_toilet_data'),
    path('toilet_review/', views.toilet_review, name='toilet_review')
]