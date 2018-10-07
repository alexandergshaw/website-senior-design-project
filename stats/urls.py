from django.urls import path

from . import views


app_name = 'stats'
urlpatterns = [
    path('<int:user_id>/<int:stat_id>/', views.ShowStatsView.as_view(), name='show_stats'),
    path('history/<int:user_id>/', views.ShowStatsHistoryView.as_view(), name='stats_history')
]