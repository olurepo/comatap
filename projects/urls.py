from django.urls import path, include
from . import views
#from .views import ConfigurationView

urlpatterns = [
    path('', views.project_index, name='project-index'),
    path('project-details/<int:pk>/', views.project_detail, name='project-detail'),
    path('about-maturity-project/', views.about, name='project-about'),
    path('project_sensors/', include('sensors.urls')),
    #path('configuretest/', ConfigurationView.as_view(), name='config'),
]
