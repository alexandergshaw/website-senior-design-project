from django.urls import path

from . import views


app_name = 'stats'
urlpatterns = [
    path('<int:stat_id>/', views.ShowStatsView.as_view(), name='show_stats'),
]