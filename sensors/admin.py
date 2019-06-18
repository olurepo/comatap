from django.contrib import admin

from sensors.models import Sensor, Data, TestConfig

# Register your models here.
class SensorAdmin(admin.ModelAdmin):
    pass

class DataAdmin(admin.ModelAdmin):
    pass

class TestConfigAdmin(admin.ModelAdmin):
    pass

admin.site.register(Sensor, SensorAdmin)
admin.site.register(Data, DataAdmin)
admin.site.register(TestConfig, TestConfigAdmin)
