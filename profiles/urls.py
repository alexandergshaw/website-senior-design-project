from django.urls import path
from django.contrib.auth import views as auth_views


app_name = 'profiles'
urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
