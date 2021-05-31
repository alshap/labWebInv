from django.db import models

from django.utils import timezone

from django.contrib.auth.models import User

from django.core.validators import MinValueValidator

from datetime import datetime, timedelta

class Category(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    description = models.CharField(max_length=200, default='No description')
    available = models.BooleanField(default = True)
    def __str__(self):
        return self.name    

class Hardware(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    product_id = models.CharField(max_length = 50)
    image_name = models.CharField(max_length = 50)
    available = models.BooleanField(default = True)

    def __str__(self):
        return self.name
    
    def get_amount(self):
        return self.hardwareamount.quantity
    
class HardwareAmount(models.Model):
    hardware = models.OneToOneField(Hardware, on_delete = models.RESTRICT)
    quantity = models.PositiveIntegerField(default = 0, validators=[MinValueValidator(0)])
    totalquantity = models.PositiveIntegerField(default = 0)
    
    def __str__(self):
        return self.hardware.name
        
    def get_hardware_name(self):
        return Hardware.objects.get(pk=self.id).name
    
    def get_hardware_category(self):
        return Hardware.objects.get(pk=self.id).category

def month_after():
    return datetime.now() + timedelta(days = 30)

class TakenHardware(models.Model):
    taker = models.ForeignKey(User, on_delete = models.RESTRICT)
    hardware = models.ForeignKey(Hardware, on_delete = models.RESTRICT)
    date_from = models.DateTimeField('take date', auto_now_add = True, blank = True)
    date_to = models.DateTimeField('return date', default = month_after())
    quantity = models.PositiveIntegerField(default = 1)
    description = models.CharField(max_length = 300, default = '')
    
#   delete() method does not triggered using "delete selected objects"
#   action in admin because triggers QuerySet.delete()
    def delete(self, *args, **kwargs):
        h = Hardware.objects.get(pk=self.hardware.id)
        h.hardwareamount.quantity += int(self.quantity)
        h.hardwareamount.save()
        
        archieve_record = TakenHardwareArchieve(user = self.taker, hardware = self.hardware, quantity = self.quantity, description = self.description)
        archieve_record.save()
        
        super().delete(*args, **kwargs)
        
    def save(self, *args, **kwargs):
        h = Hardware.objects.get(pk=self.hardware.id)
        h.hardwareamount.quantity -= int(self.quantity)
        h.hardwareamount.save()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.taker.username + ' | ' + self.date_from.date().strftime("%m/%d/%Y") +'-'+ self.date_to.date().strftime("%m/%d/%Y") +' | '+ self.hardware.name+' | Q:'+ str(self.quantity)

class TakenHardwareArchieve(models.Model):
    add_date = models.DateTimeField('return date', auto_now_add = True, blank = True)
    hardware = models.ForeignKey(Hardware, on_delete = models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    quantity = models.PositiveIntegerField(default = 1)
    description = models.CharField(max_length = 300, default = '')
    
    def __str__(self):
        return self.user.username + ' | ' + self.add_date.date().strftime("%m/%d/%Y") +' | '+ self.hardware.name+' | Q:'+ str(self.quantity)
