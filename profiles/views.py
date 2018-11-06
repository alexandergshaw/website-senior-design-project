from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from marksWebapp.utils import get_most_recent_measurement_url


user_profile_decorators = [transaction.atomic]


@method_decorator(user_profile_decorators, name='dispatch')
class UserProfileView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        context = {'title': 'User Profile', 'most_recent_url': get_most_recent_measurement_url(request)}
        return render(request, 'profiles/user_profile.html', context)
