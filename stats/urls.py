from django.urls import path

from . import views


app_name = 'stats'
urlpatterns = [
    path('<int:user_id>/<int:stat_id>/', views.ShowStatsView.as_view(), name='show_stats'),
    path('no_stats/', views.NoStatsView.as_view(), name='no_stats'),
    path('<int:stat_id>/delete/', views.DeleteStatsView.as_view(), name='delete'),
    path('history/<int:user_id>/', views.ShowStatsHistoryView.as_view(), name='stats_history'),
]