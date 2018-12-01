from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from marksWebapp.utils import get_most_recent_measurement_url


settings_decorators = [transaction.atomic]


@method_decorator(settings_decorators, name='dispatch')
class SettingsView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        context = {
            'title': 'Pin Settings for {}'.format(request.user.username),
            'most_recent_url': get_most_recent_measurement_url(request),
        }
        return render(request, 'profiles/user_profile.html', context)
