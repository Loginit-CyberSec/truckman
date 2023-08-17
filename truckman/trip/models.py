from django.db import models
from django.db import transaction
from authentication.forms import Client

#---------------------------------- Vehicle models ------------------------------------------

#vehicle make/brand
class Vehicle_Make(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
#--

## Vehicle model model
class Vehicle_Model(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    make = models.ForeignKey(Vehicle_Make, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
#--

#Vehicle model
MILAGE_CHOICES = (
    ('kilometers','KILOMETERS'),
    ('miles','MILES'),
)

CONDITION_CHOICES = (
    ('operational','OPERATIONAL'),
    ('grounded','GROUNDED'),
)

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
#---

#---------------------------------- Driver Modules ------------------------------------------

# driver model
class Driver(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=12)
    last_name = models.CharField(max_length=12)
    id_no = models.CharField(max_length=12)
    dl_no = models.CharField(max_length=12)
    passport_number = models.CharField(max_length=12)
    tel_home = models.CharField(max_length=13)
    tel_roam = models.CharField(max_length=13)
    date_hired = models.DateField()
    date_terminated = models.DateField(null=True, blank=True)
    emergency_contact_person = models.CharField(max_length=50, null=True, blank=True)
    emergency_contact_no = models.CharField(max_length=14, null=True, blank=True)
    emergency_contact_two = models.CharField(max_length=14, null=True, blank=True)
    assigned_vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    passport_photo = models.ImageField(upload_to='driver_passports/', null=True, blank=True)

    def __str__(self):
        return self.first_name + self.last_name

#---------------------------------- Customer Modules ------------------------------------------

PAYMENT_TERM = (
    ('2 DAYS','2 Days'),
    ('7 DAYS','7 Days'),
    ('10 DAYS','10 Days'),
    ('15 DAYS','15 Days'),
    ('30 DAYS','30 Days'),
    ('Cash on Delivery','Cash on Delivery'),
) 
class Customer(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=7, unique=True, editable=False)
    name = models.CharField(max_length=50)
    contact_person = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address_one = models.CharField(max_length=50, null=True, blank=True)
    address_two = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    payment_term = models.CharField(max_length=50, choices=PAYMENT_TERM, default='2 DAYS')
    credit_limit = models.IntegerField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    logo = models.ImageField(upload_to='customer_logo/', null=True, blank=True)

    #generate customer_id 
    def save(self, *args, **kwargs):
        if not self.customer_id:
            prefix = 'CU'
            # Averting race condition using 'select_for_update()'
            with transaction.atomic():
                last_customer = Customer.objects.select_for_update().filter(customer_id__startswith=prefix).order_by('-customer_id').first()
                if last_customer:
                    last_id = last_customer.customer_id[2:]  # Remove prefix
                    next_id = str(int(last_id) + 1).zfill(4)
                    self.customer_id = prefix + next_id
                else:
                    self.customer_id = prefix + '0001'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
'''
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