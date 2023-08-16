from django.db import models
from authentication.forms import Client

#vehicle models start
class Vehicle_Make(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Vehicle_Model(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    make = models.ForeignKey(Vehicle_Make, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


MILAGE_CHOICES = (
    ('kilometers','KILOMETERS'),
    ('miles','MILES'),
)

CONDITION_CHOICES = (
    ('operational','OPERATIONAL'),
    ('grounded','GROUNDED'),
)

# Create your models here.
class Vehicle(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    plate_number = models.CharField(max_length=10, unique=True)
    trailer_number = models.CharField(max_length=10, unique=True)
    vin = models.CharField(max_length=20, unique=True)
    make = models.ForeignKey(Vehicle_Make, on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey(Vehicle_Model, on_delete=models.SET_NULL, null=True)
    color = models.CharField(null=True, blank=True)
    milage_unit = models.CharField(max_length=10, choices=MILAGE_CHOICES, default='kilometers')
    milage = models.PositiveIntegerField(null=True, blank=True)
    insurance_expiry = models.DateField(null=True)
    manufacture_year = models.DateField(null=True)
    purchase_year = models.DateField(null=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='operational')
    image = models.ImageField(upload_to='vehicle_images/', null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.plate_number

#end of vehicle models

'''
# Create your models here.
class Driver(models.Model):
    pass

# Create your models here.
class Customer(models.Model):
    pass

# Create your models here.
class Consignee(models.Model):
    pass

# Create your models here.
class Trip(models.Model):
    pass

# Create your models here.
class Reminders(models.Model):
    pass

# Create your models here.
class Repair_Expenses(models.Model):
    pass
'''