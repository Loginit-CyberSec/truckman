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
    color = models.CharField(max_length=50, null=True)
    milage_unit = models.CharField(max_length=10, choices=MILAGE_CHOICES, default='kilometers')
    milage = models.PositiveIntegerField(null=True)
    insurance_expiry = models.DateField(null=True)
    manufacture_year = models.DateField(null=True)
    purchase_year = models.DateField(null=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='operational')
    notes = models.TextField(null=True, blank=True)
    truck_image = models.ImageField(upload_to='vehicle_images/', null=True)
    trailer_image = models.ImageField(upload_to='vehicle_images/', null=True)
    truck_logbook = models.ImageField(upload_to='vehicle_images/', null=True)
    trailer_logbook = models.ImageField(upload_to='vehicle_images/', null=True)
    good_transit_licence  = models.ImageField(upload_to='vehicle_images/', null=True)
     

    def __str__(self):
        return self.plate_number

#---------------------------------- Driver Modules ---------------------------------------------
# driver model
DL_ISSUERER = (
    ('NTSA','NTSA'),
    ('TRA','TRA'),
    ('ZRA','ZRA'),
    ('RRA','RRA'),
    ('URA','URA'),
)

KIN_RLSHP = (
    ('Spouse','SPOUSE'),
    ('Daughter','DAUGHTER'),
    ('Son','SON'),
    ('Mother','MOTHER'),
    ('Father','FATHER'),
    ('Other','OTHER'),
)
class Driver(models.Model):
    #personal data
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=12)
    last_name = models.CharField(max_length=12)
    id_no = models.CharField(max_length=12) 
    tel_home = models.CharField(max_length=13)
    tel_roam = models.CharField(max_length=13)
    date_hired = models.DateField()
    date_terminated = models.DateField(null=True, blank=True)
    driver_photo = models.ImageField(upload_to='driver_photos/', null=True)
    id_img = models.ImageField(upload_to='driver_photos/', null=True)
    #dl and passport data
    dl_no = models.CharField(max_length=12)
    dl_issuing_authority = models.CharField(max_length=50, choices=DL_ISSUERER, null=True)
    dl_front_img = models.ImageField(upload_to='driver_passports_dl/', null=True)
    dl_back_img = models.ImageField(upload_to='driver_passports_dl/', null=True)
    passport_number = models.CharField(max_length=12)
    passport_image = models.ImageField(upload_to='driver_passports_dl/', null=True)
    # next of kin data
    emergency_contact_person = models.CharField(max_length=50, null=True, blank=True)
    emergency_contact_person_rlshp = models.CharField(max_length=30, choices=KIN_RLSHP, default='Spouse')
    emergency_contact_no = models.CharField(max_length=14, null=True, blank=True)
    emergency_contact_two = models.CharField(max_length=14, null=True, blank=True)
    #vehicle data
    assigned_vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    

    def __str__(self):
        return self.first_name + self.last_name

#---------------------------------- Customer Modules -------------------------------------------

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


#---------------------------------- Consignee & Shipper Modules ------------------------------------------

#shipper model
class Shipper(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    shipper_id = models.CharField(max_length=7, unique=True, editable=False) 
    name = models.CharField(max_length=50)
    contact_person = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address_one = models.CharField(max_length=50, null=True, blank=True)
    address_two = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    logo = models.ImageField(upload_to='customer_logo/', null=True, blank=True)
    

    #generate consignee_id 
    def save(self, *args, **kwargs):
        if not self.shipper_id:
            prefix = 'SH'
            # Averting race condition using 'select_for_update()'
            with transaction.atomic():
                last_shipper = Shipper.objects.select_for_update().filter(shipper_id__startswith=prefix).order_by('-shipper_id').first()
                if last_shipper:
                    last_id = last_shipper.shipper_id[2:]  # Remove prefix
                    next_id = str(int(last_id) + 1).zfill(4)
                    self.shipper_id = prefix + next_id
                else:
                    self.shipper_id = prefix + '0001'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# consignee model
class Consignee(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    consignee_id = models.CharField(max_length=7, unique=True, editable=False)
    name = models.CharField(max_length=50)
    contact_person = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address_one = models.CharField(max_length=50, null=True, blank=True)
    address_two = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    logo = models.ImageField(upload_to='customer_logo/', null=True, blank=True)

    #generate consignee_id 
    def save(self, *args, **kwargs):
        if not self.consignee_id:
            prefix = 'CO'
            # Averting race condition using 'select_for_update()'
            with transaction.atomic():
                last_consignee = Consignee.objects.select_for_update().filter(consignee_id__startswith=prefix).order_by('-consignee_id').first()
                if last_consignee:
                    last_id = last_consignee.consignee_id[2:]  # Remove prefix
                    next_id = str(int(last_id) + 1).zfill(4)
                    self.consignee_id = prefix + next_id
                else:
                    self.consignee_id = prefix + '0001'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

#---------------------------------- Trip & Load Modules -----------------------------------------------

#Load model
FEE_TYPE = (
    ('FLAT FEE','Flat Fee'),
    ('PER MILE','Per Mile'),
    ('PER HUNDRED WEIGHT','Per Hundred Weight'),
    ('PER TON','Per Ton'),
    ('PER QUANTITY','Per Quantity'),
) 

AMOUNT_TYPE = (
    ('FLAT FEE','Flat Fee'),
    ('PER MILE','Per Mile'),
    ('PERCENTAGE','Percent')
) 

QUANTITY_TYPE = (
    ('BARREL','Barrel'),
    ('BOXES','Boxes'),
    ('BUSHELS','Bushels'),
    ('CASES','Cases'),
    ('CRATES','Crates'),
    ('GALLONS','Gallons'),
    ('PALLETS','Pallets'),
    ('PIECES','Pieces'),
) 

class Load(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    load_id = models.CharField(max_length=7, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    shipper = models.ForeignKey(Shipper, on_delete=models.SET_NULL, null=True)
    consignee = models.ForeignKey(Consignee, on_delete=models.SET_NULL, null=True)
    #load details
    quantity = models.CharField(max_length=20, choices=QUANTITY_TYPE, default='Barrel')
    quantity_type = models.CharField(max_length=20, choices=QUANTITY_TYPE, default='Barrel')
    weight =  models.IntegerField(null=True, blank=True)
    commodity = models.CharField(max_length=155)
    pickup_date = models.DateField()
    delivery_date = models.DateField()
    driver_instructions = models.TextField(null=True, blank=True)
    #-Fees / Charges attributes -
    #--primary fee--
    primary_fee = models.FloatField()
    primary_fee_type = models.CharField(max_length=30, choices=FEE_TYPE, default='Per Mile')
    fuel_surcharge_fee = models.FloatField()
    fsc_amount_type = models.CharField(max_length=30, choices=AMOUNT_TYPE, default='Flat Fee')
    #--accessory fees--
    broker_commission = models.FloatField(null=True, blank=True)
    border_agent_fee = models.FloatField()
    road_user = models.FloatField()
    gate_tolls = models.FloatField()
    #fines = models.FloatField()
    #additional_fees = models.FloatField()
    invoice_advance = models.FloatField()
    #others
    legal_disclaimer = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    #generate customer_id 
    def save(self, *args, **kwargs):
        if not self.load_id:
            prefix = 'LO'
            # Averting race condition using 'select_for_update()'
            with transaction.atomic():
                last_load = Load.objects.select_for_update().filter(load_id__startswith=prefix).order_by('-load_id').first()
                if last_load:
                    last_id = last_load.load_id[2:]  # Remove prefix
                    next_id = str(int(last_id) + 1).zfill(4)
                    self.load_id = prefix + next_id
                else:
                    self.load_id = prefix + '0001'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.load_id

# trip model
class Trip(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    trip_id = models.CharField(max_length=7, unique=True, editable=False)
    load = models.ForeignKey(Load, on_delete=models.SET_NULL , null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL , null=True)
    vehicle_odemeter = models.BigIntegerField()
    #pickup_cordinates = models.PointField(null=True)
    #destination_cordinates =
    driver_accesory_pay = models.IntegerField(null=True)
    driver_advance = models.IntegerField(null=True)
    driver_milage = models.FloatField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    #generate customer_id 
    def save(self, *args, **kwargs):
        if not self.trip_id:
            prefix = 'TR'
            # Averting race condition using 'select_for_update()'
            with transaction.atomic():
                last_trip = Trip.objects.select_for_update().filter(trip_id__startswith=prefix).order_by('-trip_id').first()
                if last_trip:
                    last_id = last_trip.trip_id[2:]  # Remove prefix
                    next_id = str(int(last_id) + 1).zfill(4)
                    self.trip_id = prefix + next_id
                else:
                    self.trip_id = prefix + '0001'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.trip_id

#---------------------------------- Estimate  & Service Modules -----------------------------------------------
# service model
UNIT_TYPE = (
    ('KM','Kilometer'),
    ('MILE','Mile'),
    ('HUNDRED WEIGHT','Per Hundred Weight'),
    ('TON','Ton'),
    ('QUANTITY','Quantity'),
)
class Service(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPE) #km/miles
    unit = models.IntegerField(default=1) #km/miles
    unit_price = models.FloatField(default=0.00)
    tax = models.FloatField(default=0.00) #in %
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

# estimate model
class Estimate(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    estimate_id = models.CharField(max_length=7, unique=True, editable=False)
    services = models.ManyToManyField(Service) 
    sub_total = models.FloatField(default=0.00)
    discount = models.FloatField(default=0.00)
    total = models.FloatField(default=0.00)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    valid_till = models.DateField()
    date_added = models.DateTimeField(auto_now_add=True)
    note = models.TextField(null=True)

    #generate customer_id 
    def save(self, *args, **kwargs):
        if not self.trip_id:
            prefix = 'QU'
            # Averting race condition using 'select_for_update()'
            with transaction.atomic():
                last_estimate = Estimate.objects.select_for_update().filter(estimate_id__startswith=prefix).order_by('-estimate_id').first()
                if last_estimate:
                    last_id = last_estimate.estimate_id[2:]  # Remove prefix
                    next_id = str(int(last_id) + 1).zfill(4)
                    self.estimate_id = prefix + next_id
                else:
                    self.estimate_id = prefix + '0001'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.estimate_id
    
#---------------------------------- Invoice Modules -----------------------------------------------
# invoice model
class Invoice(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    invoice_id = models.CharField(max_length=7, unique=True, editable=False)
    services = models.ManyToManyField(Service) 
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True, blank=True)
    sub_total = models.FloatField(default=0.00)
    discount = models.FloatField(default=0.00)
    total = models.FloatField(default=0.00)
    valid_till = models.DateField()
    invoice_date = models.DateField()
    due_date = models.DateField()
    date_added = models.DateTimeField(auto_now_add=True)
    note = models.TextField(null=True)

    #generate customer_id 
    def save(self, *args, **kwargs):
        if not self.invoice_id:
            prefix = 'IN'
            # Averting race condition using 'select_for_update()'
            with transaction.atomic():
                last_invoice = Invoice.objects.select_for_update().filter(invoice_id__startswith=prefix).order_by('-invoice_id').first()
                if last_invoice:
                    last_id = last_invoice.invoice_id[2:]  # Remove prefix
                    next_id = str(int(last_id) + 1).zfill(4)
                    self.invoice_id = prefix + next_id
                else:
                    self.invoice_id = prefix + '0001'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_id
    
#---------------------------------- Payment Modules -----------------------------------------------
# payment model
class Payment(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=20, null=True, blank=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL , null=True)
    amount = models.FloatField(default=0.00)
    paid_on = models.DateTimeField()
    payment_method = models.CharField(max_length=20, null=True, blank=True)
    receipt = models.FileField(null=True, blank=True, upload_to='payment_receipts/')
    remark = models.TextField(null=True, blank=True)

    #generate customer_id 
    def save(self, *args, **kwargs):
        if not self.trip_id:
            prefix = 'PA'
            # Averting race condition using 'select_for_update()'
            with transaction.atomic():
                last_payment = Payment.objects.select_for_update().filter(payment_id__startswith=prefix).order_by('-payment_id').first()
                if last_payment:
                    last_id = last_payment.payment_id[2:]  # Remove prefix
                    next_id = str(int(last_id) + 1).zfill(4)
                    self.payment_id = prefix + next_id
                else:
                    self.payment_id = prefix + '0001'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice.invoice_id
    
#---------------------------------- Expense & ExpenseCategory Modules ------------------------------
#expense_category model
class Expense_Category(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

# expense model
class Expense(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    expense_id = models.CharField(max_length=7, unique=True, editable=False)
    expense_category = models.ForeignKey(Expense_Category, on_delete=models.SET_NULL, null=True)
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL , null=True)
    amount = models.FloatField()
    paid_to = models.CharField(max_length=20)
    date_paid = models.DateField()
    receipt = models.FileField(blank=True, null=True, upload_to='expense_receipts/')

    #generate customer_id 
    def save(self, *args, **kwargs):
        if not self.expense_id:
            prefix = 'EX'
            # Averting race condition using 'select_for_update()'
            with transaction.atomic():
                last_expense = Expense.objects.select_for_update().filter(expense_id__startswith=prefix).order_by('-expense_id').first()
                if last_expense:
                    last_id = last_expense.expense_id[2:]  # Remove prefix
                    next_id = str(int(last_id) + 1).zfill(4)
                    self.expense_id = prefix + next_id
                else:
                    self.expense_id = prefix + '0001'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.expense_id

#---------------------------------- Reminder Modules -----------------------------------------------
# reminder model
REMINDER_FREQUENCY = (
    ('Weekly','Weekly'),
    ('Monthly','Monthly'),
    ('Yearly','Yearly'),
)
    
REMINDER_STATUS = (
    ('Snoozed','Snoozed'),
    ('Active','Active'),
    ('Overdue','Overdue'),
    ('Due','Due'),
)
class Reminder(models.Model):
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    frequency = models.CharField(max_length=20, choices=REMINDER_FREQUENCY)
    last_date = models.DateField(null=True)
    next_date = models.DateField(null=True)
    status = models.CharField(max_length=20, choices=REMINDER_STATUS)

    def __str__(self):
        return self.name
'''
# Create your models here.
class Repair_Expenses(models.Model):
    pass
'''