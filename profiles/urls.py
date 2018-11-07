from django.urls import path
from django.contrib.auth import views as auth_views

from .views import SettingsView


app_name = 'profiles'
urlpatterns = [
    path('user_profile/', SettingsView.as_view(), name='user_profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
