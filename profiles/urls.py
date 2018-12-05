from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    IndexPinSettingsView,
    AdminPinSettingsView,
    AdminView,
    DeleteUserView,
    ActivateUserView,
    ChangePermissionsView,
)


app_name = 'profiles'
urlpatterns = [
    path('pin_settings/', IndexPinSettingsView.as_view(), name='pin_settings'),
    path('pin_settings/<int:profile_id>/', AdminPinSettingsView.as_view(), name='admin_pin_settings'),
    path('admin/', AdminView.as_view(), name='admin'),
    path('delete/<int:user_id>/', DeleteUserView.as_view(), name='delete'),
    path('activate/<int:user_id>/', ActivateUserView.as_view(), name='activate'),
    path('permissions/<int:profile_id>/', ChangePermissionsView.as_view(), name='permissions'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
