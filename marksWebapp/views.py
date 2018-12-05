from django.db import transaction
from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.views import View

from .utils import get_most_recent_measurement_url


index_decorators = [transaction.atomic]


@method_decorator(index_decorators, name='dispatch')
class Index(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated and not request.user.profile.ui_password:
            return redirect(reverse('profiles:set_ui_password', kwargs={'profile_id': request.user.id}))
        context = {'title': 'Home', 'most_recent_url': get_most_recent_measurement_url(request)}
        return render(request, 'main/index.html', context)
