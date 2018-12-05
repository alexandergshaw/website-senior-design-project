from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View

from marksWebapp.utils import get_most_recent_measurement_url

from .forms import PhaseForm, PermissionsForm
from .models import Profile


settings_decorators = [transaction.atomic]
admin_decorators = [transaction.atomic]
delete_user_decorators = [transaction.atomic]
activate_user_decorators = [transaction.atomic]
change_permissions_decorators = [transaction.atomic]


@method_decorator(settings_decorators, name='dispatch')
class BasePinSettingsView(LoginRequiredMixin, View):
    PHASE_1 = 'Phase 1'
    PHASE_2 = 'Phase 2'
    PHASE_3 = 'Phase 3'

    redirect_url = reverse_lazy('index')

    @staticmethod
    def process_initial_data(phase_pins, initial_settings):
        pins = eval(phase_pins) if phase_pins else None
        if pins:
            count = 1
            for pin_value in pins['pins']:
                initial_settings['pin{}'.format(count)] = pin_value
                count += 1

    def super_get(self, request, profile):
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
            'cancel_url': self.redirect_url,
        }
        return render(request, 'profiles/pin_settings.html', context)

    def super_post(self, request, profile):
        phase_1_form = PhaseForm(request.POST, prefix=self.PHASE_1)
        phase_2_form = PhaseForm(request.POST, prefix=self.PHASE_2)
        phase_3_form = PhaseForm(request.POST, prefix=self.PHASE_3)
        if phase_1_form.is_valid() and phase_2_form.is_valid() and phase_3_form.is_valid():
            profile.phase_1_settings = {'pins': list(phase_1_form.cleaned_data.values())}
            profile.phase_2_settings = {'pins': list(phase_2_form.cleaned_data.values())}
            profile.phase_3_settings = {'pins': list(phase_3_form.cleaned_data.values())}
            profile.save()
            messages.success(request, 'Pin Configurations Successfully Stored.')
            return redirect(self.redirect_url)
        else:
            messages.error(request, 'Something Went Wrong On Server Side Processing.')
            context = {
                'title': 'Pin Settings for {}'.format(profile),
                'most_recent_url': get_most_recent_measurement_url(request),
                'phase_1_form': phase_1_form,
                'phase_2_form': phase_2_form,
                'phase_3_form': phase_3_form,
                'cancel_url': self.redirect_url,
            }
            return render(request, 'profiles/pin_settings.html', context)


class IndexPinSettingsView(BasePinSettingsView):
    def get(self, request):
        return super(IndexPinSettingsView, self).super_get(request, request.user.profile)

    def post(self, request):
        return super(IndexPinSettingsView, self).super_post(request, request.user.profile)


class AdminPinSettingsView(BasePinSettingsView):
    redirect_url = reverse_lazy('profiles:admin')

    def get(self, request, profile_id):
        return super(AdminPinSettingsView, self).super_get(request, get_object_or_404(Profile, pk=profile_id))

    def post(self, request, profile_id):
        return super(AdminPinSettingsView, self).super_post(request, get_object_or_404(Profile, pk=profile_id))


@method_decorator(admin_decorators, name='dispatch')
class AdminView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'title': 'Manage Users',
            'users': User.objects.exclude(username=request.user.username),
        }
        return render(request, 'profiles/admin.html', context)


@method_decorator(delete_user_decorators, name='dispatch')
class DeleteUserView(LoginRequiredMixin, View):
    @staticmethod
    def get(request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.delete()
        messages.success(request, 'User {} was successfully deleted.'.format(user))
        return redirect(reverse('profiles:admin'))


@method_decorator(activate_user_decorators, name='dispatch')
class ActivateUserView(LoginRequiredMixin, View):
    @staticmethod
    def get(request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.profile.is_activated = True
        user.profile.save()
        messages.success(request, 'User {} has been successfully activated.'.format(user))
        return redirect(reverse('profiles:admin'))


@method_decorator(change_permissions_decorators, name='dispatch')
class ChangePermissionsView(LoginRequiredMixin, View):
    @staticmethod
    def get(request, profile_id):
        profile = get_object_or_404(Profile, pk=profile_id)
        context = {
            'title': 'Modify Permissions for {}.'.format(profile),
            'form': PermissionsForm(instance=profile),
        }
        return render(request, 'profiles/permissions_form.html', context)

    @staticmethod
    def post(request, profile_id):
        profile = get_object_or_404(Profile, pk=profile_id)
        form = PermissionsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'User {} has been set to permission level: {}.'.format(
                    profile,
                    profile.STATUS_CHOICES_DICT[profile.status],
                ),
            )
            return redirect(reverse('profiles:admin'))
        else:
            messages.error(request, 'Something has gone wrong on the server side.')
            context = {
                'title': 'Modify Permissions for {}.'.format(profile),
                'form': form,
            }
            return render(request, 'profiles/permissions_form.html', context)
