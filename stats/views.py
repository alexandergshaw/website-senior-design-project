import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .models import Stats


# Create your views here.


class ShowStatsView(LoginRequiredMixin, View):
    @staticmethod
    def get(request, stat_id):
        all_stats = Stats.objects.filter(user=request.user)
        power_measurements = all_stats.aggregate(Avg('power'))
        current_measurements = all_stats.aggregate(Avg('current'))
        voltage_measurements = all_stats.aggregate(Avg('voltage'))
        stat_requested = Stats.objects.get(stat_id=stat_id)
        context = {
            'power': stat_requested.power,
            'current': stat_requested.current,
            'voltage': stat_requested.voltage,
            'avg_power': '{0:.4f}'.format(power_measurements['power__avg']),
            'avg_current': '{0:.4f}'.format(current_measurements['current__avg']),
            'avg_voltage': '{0:.4f}'.format(voltage_measurements['voltage__avg']),
            'stat': stat_requested,
        }
        return render(request, 'stats/stat_view.html', context)


class NoStatsView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        context = {
            'title': 'No Stats to show you!',
        }
        return render(request, 'stats/no_stats_to_show.html', context)


class DeleteStatsView(LoginRequiredMixin, View):
    @staticmethod
    def get(request, stat_id):
        Stats.objects.filter(pk=stat_id).delete()
        return redirect(reverse('stats:stats_history'))


class ShowStatsHistoryView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        # Query the DB
        all_stats = Stats.objects.filter(user=request.user)

        if all_stats.exists():
            # Create a context with all of the results from the query
            context = { "all_stats": all_stats }
        else:
            # Create an empty context. The HTML will take care of things.
            context = {}
        return render(request, 'stats/stat_history.html', context)


class ExportStatsToExcelView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}_stats.csv"'.format(request.user.username)
        writer = csv.writer(response)
        writer.writerow(['Stat ID', 'Voltage', 'Current', 'Power', 'Time When Measured'])
        stats = Stats.objects.filter(user=request.user).values_list(
            'stat_id',
            'voltage',
            'current',
            'power',
            'time_when_measured',
        )
        for stat in stats:
            writer.writerow(stat)
        return response
