from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from .models import Project, ProjectSensorReadings
from django.shortcuts import get_object_or_404
from .models import Project

from django.utils.translation import activate
from django.conf import settings

class IndexView(generic.ListView):
    template_name = 'projects/index.html'
    
    context_object_name = 'projects'
    
    def get_queryset(self):
        return Project.objects.all()
    
    
def data_saver(request):
    try:
        n = request.GET['name']
        val_type = request.GET['val_type']
        val = request.GET['val']
#         val = int(val) if val == int(val) else float(val)
        val = float(val)
    except (KeyError, ValueError):
        return HttpResponse('Error')
    proj = get_object_or_404(Project, name = n)
    reading = ProjectSensorReadings(project = proj, value = val, value_type = val_type)
    reading.save()
    return HttpResponse('Success')

def getinfo(request, project_id):
    proj = get_object_or_404(Project, pk = project_id)
    response = render(request, 'projects/index.html', {
                'selected_proj': proj,
                'last_readings': proj.projectsensorreadings_set.all().order_by('value_type','-date').distinct('value_type'),
                'projects': Project.objects.all(),
                'error_message': 'Unexpected error occured',
                        }
                    )
    return response
    
    
    
