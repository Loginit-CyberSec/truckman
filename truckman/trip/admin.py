from django.contrib import admin
from .models import Vehicle, Vehicle_Make , Vehicle_Model, Driver, Customer, Consignee, Trip, Shipper

# Register your models here.
admin.site.register(Vehicle)
admin.site.register(Vehicle_Make)
admin.site.register(Vehicle_Model)
admin.site.register(Driver)
admin.site.register(Customer)
admin.site.register(Trip)
admin.site.register(Consignee)
admin.site.register(Shipper)