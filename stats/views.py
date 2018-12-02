import csv
import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.core.serializers.json import DjangoJSONEncoder

from marksWebapp.utils import get_most_recent_measurement_url

from .models import Stats
from .forms import filterForm

show_stats_decorators = [transaction.atomic]
no_stats_decorators = [transaction.atomic]
delete_stat_decorators = [transaction.atomic]
stat_history_decorators = [transaction.atomic]
export_stats_decorators = [transaction.atomic]


@method_decorator(show_stats_decorators, name='dispatch')
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
            'most_recent_url': get_most_recent_measurement_url(request),
        }
        return render(request, 'stats/stat_view.html', context)


@method_decorator(no_stats_decorators, name='dispatch')
class NoStatsView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        context = {'title': 'No Stats to show you!', 'most_recent_url': get_most_recent_measurement_url(request)}
        return render(request, 'stats/no_stats_to_show.html', context)


@method_decorator(delete_stat_decorators, name='dispatch')
class DeleteStatsView(LoginRequiredMixin, View):
    @staticmethod
    def get(request, stat_id):
        Stats.objects.filter(pk=stat_id).delete()
        messages.success(request, 'Statistic successfully removed from database.')
        return redirect(reverse('stats:stats_history'))


@method_decorator(stat_history_decorators, name='dispatch')
class ShowStatsHistoryView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        # Query the DB
        all_stats = Stats.objects.filter(user=request.user).values_list('pk', 'time_when_measured', 'user', 'voltage', 'current', 'power')
        context = {'title': 'All Recorded Measurements', 'most_recent_url': get_most_recent_measurement_url(request)}
        if all_stats.exists():
            all_stats = json.dumps(list(all_stats), cls=DjangoJSONEncoder)
            form = filterForm()
            # Create a context with all of the results from the query
            context['all_stats'] = all_stats
            context['form'] = form
        return render(request, 'stats/stat_history.html', context)


@method_decorator(export_stats_decorators, name='dispatch')
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
