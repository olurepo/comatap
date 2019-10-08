from django.db import models
from projects.models import Project
import uuid
from django.utils import timezone

# Create your models here.
class Sensor(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sensor_name = models.CharField(max_length=50)
    date_created = models.DateTimeField(default=timezone.now)
    sensor_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f'{self.sensor_name} ({self.project.title})'
        
class Data(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    time_taken = models.DateTimeField(default=timezone.now)
    ave_temp = models.FloatField()
    ave_hum = models.FloatField()
    last_updated = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.sensor.sensor_name}'

class Temp_Hum_Data(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, default='')
    approx_age = models.FloatField()
    approx_temp = models.FloatField()
    approx_hum = models.FloatField()
    last_updated = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.sensor.sensor_name}'

class Maturity_Data(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, default='')
    equivalent_age = models.FloatField()
    matu_index = models.FloatField()
    last_updated = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.sensor.sensor_name}'


class Strength_Data(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, default='')
    concrete_age = models.FloatField()
    concrete_strength = models.FloatField()
    last_updated = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.sensor.sensor_name}'


class TestConfig(models.Model):
    datum_temp = models.FloatField(default= -10, editable = True, null=True, blank=False)
    activation_energy = models.FloatField(default= 41000, editable=True, null=True, blank=False)
    gas_constant = models.FloatField(default= 8.314, editable=True, null=True, blank=False)
    ref_temp = models.FloatField(default= 23.0, editable=True, null=True, blank=False) # Europe, America etc
    ultimate_strength = models.FloatField(default= 50.0, editable=True, null=True, blank=False) # N/sq.mm
    a = models.FloatField(default= 3.45, editable=True, null=True, blank=False)
    b = models.FloatField(default= 0.9, editable=True, null=True, blank=False)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, default='')

    def __str__(self):
        return f'{self.sensor.project.title} Project Configuration'
    
    def save(self):
        super().save()
