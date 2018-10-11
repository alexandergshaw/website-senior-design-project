from django.db.models import Max
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from stats.models import Stats


class Index(View):
    def get(self, request):
        if request.user.is_authenticated:
            most_rec_measure = Stats.objects.filter(username=request.user.username)
            if most_rec_measure.count() == 0:
                most_rec_measure = None
            else:
                max_id = most_rec_measure.aggregate(Max('stat_id'))['stat_id__max']
                most_rec_measure = most_rec_measure.get(pk=max_id)
        else:
            most_rec_measure = None
        context = {
            'title': 'Login',
            'most_recent_url':
                reverse(most_rec_measure.get_absolute_url()) if most_rec_measure else reverse('stats:no_stats'),
        }
        return render(request, 'main/index.html', context)
