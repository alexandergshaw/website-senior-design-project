from django.shortcuts import render
from django.views import View


class Index(View):
    def get(self, request):
        context = {
            'title': 'Login',
        }
        return render(request, 'profiles/login.html', context)
