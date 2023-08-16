from django.contrib import admin
from .models import Vehicle, Vehicle_Make , Vehicle_Model

# Register your models here.
admin.site.register(Vehicle)
admin.site.register(Vehicle_Make)
admin.site.register(Vehicle_Model)