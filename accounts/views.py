from django.shortcuts import render

from django.views import generic

from django.contrib.auth.models import User


# Create your views here.

class IndexView(generic.ListView):
    template_name = 'accounts/index.html'
    model = User