from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Project
from sensors.models import Sensor, Data

def about(request):

    return render(request, 'projects/project_about.html')   #, {'title': 'About'})

    
def project_index(request):
    projects = Project.objects.all()
    context = {
        'projects': projects,
    }
    return render(request, 'projects/project_index.html', context)


def project_detail(request, pk):
    project = Project.objects.get(pk=pk)
    sensors = Sensor.objects.filter(project=project)

    describe = project.description

    context = {
        'project': project,
        'sensors': sensors,
        'describe': describe,
    }
    return render(request, 'projects/project_detail.html', context)
