from django.db import models

from hardware.models import Hardware, HardwareAmount
# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    description = models.CharField(max_length=200, default='No description')
    image_name = models.CharField(max_length = 50, unique = True)
    schema_name = models.CharField(max_length = 50, unique = True)
    available = models.BooleanField(default = True)
    
    def __str__(self):
        return self.name
    
class ProjectHardware(models.Model):
    hardware = models.ForeignKey(Hardware, on_delete = models.CASCADE)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    
    def save(self, *args, **kwargs):
        h = self.hardware
        h.hardwareamount.quantity -= int(self.quantity)
        h.hardwareamount.save()
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        h = self.hardware
        h.hardwareamount.quantity += int(self.quantity)
        h.hardwareamount.save()
        super().delete(*args, **kwargs)
       
    
class ProjectSensorReadings(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    date = models.DateTimeField('save date', auto_now_add = True, blank = True)
    value = models.FloatField()
    value_type = models.CharField(max_length = 50)