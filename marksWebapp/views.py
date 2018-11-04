from django.db.models import Max
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from stats.models import Stats


class Index(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            most_rec_measure = Stats.objects.filter(user=request.user)
            if most_rec_measure.exists():
                max_id = most_rec_measure.aggregate(Max('stat_id'))['stat_id__max']
                most_rec_measure = most_rec_measure.get(pk=max_id)
            else:
                most_rec_measure = None
        else:
            most_rec_measure = None
        context = {
            'title': 'Home',
            'most_recent_url': most_rec_measure.get_absolute_url() if most_rec_measure else reverse('stats:no_stats'),
        }
        return render(request, 'main/index.html', context)
