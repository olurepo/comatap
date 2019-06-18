from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Project
from sensors.models import Sensor, Data
from sensors.forms import TestConfiguration, MaturityForm

def about(request):

    return render(request, 'blog/about.html')   #, {'title': 'About'})

    
def project_index(request):
    projects = Project.objects.all()
    context = {
        'projects': projects,
    }
    return render(request, 'projects/project_index.html', context)


def project_detail(request, pk):
    project = Project.objects.get(pk=pk)
    sensors = Sensor.objects.filter(project=project)

    context = {
        'project': project,
        'sensors': sensors,
    }
    return render(request, 'projects/project_detail.html', context)


"""
class ConfigurationView(TemplateView):
    template_name = 'projects/configuretest.html'

    def get(self, request):
        form = MaturityForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = MaturityForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['datum_temp']
        args = {'form': form, 'text': text}
        print(text*2)
        return render(request, self.template_name, args)
"""