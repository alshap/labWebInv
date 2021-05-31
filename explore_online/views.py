from django.shortcuts import render
from django.views import generic

class IndexView(generic.ListView):
    template_name = 'explore_online/index.html'
    
    def get_queryset(self):
        return None