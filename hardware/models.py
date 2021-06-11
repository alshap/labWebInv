from django.db import models

from django.utils import timezone

from django.contrib.auth.models import User

from django.core.validators import MinValueValidator

from datetime import datetime, timedelta

class Category(models.Model):
    """
    Category model of hardwares
    """
    name = models.CharField(max_length = 50, unique = True)
    """Category name. Should be unique"""
    description = models.CharField(max_length=200, default='No description')
    """Category description. Not necessary field. Used only for visualization in template"""
    available = models.BooleanField(default = True)
    """Availability is used to specify is user can see category in template. Default True"""

    
    def hardwares_amount(self):
        """Get all hardware related to this category

        :return: Hardware list related to category
        :rtype: list
        """
        return len(self.hardware_set.all())
    
    def hardwares_available_amount(self):
        """Get all hardware related to this category with quantity > 0

        :return: Hardware list related to category with quantity > 0
        :rtype: list
        """
        hardwares = self.hardware_set.all()
        return len([x for x in hardwares if x.hardwareamount.quantity > 0])
    
    def hardwares_empty_amount(self):
        """Get all hardware related to this category with quantity <= 0

        :return: Hardware list related to category with quantity <= 0
        :rtype: list
        """
        hardwares = self.hardware_set.all()
        return len([x for x in hardwares if not x.hardwareamount.quantity > 0])
    
    def __str__(self):
        return self.name    

class Hardware(models.Model):
    """Hardware model"""
    name = models.CharField(max_length = 50, unique = True)
    """name is a text type. Should be unique with length not more than 50 symbols."""
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    """Foreign key referenced to Category model."""
    product_id = models.CharField(max_length = 50)
    """Currently field has no useful purpose and used to define only some hardwares product ids"""
    image_name = models.CharField(max_length = 50)
    """jpeg image filename"""
    available = models.BooleanField(default = True)
    """Availability is used to specify is user can see hardware in template. Default True"""

    def __str__(self):
        return self.name
    
    def get_amount(self):
        """Get hardware available quantity
        
        :return: numeric hardware available amount
        :rtype: int
        """
        return self.hardwareamount.quantity
    
class HardwareAmount(models.Model):
    """
    Hardware amount related to Hardware model.
    
    Is presented as a separate model in order not to load Hardware model.
    """
    hardware = models.OneToOneField(Hardware, on_delete = models.RESTRICT)
    """Foreign key related to hardware. OneToOne relationship."""
    quantity = models.PositiveIntegerField(default = 0, validators=[MinValueValidator(0)])
    """Current available quantity. Should be positive integer"""
    totalquantity = models.PositiveIntegerField(default = 0)
    """Total hardwares quantity. Should be positive integer"""
    
    def __str__(self):
        return self.hardware.name
        
    def get_hardware_name(self):
        """Get hardware name related to hardwareamount
        
        :return: hardware name
        :rtype: str
        """
        return Hardware.objects.get(pk=self.id).name
    
    def get_hardware_category(self):
        """Get hardware category related to hardwareamount
        
        :return: hardware category
        :rtype: Category
        """
        return Hardware.objects.get(pk=self.id).category

def month_after():
    """Get date 30 days after
        
    :return: datetime 30 days after
    :rtype: timestamp
    """
    return datetime.now() + timedelta(days = 30)

class TakenHardware(models.Model):
    """Recording model to track hardware which was taken"""
    taker = models.ForeignKey(User, on_delete = models.RESTRICT)
    """User who takes the hardware. Defined as foreign key on User"""
    hardware = models.ForeignKey(Hardware, on_delete = models.RESTRICT)
    """Hardware id Foreign key"""
    date_from = models.DateTimeField('take date', auto_now_add = True, blank = True)
    """Date when hardware was taken"""
    date_to = models.DateTimeField('return date', default = month_after())
    """Date when hardware should be given back. Default date is today+30days."""
    quantity = models.PositiveIntegerField(default = 1)
    """Hardware taken quantity. Should be >= 1"""
    description = models.CharField(max_length = 300, default = '')
    """Unnecessary description to specify something if needed"""
    
    def delete(self, *args, **kwargs):
        """
        Overwritten delete method
        
        Remember:
        
        **delete() method does not triggered using "delete selected objects"**
        **action in admin because triggers QuerySet.delete()**
        
        This method change hardwareamount value on TakenHardware object deletion.
        Else it triggers to create entry to archieve by creating TakenHardwareArchieve object.
        Then it triggers default delete() method 
        """
        h = Hardware.objects.get(pk=self.hardware.id)
        h.hardwareamount.quantity += int(self.quantity)
        h.hardwareamount.save()
        
        archieve_record = TakenHardwareArchieve(user = self.taker, hardware = self.hardware, quantity = self.quantity, description = self.description)
        archieve_record.save()
        
        super().delete(*args, **kwargs)
        
    def save(self, *args, **kwargs):
        """
        Overwritten save method
        
        This method changes HardwareAmount quantity on new TakenHardware object creation.
        It is necessary to save actual available hardware quantity.
        Then it triggers default delete() method.
        """
        h = Hardware.objects.get(pk=self.hardware.id)
        h.hardwareamount.quantity -= int(self.quantity)
        h.hardwareamount.save()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.taker.username + ' | ' + self.date_from.date().strftime("%m/%d/%Y") +'-'+ self.date_to.date().strftime("%m/%d/%Y") +' | '+ self.hardware.name+' | Q:'+ str(self.quantity)

class TakenHardwareArchieve(models.Model):
    """
        Archieve model for storing deleted TakenHardware objects. 
    """
    add_date = models.DateTimeField('return date', auto_now_add = True, blank = True)
    """Date when object was created."""
    hardware = models.ForeignKey(Hardware, on_delete = models.DO_NOTHING)
    """
    Hardware Foreign key.
    Important: On hardware deletion from database this field will not be affected.
    """
    user = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    """
    Foreign key User, who had taken the hardware.
    Important: On hardware deletion from database this field will not be affected.
    """
    quantity = models.PositiveIntegerField(default = 1)
    """Taken hardware quantity. Should be positive."""
    description = models.CharField(max_length = 300, default = '')
    """Not necessary description."""
    
    def __str__(self):
        return self.user.username + ' | ' + self.add_date.date().strftime("%m/%d/%Y") +' | '+ self.hardware.name+' | Q:'+ str(self.quantity)
