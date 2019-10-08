from django.contrib import admin

from sensors.models import Sensor, Data, TestConfig, Temp_Hum_Data

# Register your models here.
class SensorAdmin(admin.ModelAdmin):
    pass

class DataAdmin(admin.ModelAdmin):
    pass

class TestConfigAdmin(admin.ModelAdmin):
    pass

class Temp_Hum_DataAdmin(admin.ModelAdmin):
    pass

admin.site.register(Sensor, SensorAdmin)
admin.site.register(Data, DataAdmin)
admin.site.register(TestConfig, TestConfigAdmin)
admin.site.register(Temp_Hum_Data, Temp_Hum_DataAdmin)
