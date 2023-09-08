from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from truckman.decorators import permission_required
from django.utils import timezone
from datetime import datetime, timedelta
import os
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from authentication.models import Preference

from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from premailer import transform
from premailer import Premailer


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
    Reminder,
    Service,
    Estimate
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
    ReminderForm,
    InvoiceForm,
    EstimateForm
)

from truckman.utils import get_user_company
from truckman.tasks import send_email_task




#---------------------------------- Vehicle Make Views------------------------------------------
# add vehicle make
@login_required(login_url='login')
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
@login_required(login_url='login')
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
@login_required(login_url='login')
@permission_required('trip.add_vehicle')
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
@login_required(login_url='login')
@permission_required('trip.change_vehicle')
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
@login_required(login_url='login')
@permission_required('trip.view_vehicle')
def list_vehicles(request):
    vehicles = Vehicle.objects.filter(company=get_user_company(request))
    context = {'vehicles':vehicles}
    return render(request, 'trip/vehicle/vehicle-list.html', context)
#--ends

#view vehicle
@login_required(login_url='login')
@permission_required('trip.view_vehicle')
def view_vehicle(request, pk):
    vehicle = Vehicle.objects.get(id=pk, company=get_user_company(request))
    context={'vehicle':vehicle}
    return render(request, 'trip/vehicle/view-vehicle.html', context)
#--ends

# remove vehicle
@login_required(login_url='login')
@permission_required('trip.delete_vehicle')
def remove_vehicle(request, pk):
    if request.method == 'POST':
        vehicle = Vehicle.objects.get(id=pk, company=get_user_company(request))
        vehicle.delete()
        messages.success(request, f'Vehicle {vehicle.plate_number} removed')
        return redirect('list_vehicles')
#--ends

#---------------------------------- Driver views------------------------------------------

# add driver
@login_required(login_url='login')
@permission_required('trip.add_driver')
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
@login_required(login_url='login')
@permission_required('trip.change_driver')
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
@login_required(login_url='login')
@permission_required('trip.view_driver')
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
@login_required(login_url='login')
@permission_required('trip.view_driver')
def view_driver(request, pk):
    driver = Driver.objects.get(id=pk, company=get_user_company(request))
    context={'driver':driver}
    return render(request, 'trip/driver/view-driver.html', context)
#--ends

# remove driver
@login_required(login_url='login')
@permission_required('trip.delete_driver')
def remove_driver(request, pk):
    if request.method == 'POST':
        driver = Driver.objects.get(id=pk, company=get_user_company(request))
        driver.delete()
        messages.success(request, f'Driver {driver.first_name} removed')
        return redirect('list_drivers')
#--ends

#---------------------------------- Customer views------------------------------------------

# add customer
@login_required(login_url='login')
@permission_required('trip.add_customer')
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
@login_required(login_url='login')
@permission_required('trip.change_customer')
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
@login_required(login_url='login')
@permission_required('trip.view_customer')
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
@login_required(login_url='login')
@permission_required('trip.view_customer')
def view_customer(request, pk):
    customer = Customer.objects.get(id=pk, company=get_user_company(request))
    context={'customer':customer}
    return render(request, 'trip/customer/view-customer.html', context)
#--ends

# remove customer
@login_required(login_url='login')
@permission_required('trip.delete_customer')
def remove_customer(request, pk):
    if request.method == 'POST':
        customer = Customer.objects.get(id=pk, company=get_user_company(request))
        customer.delete()
        messages.success(request, f'Customer {customer.first_name} removed')
        return redirect('list_customers')
#--ends

#---------------------------------- Consignee views------------------------------------------
# add consignee
@login_required(login_url='login')
@permission_required('trip.add_consignee')
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
@login_required(login_url='login')
@permission_required('trip.change_consignee')
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
@login_required(login_url='login')
@permission_required('trip.view_consignee')
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
@login_required(login_url='login')
@permission_required('trip.view_consignee')
def view_consignee(request, pk):
    consignee = Consignee.objects.get(id=pk, company=get_user_company(request))
    context={'consignee':consignee}
    return render(request, 'trip/consignee/view-consignee.html', context)
#--ends

# remove consignee
@login_required(login_url='login')
@permission_required('trip.delete_consignee')
def remove_consignee(request, pk):
    if request.method == 'POST':
        consignee = Consignee.objects.get(id=pk, company=get_user_company(request))
        consignee.delete()
        messages.success(request, f'Consignee {consignee.name} removed')
        return redirect('list_consignees')
#--ends

#---------------------------------- Shipper views------------------------------------------
# add shipper
@login_required(login_url='login')
@permission_required('trip.add_shipper')
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
@login_required(login_url='login')
@permission_required('trip.change_shipper')
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
@login_required(login_url='login')
@permission_required('trip.view_shipper')
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
@login_required(login_url='login')
@permission_required('trip.view_shipper')
def view_shipper(request, pk):
    shipper = Shipper.objects.get(id=pk, company=get_user_company(request))
    context={'shipper':shipper}
    return render(request, 'trip/shipper/view-shipper.html', context)
#--ends

# remove shipper
@login_required(login_url='login')
@permission_required('trip.delete_shipper')
def remove_shipper(request, pk):
    if request.method == 'POST':
        shipper = Shipper.objects.get(id=pk, company=get_user_company(request))
        shipper.delete()
        messages.success(request, f'Shipper {shipper.name} removed')
        return redirect('list_shippers')
#--ends

#---------------------------------- Load views------------------------------------------
# add load
@login_required(login_url='login')
@permission_required('trip.add_load')
def add_load(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = LoadForm(request.POST, company=company) 
    if request.method == 'POST':
        '''
        customer_id = request.POST.get('customer')
        customer = Customer.objects.get(company=company, id=customer_id)
        '''
        shipper_id = request.POST.get('shipper')
        shipper = Shipper.objects.get(company=company, id=shipper_id)

        consignee_id = request.POST.get('consignee')
        consignee = Consignee.objects.get(company=company, id=consignee_id)

        estimate_id = request.POST.get('estimate')
        estimate = Estimate.objects.get(company=company, id=estimate_id)

        #create instance of a load
        load = Load.objects.create(
            company=company,
            #customer = customer,
            shipper = shipper,
            consignee = consignee,
            estimate = estimate,
            quantity = request.POST.get('quantity'),
            quantity_type = request.POST.get('quantity_type'),
            commodity = request.POST.get('commodity'),
            weight = request.POST.get('weight'),
            quote_amount = request.POST.get('quoteAmount'),
            pickup_date = request.POST.get('pickup_date'),
            delivery_date = request.POST.get('delivery_date'),
            driver_instructions = request.POST.get('driver_instructions'),
            legal_disclaimer = request.POST.get('legal_disclaimer'),
            notes = request.POST.get('notes'),
        )

        messages.success(request, f'Load was added successfully.You can now add a Trip here.')
        return redirect('add_trip')

    context= {'form':form}
    return render(request, 'trip/load/add-load.html', context)
#--ends

# update load
@login_required(login_url='login')
@permission_required('trip.change_load')
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
@login_required(login_url='login')
@permission_required('trip.view_load')
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
@login_required(login_url='login')
@permission_required('trip.view_load')
def view_load(request, pk):
    load = Load.objects.get(id=pk, company=get_user_company(request))
    context={'load':load}
    return render(request, 'trip/load/view-load.html', context)
#--ends

# remove load
@login_required(login_url='login')
@permission_required('trip.delete_load')
def remove_load(request, pk):
    if request.method == 'POST':
        load = Load.objects.get(id=pk, company=get_user_company(request))
        load.delete()
        messages.success(request, f'Load of ID: {load.load_id} removed')
        return redirect('list_loads')
#--ends

#---------------------------------- Trip views------------------------------------------
# add trip
@login_required(login_url='login')
@permission_required('trip.add_trip')
def add_trip(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = TripForm(request.POST, company=company) 
    if request.method == 'POST':

        load_id = request.POST.get('load')
        load = Load.objects.get(company=company, id=load_id)

        vehicle_id = request.POST.get('vehicle')
        vehicle = Vehicle.objects.get(company=company, id=vehicle_id)

        distance = int(request.POST.get('distance')) + 50 #use this to estimate the trip cost.

        #create instance of a trip
        trip = Trip.objects.create(
            company=company,
            load = load,
            vehicle = vehicle,
            driver_accesory_pay = request.POST.get('driver_accesory_pay'),
            vehicle_odemeter = request.POST.get('vehicle_odemeter'),
            driver_advance = request.POST.get('driver_advance'),
            driver_milage = request.POST.get('driver_advance'),
            pick_up_location = request.POST.get('pick_up_location'),
            drop_off_location = request.POST.get('drop_off_location'),
            distance = distance,
        )
        description = f"Transport of {trip.load.commodity} from {trip.pick_up_location} to {trip.drop_off_location}, ({trip.distance}kms)"
        invoice_date = timezone.now().date()
        payment_term_days = load.estimate.customer.payment_term
        if payment_term_days == '2 DAYS':
            due_date = invoice_date + timedelta(days=2)
        elif payment_term_days == '7 DAYS' or payment_term_days == 'Cash on Delivery':
            due_date = invoice_date + timedelta(days=7)
        elif payment_term_days == '10 DAYS':
            due_date = invoice_date + timedelta(days=10)
        elif payment_term_days == '15 DAYS':
            due_date = invoice_date + timedelta(days=15)
        elif payment_term_days == '30 DAYS':
            due_date = invoice_date + timedelta(days=30)
        
        downpaymnet = load.estimate.customer.credit_limit / 100 * load.estimate.total
        
        #invoice note based on customer's credit limit and company payment details
        note = f'Downpayment of {load.estimate.customer.credit_limit}% (${downpaymnet}). Pay to:{load.company.invoice_payment_details}'
        #generate a invoice instance
        invoice = Invoice.objects.create(
            company=company,
            trip = trip,
            item = load.estimate.item,
            quantity = load.estimate.quantity,
            unit_price = load.estimate.unit_price,
            description = description,
            sub_total = load.estimate.sub_total,
            tax = load.estimate.tax,
            discount = load.estimate.discount,
            total = load.estimate.total,
            balance = load.estimate.total,
            invoice_date = invoice_date,
            due_date = due_date,
            status = 'Unpaid',
            note = note,

        )

        messages.success(request, f'Trip was added successfully.')
        return redirect('view_trip', trip.id)

    context= {
        'form':form,
    }
    return render(request, 'trip/trip/add-trip.html', context)
#--ends

# update trip
@login_required(login_url='login')
@permission_required('trip.change_trip')
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
@login_required(login_url='login')
@permission_required('trip.view_trip')
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
@login_required(login_url='login')
@permission_required('trip.view_trip')
def view_trip(request, pk):
    company=get_user_company(request)
    trip = Trip.objects.get(id=pk, company=company)
    expenses = Expense.objects.filter(company=company, trip=trip)
    invoice = Invoice.objects.get(company=company, trip=trip)
    payments = Payment.objects.filter(company=company, invoice=invoice) #invoice in invoices associated with the trip 
    form = ExpenseForm(request.POST, company=company) # for expense modal
    category_form = ExpenseCategoryForm(request.POST) # for expense category modal
    payment_form = PaymentForm(request.POST, company=company) # for payment modal
    context={
        'company':company,
        'trip':trip,
        'expenses':expenses,
        'invoice':invoice,
        'payments':payments,
        'form':form,
        'category_form':category_form,
        'payment_form':payment_form
    }
    return render(request, 'trip/trip/view-trip.html', context)
#--ends

# remove trip
@login_required(login_url='login')
@permission_required('trip.delete_trip')
def remove_trip(request, pk):
    if request.method == 'POST':
        trip = Trip.objects.get(id=pk, company=get_user_company(request))
        trip.delete()
        messages.success(request, f'Trip of id : {trip.trip_id} removed')
        return redirect('list_trips')
#--ends

#---------------------------------- Payment views------------------------------------------

# add payment
@login_required(login_url='login')
@permission_required('trip.add_payment')
def add_payment(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = PaymentForm(request.POST, company=company) 
    if request.method == 'POST':

        invoice_id = request.POST.get('invoice')
        invoice = Invoice.objects.get(company=company, id=invoice_id)
        amount = int(request.POST.get('amount'))

        #create instance of a payment
        payment = Payment.objects.create(
            company=company,
            transaction_id = request.POST.get('transaction_id'),
            invoice = invoice,
            amount = amount,
            paid_on = request.POST.get('paid_on'),
            payment_method = request.POST.get('payment_method'),
            remark = request.POST.get('remark'),
        )

        #update invoice balance
        invoice.balance = invoice.balance - amount

        # Update invoice status
        if invoice.balance <= 0:
            invoice.status = 'Paid'
        elif invoice.balance == invoice.total:
            invoice.status = 'Unpaid'
        else:
            invoice.status = 'Partially Paid'
        invoice.save()
  
        #send email to client

        messages.success(request, f'Payment was added and receipt sent to the customer successfuly.')
        return redirect('view_invoice', invoice.id)

    context= {
        'form':form,
    }
    return render(request, 'trip/payment/payment-list.html', context)
#--ends

# add payment inside a trip
@login_required(login_url='login')
@permission_required('trip.add_payment')
def add_payment_trip(request, pk):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = PaymentForm(request.POST, company=company) 
    if request.method == 'POST':

        trip = Trip.objects.get(id=pk)
        invoice = Invoice.objects.get(trip=trip)
        amount = int(request.POST.get('amount'))

        #create instance of a payment
        payment = Payment.objects.create(
            company=company,
            transaction_id = request.POST.get('transaction_id'),
            invoice = invoice,
            amount = amount,
            paid_on = request.POST.get('paid_on'),
            payment_method = request.POST.get('payment_method'),
            remark = request.POST.get('remark'),
        )

        #update invoice balance
        invoice.balance = invoice.balance - amount

        # Update invoice status
        if invoice.balance <= 0:
            invoice.status = 'Paid'
        elif invoice.balance == invoice.total:
            invoice.status = 'Unpaid'
        else:
            invoice.status = 'Partially Paid'
        invoice.save()
  
        #send email to client

        messages.success(request, f'Payment was added and receipt sent to the customer successfuly.')
        return redirect('view_trip', trip.id)

    context= {
        'form':form,
    }
    return render(request, 'trip/payment/payment-list.html', context)
#--ends

# update trip
@login_required(login_url='login')
@permission_required('trip.change_payment')
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
@login_required(login_url='login')
@permission_required('trip.view_payment')
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
@login_required(login_url='login')
@permission_required('trip.view_payment')
def view_payment(request, pk):
    trip = Trip.objects.get(id=pk, company=get_user_company(request))
    context={'trip':trip}
    return render(request, 'trip/trip/view-trip.html', context)
#--ends

# remove trip
@login_required(login_url='login')
@permission_required('trip.delete_payment')
def remove_payment(request, pk):
    if request.method == 'POST':
        trip = Trip.objects.get(id=pk, company=get_user_company(request))
        trip.delete()
        messages.success(request, f'Trip of id : {trip.trip_id} removed')
        return redirect('list_trips')
#--ends

#---------------------------------- Expense Category views------------------------------------------

# add expense category
@login_required(login_url='login')
@permission_required('trip.add_expense_category')
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
@login_required(login_url='login')
@permission_required('trip.view_expense_category')
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
@login_required(login_url='login')
@permission_required('trip.delete_expense_category')
def remove_expense_category(request, pk):
    if request.method == 'POST':
        trip = Trip.objects.get(id=pk, company=get_user_company(request))
        trip.delete()
        messages.success(request, f'Trip of id : {trip.trip_id} removed')
        return redirect('list_trips')
#--ends

#---------------------------------- Expense views------------------------------------------

# add expense
@login_required(login_url='login')
@permission_required('trip.add_expense')
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

# add expense inside a trip 
@login_required(login_url='login')
@permission_required('trip.add_expense')
def add_expense_trip(request, pk):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = ExpenseForm(request.POST, company=company) 
    if request.method == 'POST':
        trip = Trip.objects.get(id=pk)

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
        return redirect('view_trip', trip.id )

    context= {
        'form':form,
    }
    return render(request, 'trip/expense/expense-list.html', context)
#--ends

# update trip
@login_required(login_url='login')
@permission_required('trip.change_expense')
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
@login_required(login_url='login')
@permission_required('trip.view_expense')
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
@login_required(login_url='login')
@permission_required('trip.view_expense')
def view_expense(request, pk):
    trip = Trip.objects.get(id=pk, company=get_user_company(request))
    context={'trip':trip}
    return render(request, 'trip/trip/view-trip.html', context)
#--ends

# remove trip
@login_required(login_url='login')
@permission_required('trip.delete_expense')
def remove_expense(request, pk):
    if request.method == 'POST':
        trip = Trip.objects.get(id=pk, company=get_user_company(request))
        trip.delete()
        messages.success(request, f'Trip of id : {trip.trip_id} removed')
        return redirect('list_trips')
#--ends

#---------------------------------- Invoice views------------------------------------------
# add invoice
@login_required(login_url='login')
@permission_required('trip.add_invoice')
def add_invoice(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = InvoiceForm(request.POST, company=company)  
    if request.method == 'POST':

        trip_id = request.POST.get('trip')
        trip = Trip.objects.get(company=company, id=trip_id)

        description = f"Transport of {trip.load.commodity} from {trip.pick_up_location} to {trip.drop_off_location}, ({trip.distance}kms)"

        service = Service.objects.create(
            company=company,
            name = request.POST.get('name'),
            description = description,
            unit = request.POST.get('unit'),
            unit_price = request.POST.get('unit_price'),
            amount = request.POST.get('sub_total'),
            tax = request.POST.get('tax')

        )

        #create instance of a invoice
        invoice = Invoice.objects.create(
            company=company,
            trip = trip,
            service = service,
            sub_total = request.POST.get('sub_total'),
            discount = request.POST.get('discount'),
            tax = request.POST.get('tax'),
            total = request.POST.get('total'),
            balance = request.POST.get('total'),
            invoice_date = request.POST.get('invoice_date'),
            due_date = request.POST.get('due_date'),
            note = request.POST.get('note'),
        )

        messages.success(request, f'Invoice was added successfully.')
        return redirect('view_invoice', invoice.id)

    context= {
        'form':form,
    }
    return render(request, 'trip/invoice/add-invoice.html', context)
#--ends

# update trip
@login_required(login_url='login')
@permission_required('trip.change_invoice')
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
@login_required(login_url='login')
@permission_required('trip.view_invoice')
def list_invoices(request):
    invoices = Invoice.objects.filter(company=get_user_company(request))
    context = {
        'invoices':invoices,
    }
    return render(request, 'trip/invoice/invoices-list.html', context)
#--ends

#view trip
@login_required(login_url='login')
@permission_required('trip.view_invoice')
def view_invoice(request, pk):
    company = get_user_company(request)
    invoice = Invoice.objects.get(id=pk, company=get_user_company(request))
    context={
        'invoice':invoice,
        'company':company
        }
    return render(request, 'trip/invoice/view-invoice.html', context)
#--ends

# remove trip
@login_required(login_url='login')
@permission_required('trip.delete_invoice')
def remove_invoice(request, pk):
    if request.method == 'POST':
        trip = Trip.objects.get(id=pk, company=get_user_company(request))
        trip.delete()
        messages.success(request, f'Trip of id : {trip.trip_id} removed')
        return redirect('list_trips')
#--ends

#send trip invoice
@login_required(login_url='login')
@permission_required('trip.view_invoice') 
def send_trip_invoice(request, pk):
    company = get_user_company(request)
    trip = get_object_or_404(Trip, id=pk, company=company)
    print(f'This is the trip id :{trip.trip_id}')
    invoice = Invoice.objects.get(trip=trip)
    preference = Preference.objects.get(company=company)

    #having this context because delay() need model serialzation
    context = {
        'customer_name': trip.load.estimate.customer.name,
        'invoice_pdf': 'pdf of the invoice' #invoice goes here
        #'due_amount': loan.due_amount,
        #'due_date': user_local_time(loan.company.timezone, loan.due_date).date(),
        #'total_payable': loan.total_payable(),
        #'tzone':company.timezone
    }

    from_name = preference.email_from_name
    from_email = preference.from_email
    template_path = 'trip/invoice/trip-invoice.html'
    subject = 'Trip Invoice'
    recipient_email = trip.load.estimate.customer.email
    replyto_email = company.email

    send_email_task.delay(
        context,  
        template_path, 
        from_name, 
        from_email, 
        subject, 
        recipient_email, 
        replyto_email
    )

    messages.success(request, 'Invoice sent to customer.')
    return redirect('view_trip', trip.id)

# generate invoice pdf view 
def generate_invoice_pdf(request, pk):
    company = get_user_company(request)
    trip = Trip.objects.get(id=pk, company=company)
    invoice = Invoice.objects.get(trip=trip)
    # Path to your HTML template.
    template_path = 'trip/invoice/invoice-template.html'

    # Load the HTML template using Django's get_template method.
    template = get_template(template_path)
    context = {
        'company':company,
        'invoice':invoice
    }  # You can pass context data here if needed

    # Render the template with the context data.
    html = template.render(context)

    # Create a response object with PDF content type.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{invoice.invoice_id}.pdf"'

    # Create a PDF object using xhtml2pdf's pisa.CreatePDF.
    pdf = pisa.CreatePDF(html, dest=response)

    # Check if PDF generation was successful.
    if not pdf.err:
        return response

    # If PDF generation failed, return an error message.
    return HttpResponse('PDF generation failed: %s' % pdf.err)


#---------------------------------- Estimate views------------------------------------------

# add estimate
@login_required(login_url='login')
@permission_required('trip.add_estimate')
def add_estimate(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = EstimateForm(request.POST, company=company)  
    if request.method == 'POST':

        customer_id = request.POST.get('customer')
        customer = Customer.objects.get(company=company, id=customer_id)

        #create instance of a invoice
        estimate = Estimate.objects.create(
            company=company,
            customer = customer,
            valid_till = request.POST.get('valid_till'),
            description = request.POST.get('description'),
            item = request.POST.get('item'),
            quantity = request.POST.get('quantity'), #km/ml
            unit_price = request.POST.get('unit_price'),
            sub_total = request.POST.get('sub_total'),
            discount = request.POST.get('discount'),
            tax = request.POST.get('tax'),
            total = request.POST.get('total'),
            note = request.POST.get('note'),
        )

        messages.success(request, f'Estimate was added successfully.')
        return redirect('view_estimate', estimate.id)

    context= {
        'form':form,
    }
    return render(request, 'trip/estimate/add-estimate.html', context)
#--ends

# update estimate
@login_required(login_url='login')
@permission_required('trip.change_estimate')
def update_estimate(request, pk):
    company = get_user_company(request) #get request user company
    estimate = Estimate.objects.get(id=pk, company=company)
    if request.method == 'POST':
        # block updates on accepted quotes
        if estimate.status != 'Accepted':

            customer_id = request.POST.get('customer')
            customer = Customer.objects.get(company=company, id=customer_id)

            #update instance 
            estimate.company = company
            estimate.customer = customer
            estimate.valid_till = request.POST.get('valid_till')
            estimate.description = request.POST.get('description')
            estimate.item = request.POST.get('item')
            estimate.quantity = request.POST.get('quantity')
            estimate.unit_price = request.POST.get('unit_price')
            estimate.sub_total = request.POST.get('sub_total')
            estimate.discount = request.POST.get('discount')
            estimate.tax = request.POST.get('tax')
            estimate.total = request.POST.get('total')
            estimate.note = request.POST.get('note')
            estimate.status = request.POST.get('status')
            estimate.save()
            
            messages.success(request, f'Estimate details updated successfully.')
            return redirect('view_estimate', estimate.id)
        else:
            messages.error(request, f'Accepted quotations can not be edited!')
            return redirect('view_estimate', estimate.id)
    else:
        # prepopulate the form with existing data
        form_data = {
            'customer': estimate.customer,
            'valid_till': estimate.valid_till,
            'item': estimate.item,
            'quantity': estimate.quantity,
            'unit_price': estimate.unit_price,
            'sub_total': estimate.sub_total,
            'tax': estimate.tax,
            'total': estimate.total,
            'description': estimate.description,
            'note': estimate.note, 
            'status':estimate.status           
        }

        form = EstimateForm(initial=form_data, company=company )
        context = {
            'estimate':estimate,
            'form':form
        }
        return render(request,'trip/estimate/update-estimate.html', context)
#--ends

#estimate list
@login_required(login_url='login')
@permission_required('trip.view_estimate')
def list_estimates(request):
    estimates = Estimate.objects.filter(company=get_user_company(request))
    number_of_estimates = estimates.count()
    context = {
        'estimates':estimates,
        'number_of_estimates':number_of_estimates
    }
    return render(request, 'trip/estimate/estimates-list.html', context)
#--ends

#view estimate
@login_required(login_url='login')
@permission_required('trip.view_estimate')
def view_estimate(request, pk):
    company=get_user_company(request)
    estimate = Estimate.objects.get(id=pk, company=company)
    context={
        'estimate':estimate,
        'company':company
        }
    return render(request, 'trip/estimate/view-estimate.html', context)
#--ends

# remove estimate
@login_required(login_url='login')
@permission_required('trip.delete_estimate')
def remove_estimate(request, pk):
    if request.method == 'POST':
        estimate = Estimate.objects.get(id=pk, company=get_user_company(request))
        estimate.delete()
        messages.success(request, f'Estimate of id : {estimate.estimate_id} removed')
        return redirect('list_estimates')
#--ends

#send estimate to client via email
@login_required(login_url='login')
@permission_required('trip.view_estimate') 
def send_estimate(request, pk):
    company = get_user_company(request)
    estimate = Estimate.objects.get(id=pk, company=company)
    preference = Preference.objects.get(company=company)

    #having this context because delay() need model serialzation
    context = {
        'customer_name': estimate.customer.name,
        'estimate_pdf': 'pdf of the estimate',
        'company_name': company.name
        #'due_amount': loan.due_amount,
        #'due_date': user_local_time(loan.company.timezone, loan.due_date).date(),
        #'total_payable': loan.total_payable(),
        #'tzone':company.timezone
    }

    from_name = preference.email_from_name
    from_email = preference.from_email
    template_path = 'trip/estimate/load-estimate.html'
    subject = 'Quotation'
    recipient_email = estimate.customer.email
    replyto_email = company.email

    send_email_task.delay(
        context, 
        template_path, 
        from_name, 
        from_email, 
        subject, 
        recipient_email, 
        replyto_email
    )

    messages.success(request, 'Estimate sent to customer.')
    return redirect('view_estimate', estimate.id)

#---------------------------------- Reminder views------------------------------------------

# add reminder
@login_required(login_url='login')
@permission_required('trip.add_reminder')
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
@login_required(login_url='login')
@permission_required('trip.view_reminder')
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
@login_required(login_url='login')
@permission_required('trip.delete_reminder')
def remove_reminder(request, pk):
    #if request.method == 'POST':
    reminder = Reminder.objects.get(id=pk, company=get_user_company(request))
    reminder.delete()
    messages.success(request, 'Reminder removed')
    return redirect('list_reminders')
#--ends

#---------------------------------- Reminder views------------------------------------------



#---------------------------------- front end endpoint views -------------------------------------------------------------------------


# view to get trip info when adding an invoice
@login_required(login_url='login')
def get_trip_info(request, trip_id):
    company = get_user_company(request)
    try:
        trip = Trip.objects.get(id=trip_id, company=company)  # Fetch the Trip object based on the trip_id
        trip_info = {
            'vehicle': trip.vehicle.plate_number,
            'customer': trip.load.customer.name,
        }
        return JsonResponse(trip_info)
    except Trip.DoesNotExist:
        return JsonResponse({'error': 'Trip not found'}, status=404)
    
#--------------------------- vehicle info ____________________________________________

# view to get load info when adding a trip
@login_required(login_url='login')
def get_vehicle_info(request, vehicle_id):
    company = get_user_company(request)
    try:
        vehicle = Vehicle.objects.get(id=vehicle_id, company=company)
        try:
            driver = Driver.objects.get(assigned_vehicle=vehicle, company=company)
        except Driver.DoesNotExist:
            driver = None

        vehicle_info = {
            'trailer': vehicle.trailer_number,
            'driver': driver.first_name + ' ' + driver.last_name ,
        }
        return JsonResponse(vehicle_info)
    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Vehicle not found'}, status=404)

#--------------------------- load info ____________________________________________

#view to get load info when adding an trip
@login_required(login_url='login')
def get_load_info(request, load_id):
    company = get_user_company(request)
    try:
        load = Load.objects.get(id=load_id, company=company)
        load_info = {
            'customer': load.estimate.customer.name,
            'commodity': load.commodity,
        }
        return JsonResponse(load_info)
    except Load.DoesNotExist:
        return JsonResponse({'error': 'Load not found'}, status=404)
    
#--------------------------- estimate info ____________________________________________

#view to get estimate info when adding an load
@login_required(login_url='login')
def get_estimate_info(request, estimate_id):
    company = get_user_company(request)
    try:
        estimate = Estimate.objects.get(id=estimate_id, company=company)
        estimate_info = {
            'amount': estimate.total,
            'item': estimate.item,
            'quantity': estimate.quantity,
            'customer': estimate.customer.name,
        }
        return JsonResponse(estimate_info)
    except Estimate.DoesNotExist:
        return JsonResponse({'error': 'Estimate not found'}, status=404)

