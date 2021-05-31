from django.shortcuts import render
from django.views import generic

class IndexView(generic.ListView):
    template_name = 'guides/index.html'
    context_object_name = 'hardware_categories'
    
    def get_queryset(self):
        return None
