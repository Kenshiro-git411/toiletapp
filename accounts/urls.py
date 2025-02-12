from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('home', views.home, name='home'),
    path('user_login', views.user_login, name='user_login'),
    path('user_create', views.user_create, name='user_create'),
    path('user_logout', views.user_logout, name='user_logout'),
]