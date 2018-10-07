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

        # Print some basic debug info
        print(self.all_stats)
        print(len(self.all_stats))
        print(user_id)
        if len(self.all_stats) > 0:
            # PyCharm does not like this aggregate call and I cannot figure out why.
            # The one in the basic Stats view does not throw this flag.
            power_measurements = self.all_stats.aggregate(Avg('power'))
            current_measurements = self.all_stats.aggregate(Avg('current'))
            voltage_measurements = self.all_stats.aggregate(Avg('voltage'))
            context = {
                'power': self.all_stats.power,
                'current': self.all_stats.current,
                'voltage': self.all_stats.voltage,
                'avg_power': power_measurements['power__avg'],
                'avg_current': current_measurements['current__avg'],
                'avg_voltage': voltage_measurements['voltage__avg'],
            }
            self.all_stats = context
        else:
            # Create an empty context. The HTML will take care of things.
            context = {}
        return render(request, 'stats/stat_history.html', context)
