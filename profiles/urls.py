from django.urls import path
from django.contrib.auth import views as auth_views

from .views import SettingsView


app_name = 'profiles'
urlpatterns = [
    path('pin_settings/', SettingsView.as_view(), name='pin_settings'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
