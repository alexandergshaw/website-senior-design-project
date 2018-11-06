from django.db.models import Max
from django.urls import reverse

from stats.models import Stats


def get_most_recent_measurement_url(request):
    if request.user.is_authenticated:
        most_rec_measure = Stats.objects.filter(user=request.user)
        if most_rec_measure.exists():
            max_id = most_rec_measure.aggregate(Max('stat_id'))['stat_id__max']
            most_rec_measure = most_rec_measure.get(pk=max_id)
        else:
            most_rec_measure = None
    else:
        most_rec_measure = None
    return most_rec_measure.get_absolute_url() if most_rec_measure else reverse('stats:no_stats')
