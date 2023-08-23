from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime
from django.contrib import messages
from .models import Vehicle, Vehicle_Make, Vehicle_Model, Driver, Customer, Consignee, Shipper, Load, Trip

from . models import (
    Vehicle, 
    Vehicle_Make, 
    Vehicle_Model, 
    Driver, Customer, 
    Consignee, 
    Shipper, 
    Load, 
    Trip,
    Expense,
    Payment,
    Invoice,
    Expense_Category,
    Reminder
)

from .forms import (
    VehicleMakeForm,
    VehicleModelForm,
    VehicleForm, 
    DriverForm, 
    CustomerForm, 
    ConsigneeForm, 
    ShipperForm, 
    LoadForm, 
    TripForm,
    ExpenseForm,
    PaymentForm, 
    ExpenseCategoryForm,
    ReminderForm
)

from truckman.utils import get_user_company





#---------------------------------- Vehicle Make Views------------------------------------------
# add vehicle make
def add_vehicle_make(request):
    company = get_user_company(request) #get request user company
    #instantiate the two kwargs to be able to access them on the forms.py
    #form = VehicleMakeForm(request.POST, company=company) 
    if request.method == 'POST':
        #create instance of vehicle make
        vehicle_make = Vehicle_Make.objects.create(
            company=company,
            name = request.POST.get('name'),
        )

        messages.success(request, f' {vehicle_make.name} was added successfully.')
        return redirect('add_vehicle')

    #redirect
    #context= {'form':form}
    return render(request, 'trip/vehicle-make/add-vehicle-make.html')
#--ends

#---------------------------------- Vehicle Model Views------------------------------------------
# add vehicle model
def add_vehicle_model(request):
    company = get_user_company(request) #get request user company
    #instantiate the two kwargs to be able to access them on the forms.py
    form = VehicleModelForm(request.POST, company=company) 
    if request.method == 'POST':
        make_id = request.POST.get('make')
        make = Vehicle_Make.objects.get(id=make_id)
        #create instance of vehicle make
        vehicle_model = Vehicle_Model.objects.create(
            company=company,
            name = request.POST.get('name'),
            make=make
        )

        messages.success(request, f' {vehicle_model.name} was added successfully.')
        return redirect('add_vehicle')

    #redirect
    context= {'form':form}
    return render(request, 'trip/vehicle-model/add-vehicle-model.html', context)
#--ends

#---------------------------------- Vehicle Views------------------------------------------
# add vehicle
def add_vehicle(request):
    company = get_user_company(request) #get request user company
    #instantiate the two kwargs to be able to access them on the forms.py
    form = VehicleForm(request.POST, company=company) 
    vehicle_form = VehicleMakeForm(request.POST)
    vehicle_model_form = VehicleModelForm(request.POST, company=company)
    if request.method == 'POST':
        #get post data
        make_id = request.POST.get('make')
        make = Vehicle_Make.objects.get(id=make_id)
        model_id = request.POST.get('model')
        model= Vehicle_Model.objects.get(id=model_id)

        #create instance of vehicle
        vehicle = Vehicle.objects.create(
            company=company,
            plate_number = request.POST.get('plate_number'),
            trailer_number = request.POST.get('trailer_number'),
            vin = request.POST.get('vin'),
            make=make,
            model=model,
            milage=request.POST.get('milage'),
            color=request.POST.get('color'),
            milage_unit = request.POST.get('milage_unit'),
            insurance_expiry = request.POST.get('insurance_expiry'),
            manufacture_year = request.POST.get('manufacture_year'),
            purchase_year = request.POST.get('purchase_year'),
            condition = request.POST.get('condition'),
            notes = request.POST.get('notes'),
            truck_image = request.FILES.get('truck_image'),
            trailer_image = request.FILES.get('trailer_image'),
            truck_logbook = request.FILES.get('truck_logbook'),
            trailer_logbook = request.FILES.get('trailer_logbook'),
            good_transit_licence = request.FILES.get('good_transit_licence'),
        )

        messages.success(request, f'Vehicle {vehicle.plate_number} was added successfully.')
        return redirect('list_vehicles')
    context= {
        'form':form,
        'vehicle_form':vehicle_form,
        'vehicle_model_form':vehicle_model_form
        }
    return render(request, 'trip/vehicle/add-vehicle.html', context)
#--ends

# update vehicle
def update_vehicle(request, pk):
    company = get_user_company(request) #get request user company
    vehicle = Vehicle.objects.get(id=pk, company=company)
    #instantiate the two kwargs to be able to access them on the forms.py
    #form = VehicleForm(request.POST, company=company) 
    if request.method == 'POST':
        #get post data
        make_id = request.POST.get('make')
        make = Vehicle_Make.objects.get(id=make_id)
        model_id = request.POST.get('model')
        model= Vehicle_Model.objects.get(id=model_id)

        #update instance 
        vehicle.company=company
        vehicle.plate_number = request.POST.get('plate_number')
        vehicle.trailer_number = request.POST.get('trailer_number')
        vehicle.vin = request.POST.get('vin')
        vehicle.make=make
        vehicle.model=model
        vehicle.milage=request.POST.get('milage')
        vehicle.color=request.POST.get('color')
        vehicle.milage_unit = request.POST.get('milage_unit')
        vehicle.insurance_expiry = request.POST.get('insurance_expiry')
        vehicle.manufacture_year = request.POST.get('manufacture_year')
        vehicle.purchase_year = request.POST.get('purchase_year')
        vehicle.condition = request.POST.get('condition')
        vehicle.notes = request.POST.get('notes')
        vehicle.truck_image = request.FILES.get('truck_image')
        vehicle.trailer_image = request.FILES.get('trailer_image')
        vehicle.truck_logbook = request.FILES.get('truck_logbook')
        vehicle.trailer_logbook = request.FILES.get('trailer_logbook')
        vehicle.good_transit_licence = request.FILES.get('good_transit_licence')
        vehicle.save()
        
        messages.success(request, f'Vehicle {vehicle.plate_number} was edited successfully.')
        return redirect('list_vehicles')
    else:
        # prepopulate the form with existing data
        form_data = {
            'plate_number': vehicle.plate_number,
            'trailer_number': vehicle.trailer_number,
            'vin': vehicle.vin,
            'make': vehicle.make,
            'model': vehicle.model,
            'milage': vehicle.milage,
            'milage_unit': vehicle.milage_unit,
            'insurance_expiry': vehicle.insurance_expiry,
            'manufacture_year': vehicle.manufacture_year,
            'purchase_year': vehicle.purchase_year,
            'condition': vehicle.condition,
            'notes': vehicle.notes,
            'truck_image': vehicle.truck_image,
            'trailer_image': vehicle.trailer_image,
            'truck_logbook': vehicle.truck_logbook,
            'trailer_logbook': vehicle.trailer_logbook,
            'good_transit_licence': vehicle.good_transit_licence,
        }

        form = VehicleForm(initial=form_data, company=company )
        return render(request,'trip/vehicle/update-vehicle.html',{'form':form})
#--ends

#vehicle list
def list_vehicles(request):
    vehicles = Vehicle.objects.filter(company=get_user_company(request))
    context = {'vehicles':vehicles}
    return render(request, 'trip/vehicle/vehicle-list.html', context)
#--ends

#view vehicle
def view_vehicle(request, pk):
    vehicle = Vehicle.objects.get(id=pk, company=get_user_company(request))
    context={'vehicle':vehicle}
    return render(request, 'trip/vehicle/view-vehicle.html', context)
#--ends

# remove vehicle
def remove_vehicle(request, pk):
    if request.method == 'POST':
        vehicle = Vehicle.objects.get(id=pk, company=get_user_company(request))
        vehicle.delete()
        messages.success(request, f'Vehicle {vehicle.plate_number} removed')
        return redirect('list_vehicles')
#--ends

#---------------------------------- Driver views------------------------------------------

# add driver
def add_driver(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = DriverForm(request.POST, company=company) 
    if request.method == 'POST':
        assigned_driver_id  = request.POST.get('assigned_vehicle')
        assigned_vehicle = Vehicle.objects.get(id=assigned_driver_id, company=get_user_company(request))

        #create instance of a driver
        driver = Driver.objects.create(
            #personal data
            company=company,
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            id_no = request.POST.get('id_no'),
            tel_home = request.POST.get('tel_home'),
            tel_roam = request.POST.get('tel_roam'),
            date_hired = request.POST.get('date_hired'),
            driver_photo = request.FILES.get('driver_photo'),
            id_img = request.FILES.get('id_img'),
            #passport and dl data
            dl_no = request.POST.get('dl_no'),
            dl_issuing_authority = request.POST.get('dl_issuing_authority'),
            dl_front_img = request.FILES.get('dl_front_img'),
            dl_back_img = request.FILES.get('dl_back_img'),
            passport_number = request.POST.get('passport_number'),
            passport_image = request.FILES.get('passport_image'),
            #next of kin
            emergency_contact_person = request.POST.get('emergency_contact_person'),
            emergency_contact_person_rlshp = request.POST.get('emergency_contact_person_rlshp'),
            emergency_contact_no = request.POST.get('emergency_contact_no'),
            emergency_contact_two = request.POST.get('emergency_contact_two'),
            assigned_vehicle = assigned_vehicle,
        )

        messages.success(request, f'Driver was added successfully.')
        return redirect('list_drivers')

    context= {'form':form}
    return render(request, 'trip/driver/add-driver.html', context)
#--ends

# update driver
def update_driver(request, pk):
    company = get_user_company(request) #get request user company
    driver = Driver.objects.get(id=pk, company=company)
    if request.method == 'POST':
        assigned_driver_id  = request.POST.get('assigned_vehicle')
        assigned_vehicle = Vehicle.objects.get(id=assigned_driver_id, company=get_user_company(request))
        #update instance 
        driver.company=company
        driver.first_name = request.POST.get('first_name')
        driver.last_name = request.POST.get('last_name')
        driver.id_no = request.POST.get('id_no')
        driver.tel_home = request.POST.get('tel_home')
        driver.tel_roam = request.POST.get('tel_roam')
        driver.date_hired = request.POST.get('date_hired')
        driver.driver_photo = request.FILES.get('driver_photo')
        driver.id_img = request.FILES.get('id_img')

        driver.dl_no = request.POST.get('dl_no')
        driver.passport_number = request.POST.get('passport_number')
        driver.dl_issuing_authority = request.POST.get('dl_issuing_authority')
        driver.dl_front_img = request.FILES.get('dl_front_img')
        driver.dl_back_img = request.FILES.get('dl_back_img')
        driver.passport_image = request.FILES.get('passport_image')
       
        driver.emergency_contact_person = request.POST.get('emergency_contact_person')
        driver.emergency_contact_person_rlshp = request.POST.get('emergency_contact_person_rlshp')
        driver.emergency_contact_no = request.POST.get('emergency_contact_no')
        driver.emergency_contact_two = request.POST.get('emergency_contact_two')
        driver.assigned_vehicle = assigned_vehicle
        driver.save()
        
        messages.success(request, f'Driver details edited successfully.')
        return redirect('list_drivers')
    else:
        # prepopulate the form with existing data
        form_data = {
            'first_name': driver.first_name,
            'last_name': driver.last_name,
            'id_no': driver.id_no,
            'tel_home': driver.tel_home,
            'tel_roam': driver.tel_roam,
            'date_hired': driver.date_hired,
            'driver_photo': driver.driver_photo,
            'id_img': driver.id_img,

            'dl_no': driver.dl_no,
            'passport_number': driver.passport_number,
            'dl_issuing_authority':driver.dl_issuing_authority,
            'dl_front_img':driver.dl_front_img,
            'dl_back_img':driver.dl_back_img,
            'passport_image':driver.passport_image,
            
            'emergency_contact_person': driver.emergency_contact_person,
            'emergency_contact_person_rlshp': driver.emergency_contact_person_rlshp,
            'emergency_contact_no': driver.emergency_contact_no,
            'emergency_contact_two': driver.emergency_contact_two,
            'assigned_vehicle': driver.assigned_vehicle,
        }

        form = DriverForm(initial=form_data, company=company )
        context = {
            'driver':driver,
            'form':form
        }
        return render(request,'trip/driver/update-driver.html', context)
#--ends

#drivers list
def list_drivers(request):
    drivers = Driver.objects.filter(company=get_user_company(request))
    number_of_driver = drivers.count()
    context = {
        'drivers':drivers,
        'number_of_driver':number_of_driver
    }
    return render(request, 'trip/driver/drivers-list.html', context)
#--ends

#view driver
def view_driver(request, pk):
    driver = Driver.objects.get(id=pk, company=get_user_company(request))
    context={'driver':driver}
    return render(request, 'trip/driver/view-driver.html', context)
#--ends

# remove driver
def remove_driver(request, pk):
    if request.method == 'POST':
        driver = Driver.objects.get(id=pk, company=get_user_company(request))
        driver.delete()
        messages.success(request, f'Driver {driver.first_name} removed')
        return redirect('list_drivers')
#--ends

#---------------------------------- Customer views------------------------------------------

# add customer
def add_customer(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = CustomerForm(request.POST) 
    if request.method == 'POST':
        #create instance of a customer
        customer = Customer.objects.create(
            company=company,
            name = request.POST.get('name'),
            contact_person = request.POST.get('contact_person'),
            phone = request.POST.get('phone'),
            email = request.POST.get('email'),
            address_one = request.POST.get('address_one'),
            address_two = request.POST.get('address_two'),
            country = request.POST.get('country'),
            city = request.POST.get('city'),
            website = request.POST.get('website'),
            credit_limit = request.POST.get('credit_limit'),
            payment_term = request.POST.get('payment_term'),
            logo = request.FILES.get('logo'),
        )

        messages.success(request, f'Customer was added successfully.')
        return redirect('list_customers')

    context= {'form':form}
    return render(request, 'trip/customer/add-customer.html', context)
#--ends

# update customer
def update_customer(request, pk):
    company = get_user_company(request) #get request user company
    customer = Customer.objects.get(id=pk, company=company)
    if request.method == 'POST':
        #update instance 
        customer.company=company
        customer.name = request.POST.get('name')
        customer.contact_person = request.POST.get('contact_person')
        customer.phone = request.POST.get('phone')
        customer.email = request.POST.get('email')
        customer.address_one = request.POST.get('address_one')
        customer.address_two = request.POST.get('address_two')
        customer.country = request.POST.get('country')
        customer.city = request.POST.get('city')
        customer.website = request.POST.get('website')
        customer.credit_limit = request.POST.get('credit_limit')
        customer.payment_term = request.POST.get('payment_term')
        customer.logo = request.FILES.get('logo')
        customer.save()
        
        messages.success(request, f'Customer details edited successfully.')
        return redirect('list_customers')
    else:
        # prepopulate the form with existing data
        form_data = {
            'name': customer.name,
            'contact_person': customer.contact_person,
            'phone': customer.phone,
            'email': customer.email,
            'address_one': customer.address_one,
            'address_two': customer.address_two,
            'country': customer.country,
            'city': customer.city,
            'website': customer.website,
            'credit_limit': customer.credit_limit,
            'payment_term': customer.payment_term,
            'logo': customer.logo,
        }

        form = CustomerForm(initial=form_data)
        context = {
            'customer':customer,
            'form':form
        }
        return render(request,'trip/customer/update-customer.html', context)
#--ends

#customers list
def list_customers(request):
    customers = Customer.objects.filter(company=get_user_company(request))
    number_of_customers = customers.count()
    context = {
        'customers':customers,
        'number_of_customers':number_of_customers
    }
    return render(request, 'trip/customer/customers-list.html', context)
#--ends

#view customer
def view_customer(request, pk):
    customer = Customer.objects.get(id=pk, company=get_user_company(request))
    context={'customer':customer}
    return render(request, 'trip/customer/view-customer.html', context)
#--ends

# remove customer
def remove_customer(request, pk):
    if request.method == 'POST':
        customer = Customer.objects.get(id=pk, company=get_user_company(request))
        customer.delete()
        messages.success(request, f'Customer {customer.first_name} removed')
        return redirect('list_customers')
#--ends

#---------------------------------- Consignee views------------------------------------------
# add consignee
def add_consignee(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = ConsigneeForm(request.POST) 
    if request.method == 'POST':
        #create instance of a driver
        consignee = Consignee.objects.create(
            company=company,
            name = request.POST.get('name'),
            contact_person = request.POST.get('contact_person'),
            phone = request.POST.get('phone'),
            email = request.POST.get('email'),
            address_one = request.POST.get('address_one'),
            address_two = request.POST.get('address_two'),
            country = request.POST.get('country'),
            city = request.POST.get('city'),
            website = request.POST.get('website'),
            logo = request.FILES.get('logo'),
        )

        messages.success(request, f'Consignee was added successfully. You can now add a load here.')
        return redirect('add_load') #redirect a user to add load

    context= {'form':form}
    return render(request, 'trip/consignee/add-consignee.html', context)
#--ends

# update consignee
def update_consignee(request, pk):
    company = get_user_company(request) #get request user company
    consignee = Consignee.objects.get(id=pk, company=company)
    if request.method == 'POST':
        #update instance 
        consignee.company=company
        consignee.name = request.POST.get('name')
        consignee.contact_person = request.POST.get('contact_person')
        consignee.phone = request.POST.get('phone')
        consignee.email = request.POST.get('email')
        consignee.address_one = request.POST.get('address_one')
        consignee.address_two = request.POST.get('address_two')
        consignee.country = request.POST.get('country')
        consignee.city = request.POST.get('city')
        consignee.website = request.POST.get('website')
        consignee.logo = request.FILES.get('logo')
        consignee.save()
        
        messages.success(request, f'Consignee details updated successfully.')
        return redirect('list_consignees')
    else:
        # prepopulate the form with existing data
        form_data = {
            'name': consignee.name,
            'contact_person': consignee.contact_person,
            'phone': consignee.phone,
            'email': consignee.email,
            'address_one': consignee.address_one,
            'address_two': consignee.address_two,
            'country': consignee.country,
            'city': consignee.city,
            'website': consignee.website,
            'logo': consignee.logo,
        }

        form = ConsigneeForm(initial=form_data )
        context = {
            'consignee':consignee,
            'form':form
        }
        return render(request,'trip/consignee/update-consignee.html', context)
#--ends

#consignees list
def list_consignees(request):
    consignees = Consignee.objects.filter(company=get_user_company(request))
    number_of_consignees = consignees.count()
    context = {
        'consignees':consignees,
        'number_of_consignees':number_of_consignees
    }
    return render(request, 'trip/consignee/consignees-list.html', context)
#--ends

#view consignee
def view_consignee(request, pk):
    consignee = Consignee.objects.get(id=pk, company=get_user_company(request))
    context={'consignee':consignee}
    return render(request, 'trip/consignee/view-consignee.html', context)
#--ends

# remove consignee
def remove_consignee(request, pk):
    if request.method == 'POST':
        consignee = Consignee.objects.get(id=pk, company=get_user_company(request))
        consignee.delete()
        messages.success(request, f'Consignee {consignee.name} removed')
        return redirect('list_consignees')
#--ends

#---------------------------------- Shipper views------------------------------------------
# add shipper
def add_shipper(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = ShipperForm(request.POST) 
    if request.method == 'POST':
        #create instance of a driver
        shipper = Shipper.objects.create(
            company=company,
            name = request.POST.get('name'),
            contact_person = request.POST.get('contact_person'),
            phone = request.POST.get('phone'),
            email = request.POST.get('email'),
            address_one = request.POST.get('address_one'),
            address_two = request.POST.get('address_two'),
            country = request.POST.get('country'),
            city = request.POST.get('city'),
            website = request.POST.get('website'),
            logo = request.FILES.get('logo'),
        )

        messages.success(request, f'Shipper was added successfully. You can now add a Consignee here.')
        return redirect('add_consignee') #redirect a user to add consignee

    context= {'form':form}
    return render(request, 'trip/shipper/add-shipper.html', context)
#--ends

# update shipper
def update_shipper(request, pk):
    company = get_user_company(request) #get request user company
    shipper = Shipper.objects.get(id=pk, company=company)
    if request.method == 'POST':
        #update instance 
        shipper.company=company
        shipper.name = request.POST.get('name')
        shipper.contact_person = request.POST.get('contact_person')
        shipper.phone = request.POST.get('phone')
        shipper.email = request.POST.get('email')
        shipper.address_one = request.POST.get('address_one')
        shipper.address_two = request.POST.get('address_two')
        shipper.country = request.POST.get('country')
        shipper.city = request.POST.get('city')
        shipper.website = request.POST.get('website')
        shipper.logo = request.FILES.get('logo')
        shipper.save()
        
        messages.success(request, f'Shipper details updated successfully.')
        return redirect('list_shippers')
    else:
        # prepopulate the form with existing data
        form_data = {
            'name': shipper.name,
            'contact_person': shipper.contact_person,
            'phone': shipper.phone,
            'email': shipper.email,
            'address_one': shipper.address_one,
            'address_two': shipper.address_two,
            'country': shipper.country,
            'city': shipper.city,
            'website': shipper.website,
            'logo': shipper.logo,
        }

        form = ShipperForm(initial=form_data )
        context = {
            'shipper':shipper,
            'form':form
        }
        return render(request,'trip/shipper/update-shipper.html', context)
#--ends

#shippers list
def list_shippers(request):
    shippers = Shipper.objects.filter(company=get_user_company(request))
    number_of_shippers = shippers.count()
    context = {
        'shippers':shippers,
        'number_of_shippers':number_of_shippers
    }
    return render(request, 'trip/shipper/shippers-list.html', context)
#--ends

#view shipper
def view_shipper(request, pk):
    shipper = Shipper.objects.get(id=pk, company=get_user_company(request))
    context={'shipper':shipper}
    return render(request, 'trip/shipper/view-shipper.html', context)
#--ends

# remove shipper
def remove_shipper(request, pk):
    if request.method == 'POST':
        shipper = Shipper.objects.get(id=pk, company=get_user_company(request))
        shipper.delete()
        messages.success(request, f'Shipper {shipper.name} removed')
        return redirect('list_shippers')
#--ends

#---------------------------------- Load views------------------------------------------
# add load
def add_load(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = LoadForm(request.POST, company=company) 
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        customer = Customer.objects.get(company=company, id=customer_id)

        shipper_id = request.POST.get('shipper')
        shipper = Shipper.objects.get(company=company, id=shipper_id)

        consignee_id = request.POST.get('consignee')
        consignee = Consignee.objects.get(company=company, id=consignee_id)

        #create instance of a driver
        load = Load.objects.create(
            company=company,
            customer = customer,
            shipper = shipper,
            consignee = consignee,
            weight = request.POST.get('weight'),
            pickup_date = request.POST.get('pickup_date'),
            delivery_date = request.POST.get('delivery_date'),
            quantity = request.POST.get('quantity'),
            quantity_type = request.POST.get('quantity_type'),
            commodity = request.POST.get('commodity'),
            driver_instructions = request.POST.get('driver_instructions'),
            primary_fee = request.POST.get('primary_fee'),
            primary_fee_type = request.POST.get('primary_fee_type'),
            fuel_surcharge_fee = request.POST.get('fuel_surcharge_fee'),
            fsc_amount_type = request.POST.get('fsc_amount_type'),
            border_agent_fee = request.POST.get('border_agent_fee'),
            road_user = request.POST.get('road_user'),
            gate_tolls = request.POST.get('gate_tolls'),
            fines = request.POST.get('fines'),
            additional_fees = request.POST.get('additional_fees'),
            invoice_advance = request.POST.get('invoice_advance'),
            legal_disclaimer = request.POST.get('legal_disclaimer'),
            notes = request.POST.get('notes'),
        )

        messages.success(request, f'Load was added successfully.You can now add a Trip here.')
        return redirect('add_trip')

    context= {'form':form}
    return render(request, 'trip/load/add-load.html', context)
#--ends

# update load
def update_load(request, pk):
    company = get_user_company(request) #get request user company
    load = Load.objects.get(id=pk, company=company)
    if request.method == 'POST':

        customer_id = request.POST.get('customer')
        customer = Customer.objects.get(company=company, id=customer_id)

        shipper_id = request.POST.get('shipper')
        shipper = Shipper.objects.get(company=company, id=shipper_id)

        consignee_id = request.POST.get('consignee')
        consignee = Consignee.objects.get(company=company, id=consignee_id)

        #update instance 
        load.company = company
        load.customer = customer
        load.shipper = shipper
        load.consignee = consignee
        load.pickup_date = request.POST.get('pickup_date')
        load.weight = request.POST.get('weight')
        load.delivery_date = request.POST.get('delivery_date')
        load.quantity = request.POST.get('quantity')
        load.quantity_type = request.POST.get('quantity_type')
        load.commodity = request.POST.get('commodity')
        load.driver_instructions = request.POST.get('driver_instructions')
        load.primary_fee = request.POST.get('primary_fee')
        load.primary_fee_type = request.POST.get('primary_fee_type')
        load.fuel_surcharge_fee = request.POST.get('fuel_surcharge_fee')
        load.fsc_amount_type = request.POST.get('fsc_amount_type')
        load.border_agent_fee = request.POST.get('border_agent_fee')
        load.road_user = request.POST.get('road_user')
        load.gate_tolls = request.POST.get('gate_tolls')
        load.fines = request.POST.get('fines')
        load.additional_fees = request.POST.get('additional_fees')
        load.invoice_advance = request.POST.get('invoice_advance')
        load.legal_disclaimer = request.POST.get('legal_disclaimer')
        load.notes = request.POST.get('notes')
        
        load.save()
        
        messages.success(request, f'Load details updated successfully.')
        return redirect('view_load', load.id)
    else:
        # prepopulate the form with existing data
        form_data = {
            'customer': load.customer,
            'shipper': load.shipper,
            'consignee': load.consignee,
            'pickup_date': load.pickup_date,
            'weight': load.weight,
            'delivery_date': load.delivery_date,
            'quantity': load.quantity,
            'quantity_type': load.quantity_type,
            'driver_instructions': load.driver_instructions,
            'commodity': load.commodity,
            'primary_fee': load.primary_fee,
            'primary_fee_type': load.primary_fee_type,
            'fuel_surcharge_fee': load.fuel_surcharge_fee,
            'border_agent_fee': load.border_agent_fee,
            'road_user': load.road_user,
            'gate_tolls': load.gate_tolls,
            'fines': load.fines,
            'additional_fees': load.additional_fees,
            'invoice_advance': load.invoice_advance,
            'legal_disclaimer': load.legal_disclaimer,
            'notes': load.notes,
            
        }

        form = LoadForm(initial=form_data, company=company )
        context = {
            'load':load,
            'form':form
        }
        return render(request,'trip/load/update-load.html', context)
#--ends

#loads list
def list_loads(request):
    loads = Load.objects.filter(company=get_user_company(request))
    number_of_loads = loads.count()
    context = {
        'loads':loads,
        'number_of_loads':number_of_loads
    }
    return render(request, 'trip/load/loads-list.html', context)
#--ends

#view load
def view_load(request, pk):
    load = Load.objects.get(id=pk, company=get_user_company(request))
    context={'load':load}
    return render(request, 'trip/load/view-load.html', context)
#--ends

# remove load
def remove_load(request, pk):
    if request.method == 'POST':
        load = Load.objects.get(id=pk, company=get_user_company(request))
        load.delete()
        messages.success(request, f'Load of ID: {load.load_id} removed')
        return redirect('list_loads')
#--ends

#---------------------------------- Trip views------------------------------------------
# add trip
def add_trip(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = TripForm(request.POST, company=company) 
    if request.method == 'POST':

        load_id = request.POST.get('load')
        load = Load.objects.get(company=company, id=load_id)


        vehicle_id = request.POST.get('vehicle')
        vehicle = Vehicle.objects.get(company=company, id=vehicle_id)

        #create instance of a trip
        trip = Trip.objects.create(
            company=company,
            load = load,
            vehicle = vehicle,
            driver_accesory_pay = request.POST.get('driver_accesory_pay'),
            vehicle_odemeter = request.POST.get('vehicle_odemeter'),
            driver_advance = request.POST.get('driver_advance'),
            driver_milage = request.POST.get('driver_advance'),
        )

        messages.success(request, f'Trip was added successfully.')
        return redirect('view_trip', trip.id)

    context= {
        'form':form,
    }
    return render(request, 'trip/trip/add-trip.html', context)
#--ends

# update trip
def update_trip(request, pk):
    company = get_user_company(request) #get request user company
    trip = Trip.objects.get(id=pk, company=company)
    if request.method == 'POST':

        load_id = request.POST.get('load')
        load = Load.objects.get(company=company, id=load_id)

        vehicle_id = request.POST.get('vehicle')
        vehicle = Vehicle.objects.get(company=company, id=vehicle_id)
        #update instance 
        trip.company = company
        trip.load = load
        trip.vehicle = vehicle
        trip.driver_accesory_pay = request.POST.get('driver_accesory_pay')
        trip.vehicle_odemeter = request.POST.get('vehicle_odemeter')
        trip.driver_advance = request.POST.get('driver_advance')
        trip.driver_milage = request.POST.get('driver_milage')
        trip.save()
        
        messages.success(request, f'Trip details updated successfully.')
        return redirect('view_trip', trip.id)
    else:
        # prepopulate the form with existing data
        form_data = {
            'load': trip.load,
            'vehicle': trip.vehicle,
            'driver_accesory_pay': trip.driver_accesory_pay,
            'vehicle_odemeter': trip.vehicle_odemeter,
            'driver_advance': trip.driver_advance,
            'driver_milage': trip.driver_milage,
        }

        form = TripForm(initial=form_data, company=company )
        context = {
            'trip':trip,
            'form':form
        }
        return render(request,'trip/trip/update-trip.html', context)
#--ends

#trip list
def list_trips(request):
    trips = Trip.objects.filter(company=get_user_company(request))
    number_of_trips = trips.count()
    context = {
        'trips':trips,
        'number_of_trips':number_of_trips
    }
    return render(request, 'trip/trip/trips-list.html', context)
#--ends

#view trip
def view_trip(request, pk):
    trip = Trip.objects.get(id=pk, company=get_user_company(request))
    context={'trip':trip}
    return render(request, 'trip/trip/view-trip.html', context)
#--ends

# remove trip
def remove_trip(request, pk):
    if request.method == 'POST':
        trip = Trip.objects.get(id=pk, company=get_user_company(request))
        trip.delete()
        messages.success(request, f'Trip of id : {trip.trip_id} removed')
        return redirect('list_trips')
#--ends

#---------------------------------- Payment views------------------------------------------

# add payment
def add_payment(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = PaymentForm(request.POST, company=company) 
    if request.method == 'POST':

        invoice_id = request.POST.get('invoice')
        invoice = Invoice.objects.get(company=company, id=invoice_id)

        #create instance of a payment
        payment = Payment.objects.create(
            company=company,
            transaction_id = request.POST.get('transaction_id'),
            invoice = invoice,
            amount = request.POST.get('amount'),
            paid_on = request.POST.get('paid_on'),
            payment_method = request.POST.get('payment_method'),
            remark = request.POST.get('remark'),
        )

        messages.success(request, f'Payment was added successfully.')
        return redirect('list_payments')

    context= {
        'form':form,
    }
    return render(request, 'trip/payment/payment-list.html', context)
#--ends

# update trip
def update_payment(request, pk):
    company = get_user_company(request) #get request user company
    trip = Trip.objects.get(id=pk, company=company)
    if request.method == 'POST':

        load_id = request.POST.get('load')
        load = Load.objects.get(company=company, id=load_id)

        driver_id = request.POST.get('driver')
        driver = Driver.objects.get(company=company, id=driver_id)

        vehicle_id = request.POST.get('vehicle')
        vehicle = Vehicle.objects.get(company=company, id=vehicle_id)
        #update instance 
        trip.company = company
        trip.driver = driver
        trip.load = load
        trip.vehicle = vehicle
        trip.driver_accesory_pay = request.POST.get('driver_accesory_pay')
        trip.vehicle_odemeter = request.POST.get('vehicle_odemeter')
        trip.driver_advance = request.POST.get('driver_advance')
        trip.save()
        
        messages.success(request, f'Trip details updated successfully.')
        return redirect('view_trip', trip.id)
    else:
        # prepopulate the form with existing data
        form_data = {
            'driver': trip.driver,
            'load': trip.load,
            'vehicle': trip.vehicle,
            'driver_accesory_pay': trip.driver_accesory_pay,
            'vehicle_odemeter': trip.vehicle_odemeter,
            'driver_advance': trip.driver_advance
        }

        form = TripForm(initial=form_data, company=company )
        context = {
            'trip':trip,
            'form':form
        }
        return render(request,'trip/trip/update-trip.html', context)
#--ends

#trip list
def list_payments(request):
    payments = Payment.objects.filter(company=get_user_company(request))
    form = PaymentForm(request.POST, company=get_user_company(request)) 
    context = {
        'payments':payments,
        'form':form,
    }
    return render(request, 'trip/payment/payment-list.html', context)
#--ends

#view trip
def view_payment(request, pk):
    trip = Trip.objects.get(id=pk, company=get_user_company(request))
    context={'trip':trip}
    return render(request, 'trip/trip/view-trip.html', context)
#--ends

# remove trip
def remove_payment(request, pk):
    if request.method == 'POST':
        trip = Trip.objects.get(id=pk, company=get_user_company(request))
        trip.delete()
        messages.success(request, f'Trip of id : {trip.trip_id} removed')
        return redirect('list_trips')
#--ends

#---------------------------------- Expense Category views------------------------------------------

# add expense category
def add_expense_category(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = ExpenseCategoryForm(request.POST) 
    if request.method == 'POST':

        #create instance of a driver
        category = Expense_Category.objects.create(
            company=company,
            name = request.POST.get('name')
        )
        messages.success(request, f'Expense category was added successfully.')
        return redirect('list_expenses')

    return redirect('list_expenses')
#--ends


#expense category list
def list_expenses_categories(request):
    expenses = Expense.objects.filter(company=get_user_company(request))
    form = ExpenseForm(request.POST, company=get_user_company(request)) 
    category_form = ExpenseCategoryForm(request.POST)
    context = {
        'expenses':expenses,
        'form':form,
        'category_form':category_form
       }
    return render(request, 'trip/expense/expense-list.html', context)
#--ends

# remove expense category
def remove_expense_category(request, pk):
    if request.method == 'POST':
        trip = Trip.objects.get(id=pk, company=get_user_company(request))
        trip.delete()
        messages.success(request, f'Trip of id : {trip.trip_id} removed')
        return redirect('list_trips')
#--ends

#---------------------------------- Expense views------------------------------------------

# add expense
def add_expense(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = ExpenseForm(request.POST, company=company) 
    if request.method == 'POST':

        trip_id = request.POST.get('trip')
        trip = Trip.objects.get(company=company, id=trip_id)

        expense_category_id = request.POST.get('expense_category')
        expense_category = Expense_Category.objects.get(company=company, id=expense_category_id)

        #create instance of a driver
        expense = Expense.objects.create(
            company=company,
            trip = trip,
            expense_category = expense_category,
            amount = request.POST.get('amount'),
            date_paid = request.POST.get('date_paid'),
            paid_to = request.POST.get('paid_to'),
            receipt = request.FILES.get('receipt'),
        )

        messages.success(request, f'Expense was added successfully.')
        return redirect('list_expenses')

    context= {
        'form':form,
    }
    return render(request, 'trip/expense/expense-list.html', context)
#--ends

# update trip
def update_expense(request, pk):
    company = get_user_company(request) #get request user company
    trip = Trip.objects.get(id=pk, company=company)
    if request.method == 'POST':

        load_id = request.POST.get('load')
        load = Load.objects.get(company=company, id=load_id)

        driver_id = request.POST.get('driver')
        driver = Driver.objects.get(company=company, id=driver_id)

        vehicle_id = request.POST.get('vehicle')
        vehicle = Vehicle.objects.get(company=company, id=vehicle_id)
        #update instance 
        trip.company = company
        trip.driver = driver
        trip.load = load
        trip.vehicle = vehicle
        trip.driver_accesory_pay = request.POST.get('driver_accesory_pay')
        trip.vehicle_odemeter = request.POST.get('vehicle_odemeter')
        trip.driver_advance = request.POST.get('driver_advance')
        trip.save()
        
        messages.success(request, f'Trip details updated successfully.')
        return redirect('view_trip', trip.id)
    else:
        # prepopulate the form with existing data
        form_data = {
            'driver': trip.driver,
            'load': trip.load,
            'vehicle': trip.vehicle,
            'driver_accesory_pay': trip.driver_accesory_pay,
            'vehicle_odemeter': trip.vehicle_odemeter,
            'driver_advance': trip.driver_advance
        }

        form = TripForm(initial=form_data, company=company )
        context = {
            'trip':trip,
            'form':form
        }
        return render(request,'trip/trip/update-trip.html', context)
#--ends

#trip list
def list_expenses(request):
    expenses = Expense.objects.filter(company=get_user_company(request))
    form = ExpenseForm(request.POST, company=get_user_company(request)) 
    category_form = ExpenseCategoryForm(request.POST)
    context = {
        'expenses':expenses,
        'form':form,
        'category_form':category_form
       }
    return render(request, 'trip/expense/expense-list.html', context)
#--ends

#view trip
def view_expense(request, pk):
    trip = Trip.objects.get(id=pk, company=get_user_company(request))
    context={'trip':trip}
    return render(request, 'trip/trip/view-trip.html', context)
#--ends

# remove trip
def remove_expense(request, pk):
    if request.method == 'POST':
        trip = Trip.objects.get(id=pk, company=get_user_company(request))
        trip.delete()
        messages.success(request, f'Trip of id : {trip.trip_id} removed')
        return redirect('list_trips')
#--ends

#---------------------------------- Invoice views------------------------------------------
# add invoice
def add_invoice(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = TripForm(request.POST, company=company) 
    if request.method == 'POST':

        load_id = request.POST.get('load')
        load = Load.objects.get(company=company, id=load_id)

        driver_id = request.POST.get('driver')
        driver = Driver.objects.get(company=company, id=driver_id)

        vehicle_id = request.POST.get('vehicle')
        vehicle = Vehicle.objects.get(company=company, id=vehicle_id)

        #create instance of a driver
        trip = Trip.objects.create(
            company=company,
            load = load,
            driver = driver,
            vehicle = vehicle,
            driver_accesory_pay = request.POST.get('driver_accesory_pay'),
            vehicle_odemeter = request.POST.get('vehicle_odemeter'),
            driver_advance = request.POST.get('driver_advance'),
        )

        messages.success(request, f'Trip was added successfully.')
        return redirect('view_trip', trip.id)

    context= {
        'form':form,
    }
    return render(request, 'trip/trip/add-trip.html', context)
#--ends

# update trip
def update_invoice(request, pk):
    company = get_user_company(request) #get request user company
    trip = Trip.objects.get(id=pk, company=company)
    if request.method == 'POST':

        load_id = request.POST.get('load')
        load = Load.objects.get(company=company, id=load_id)

        driver_id = request.POST.get('driver')
        driver = Driver.objects.get(company=company, id=driver_id)

        vehicle_id = request.POST.get('vehicle')
        vehicle = Vehicle.objects.get(company=company, id=vehicle_id)
        #update instance 
        trip.company = company
        trip.driver = driver
        trip.load = load
        trip.vehicle = vehicle
        trip.driver_accesory_pay = request.POST.get('driver_accesory_pay')
        trip.vehicle_odemeter = request.POST.get('vehicle_odemeter')
        trip.driver_advance = request.POST.get('driver_advance')
        trip.save()
        
        messages.success(request, f'Trip details updated successfully.')
        return redirect('view_trip', trip.id)
    else:
        # prepopulate the form with existing data
        form_data = {
            'driver': trip.driver,
            'load': trip.load,
            'vehicle': trip.vehicle,
            'driver_accesory_pay': trip.driver_accesory_pay,
            'vehicle_odemeter': trip.vehicle_odemeter,
            'driver_advance': trip.driver_advance
        }

        form = TripForm(initial=form_data, company=company )
        context = {
            'trip':trip,
            'form':form
        }
        return render(request,'trip/trip/update-trip.html', context)
#--ends

#trip list
def list_invoices(request):
    trips = Trip.objects.filter(company=get_user_company(request))
    number_of_trips = trips.count()
    context = {
        'trips':trips,
        'number_of_trips':number_of_trips
    }
    return render(request, 'trip/trip/trips-list.html', context)
#--ends

#view trip
def view_invoice(request, pk):
    trip = Trip.objects.get(id=pk, company=get_user_company(request))
    context={'trip':trip}
    return render(request, 'trip/trip/view-trip.html', context)
#--ends

# remove trip
def remove_invoice(request, pk):
    if request.method == 'POST':
        trip = Trip.objects.get(id=pk, company=get_user_company(request))
        trip.delete()
        messages.success(request, f'Trip of id : {trip.trip_id} removed')
        return redirect('list_trips')
#--ends

#---------------------------------- Estimate views------------------------------------------

# add estimate
def add_estimate(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = TripForm(request.POST, company=company) 
    if request.method == 'POST':

        load_id = request.POST.get('load')
        load = Load.objects.get(company=company, id=load_id)

        driver_id = request.POST.get('driver')
        driver = Driver.objects.get(company=company, id=driver_id)

        vehicle_id = request.POST.get('vehicle')
        vehicle = Vehicle.objects.get(company=company, id=vehicle_id)

        #create instance of a driver
        trip = Trip.objects.create(
            company=company,
            load = load,
            driver = driver,
            vehicle = vehicle,
            driver_accesory_pay = request.POST.get('driver_accesory_pay'),
            vehicle_odemeter = request.POST.get('vehicle_odemeter'),
            driver_advance = request.POST.get('driver_advance'),
        )

        messages.success(request, f'Trip was added successfully.')
        return redirect('view_trip', trip.id)

    context= {
        'form':form,
    }
    return render(request, 'trip/trip/add-trip.html', context)
#--ends

# update trip
def update_estimate(request, pk):
    company = get_user_company(request) #get request user company
    trip = Trip.objects.get(id=pk, company=company)
    if request.method == 'POST':

        load_id = request.POST.get('load')
        load = Load.objects.get(company=company, id=load_id)

        driver_id = request.POST.get('driver')
        driver = Driver.objects.get(company=company, id=driver_id)

        vehicle_id = request.POST.get('vehicle')
        vehicle = Vehicle.objects.get(company=company, id=vehicle_id)
        #update instance 
        trip.company = company
        trip.driver = driver
        trip.load = load
        trip.vehicle = vehicle
        trip.driver_accesory_pay = request.POST.get('driver_accesory_pay')
        trip.vehicle_odemeter = request.POST.get('vehicle_odemeter')
        trip.driver_advance = request.POST.get('driver_advance')
        trip.save()
        
        messages.success(request, f'Trip details updated successfully.')
        return redirect('view_trip', trip.id)
    else:
        # prepopulate the form with existing data
        form_data = {
            'driver': trip.driver,
            'load': trip.load,
            'vehicle': trip.vehicle,
            'driver_accesory_pay': trip.driver_accesory_pay,
            'vehicle_odemeter': trip.vehicle_odemeter,
            'driver_advance': trip.driver_advance
        }

        form = TripForm(initial=form_data, company=company )
        context = {
            'trip':trip,
            'form':form
        }
        return render(request,'trip/trip/update-trip.html', context)
#--ends

#trip list
def list_estimates(request):
    trips = Trip.objects.filter(company=get_user_company(request))
    number_of_trips = trips.count()
    context = {
        'trips':trips,
        'number_of_trips':number_of_trips
    }
    return render(request, 'trip/trip/trips-list.html', context)
#--ends

#view trip
def view_estimate(request, pk):
    trip = Trip.objects.get(id=pk, company=get_user_company(request))
    context={'trip':trip}
    return render(request, 'trip/trip/view-trip.html', context)
#--ends

# remove trip
def remove_estimate(request, pk):
    if request.method == 'POST':
        trip = Trip.objects.get(id=pk, company=get_user_company(request))
        trip.delete()
        messages.success(request, f'Trip of id : {trip.trip_id} removed')
        return redirect('list_trips')
#--ends

#---------------------------------- Reminder views------------------------------------------

# add reminder
def add_reminder(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = ReminderForm(request.POST, company=company) 
    if request.method == 'POST':

        vehicle_id = request.POST.get('vehicle')
        vehicle = Vehicle.objects.get(company=company, id=vehicle_id)

        current_date = timezone.now().date()
        next_date_str = request.POST.get('next_date')

        # Convert the next_date string to a datetime.date object
        next_date = datetime.strptime(next_date_str, '%Y-%m-%d').date()

        if next_date < current_date:
            status = 'Overdue'
        else:
            status = 'Active'

        #create instance of a reminder
        reminder = Reminder.objects.create(
            company=company,
            vehicle = vehicle,
            name = request.POST.get('name'),
            frequency = request.POST.get('frequency'),
            status = status,
            last_date = request.POST.get('last_date'),
            next_date = request.POST.get('next_date'),
        )

        messages.success(request, f'Reminder was set.')
        return redirect('list_reminders')

    context= {
        'form':form,
    }
    return render(request, 'trip/reminder/reminders-list.html', context)
#--ends

#reminder list
def list_reminders(request):
    company = get_user_company(request)
    reminders = Reminder.objects.filter(company=company)
    number_of_reminders = reminders.count()
    reminder_form = ReminderForm(request.POST, company=company) 
    context = {
        'reminders':reminders,
        'number_of_reminders':number_of_reminders,
        'reminder_form':reminder_form
    }
    return render(request, 'trip/reminder/reminders-list.html', context)
#--ends

# remove reminder
def remove_reminder(request, pk):
    #if request.method == 'POST':
    reminder = Reminder.objects.get(id=pk, company=get_user_company(request))
    reminder.delete()
    messages.success(request, 'Reminder removed')
    return redirect('list_reminders')
#--ends

#---------------------------------- Reminder views------------------------------------------