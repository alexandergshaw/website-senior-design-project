from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.shortcuts import render
from django.views import View

from .models import Stats


# Create your views here.


class ShowStatsView(LoginRequiredMixin, View):
    def get(self, request, user_id, stat_id):
        all_stats = Stats.objects.filter(user_id=user_id)
        power_measurements = all_stats.aggregate(Avg('power'))
        current_measurements = all_stats.aggregate(Avg('current'))
        voltage_measurements = all_stats.aggregate(Avg('voltage'))
        stat_requested = Stats.objects.get(stat_id=stat_id)

        context = {
            'power': stat_requested.power,
            'current': stat_requested.current,
            'voltage': stat_requested.voltage,
            'avg_power': power_measurements['power__avg'],
            'avg_current': current_measurements['current__avg'],
            'avg_voltage': voltage_measurements['voltage__avg'],
        }
        return render(request, 'stats/stat_view.html', context)


class ShowStatsHistoryView(LoginRequiredMixin, View):
    model = Stats
    all_stats = list()
    def get(self, request, user_id):
        # Query the DB
        self.all_stats = Stats.objects.filter(user_id=user_id)

        if len(self.all_stats) > 0:
            # Create a context with all of the results from the query
            context = { "all_stats": self.all_stats }
        else:
            # Create an empty context. The HTML will take care of things.
            context = {}
        return render(request, 'stats/stat_history.html', context)
