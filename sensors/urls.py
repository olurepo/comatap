from django.urls import path
from . import views


urlpatterns = [
    #path('configure/', views.test_configuration, name='configure-test'),
    path('maturity-data/<int:pk>/', views.combined_data, name='combined-data'),
    path('temperature&humidity-data/<int:pk>/', views.Temp_Humid, name='Temp-Humid')
    path('concrete-strength-data/<int:pk>/', views.Strength, name='concrete-strength'),
    path('concrete-maturity-data/<int:pk>/', views.Maturity, name='concrete-maturity'),
    path('test-configuration/<int:pk>/', views.get_data, name='get-data'),
]