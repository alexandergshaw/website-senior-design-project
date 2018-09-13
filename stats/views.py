from django.shortcuts import render
from django.views import View


# Create your views here.


class ShowStatsView(View):
    def get(self, request, stat_id):
        return render(request, 'stats/stat_view.html')
