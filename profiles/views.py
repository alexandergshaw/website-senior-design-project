from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.views import View

from marksWebapp.utils import get_most_recent_measurement_url

from .forms import PhaseForm


settings_decorators = [transaction.atomic]


@method_decorator(settings_decorators, name='dispatch')
class SettingsView(LoginRequiredMixin, View):
    PHASE_1 = 'Phase 1'
    PHASE_2 = 'Phase 2'
    PHASE_3 = 'Phase 3'

    @staticmethod
    def process_initial_data(phase_pins, initial_settings):
        pins = eval(phase_pins)
        if pins:
            count = 1
            for pin_value in pins['pins']:
                initial_settings['pin{}'.format(count)] = pin_value
                count += 1

    def get(self, request):
        profile = request.user.profile
        phase_1_initial = {}
        phase_2_initial = {}
        phase_3_initial = {}
        self.process_initial_data(profile.phase_1_settings, phase_1_initial)
        self.process_initial_data(profile.phase_2_settings, phase_2_initial)
        self.process_initial_data(profile.phase_3_settings, phase_3_initial)
        context = {
            'title': 'Pin Settings for {}'.format(profile),
            'most_recent_url': get_most_recent_measurement_url(request),
            'phase_1_form': PhaseForm(initial=phase_1_initial, prefix=self.PHASE_1),
            'phase_2_form': PhaseForm(initial=phase_2_initial, prefix=self.PHASE_2),
            'phase_3_form': PhaseForm(initial=phase_3_initial, prefix=self.PHASE_3),
        }
        return render(request, 'profiles/pin_settings.html', context)

    def post(self, request):
        profile = request.user.profile
        phase_1_form = PhaseForm(request.POST, prefix=self.PHASE_1)
        phase_2_form = PhaseForm(request.POST, prefix=self.PHASE_2)
        phase_3_form = PhaseForm(request.POST, prefix=self.PHASE_3)
        if phase_1_form.is_valid() and phase_2_form.is_valid() and phase_3_form.is_valid():
            profile.phase_1_settings = {'pins': list(phase_1_form.cleaned_data.values())}
            profile.phase_2_settings = {'pins': list(phase_2_form.cleaned_data.values())}
            profile.phase_3_settings = {'pins': list(phase_3_form.cleaned_data.values())}
            profile.save()
            messages.success(request, 'Pin Configurations Successfully Stored.')
            return redirect(reverse('index'))
        else:
            messages.error(request, 'Something Went Wrong On Server Side Processing.')
            context = {
                'title': 'Pin Settings for {}'.format(profile),
                'most_recent_url': get_most_recent_measurement_url(request),
                'phase_1_form': phase_1_form,
                'phase_2_form': phase_2_form,
                'phase_3_form': phase_3_form,
            }
            return render(request, 'profiles/pin_settings.html', context)
