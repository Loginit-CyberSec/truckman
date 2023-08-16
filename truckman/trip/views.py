from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Vehicle, Vehicle_Make, Vehicle_Model, Driver
from .forms import VehicleForm, DriverForm
from truckman.utils import get_user_company


#---------------------------------- Vehicle Views------------------------------------------

# add vehicle
def add_vehicle(request):
    company = get_user_company(request) #get request user company
    #instantiate the two kwargs to be able to access them on the forms.py
    form = VehicleForm(request.POST, company=company) 
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
            milage_unit = request.POST.get('milage_unit'),
            insurance_expiry = request.POST.get('insurance_expiry'),
            manufacture_year = request.POST.get('manufacture_year'),
            purchase_year = request.POST.get('purchase_year'),
            condition = request.POST.get('condition'),
            image = request.FILES.get('image'),
            notes = request.POST.get('notes'),
        )

        messages.success(request, f'Vehicle {vehicle.plate_number} was added successfully.')
        return redirect('list_vehicles')

    #redirect
    context= {'form':form}
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
        vehicle.milage_unit = request.POST.get('milage_unit')
        vehicle.insurance_expiry = request.POST.get('insurance_expiry')
        vehicle.manufacture_year = request.POST.get('manufacture_year')
        vehicle.purchase_year = request.POST.get('purchase_year')
        vehicle.condition = request.POST.get('condition')
        vehicle.image = request.FILES.get('image')
        vehicle.notes = request.POST.get('notes')
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
            'image': vehicle.image,
            'notes': vehicle.notes
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
        #create instance of a driver
        driver = Driver.objects.create(
            company=company,
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            id_no = request.POST.get('id_no'),
            dl_no = request.POST.get('dl_no'),
            passport_number = request.POST.get('passport_number'),
            tel_home = request.POST.get('tel_home'),
            tel_roam = request.POST.get('tel_roam'),
            date_hired = request.POST.get('date_hired'),
            emergency_contact_person = request.POST.get('emergency_contact_person'),
            emergency_contact_no = request.POST.get('emergency_contact_no'),
            emergency_contact_two = request.POST.get('emergency_contact_two'),
            passport_photo = request.FILES.get('passport_photo'),
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
        #update instance 
        driver.company=company
        driver.first_name = request.POST.get('first_name')
        driver.last_name = request.POST.get('last_name')
        driver.id_no = request.POST.get('id_no')
        driver.dl_no = request.POST.get('dl_no')
        driver.passport_number = request.POST.get('passport_number')
        driver.tel_home = request.POST.get('tel_home')
        driver.tel_roam = request.POST.get('tel_roam')
        driver.date_hired = request.POST.get('date_hired')
        driver.emergency_contact_person = request.POST.get('emergency_contact_person')
        driver.emergency_contact_no = request.POST.get('emergency_contact_no')
        driver.emergency_contact_two = request.POST.get('emergency_contact_two')
        driver.passport_photo = request.FILES.get('passport_photo')
        driver.save()
        
        messages.success(request, f'Driver details edited successfully.')
        return redirect('list_drivers')
    else:
        # prepopulate the form with existing data
        form_data = {
            'first_name': driver.first_name,
            'last_name': driver.last_name,
            'id_no': driver.id_no,
            'dl_no': driver.dl_no,
            'passport_number': driver.passport_number,
            'tel_home': driver.tel_home,
            'tel_roam': driver.tel_roam,
            'date_hired': driver.date_hired,
            'emergency_contact_person': driver.emergency_contact_person,
            'emergency_contact_no': driver.emergency_contact_no,
            'emergency_contact_two': driver.emergency_contact_two,
            'passport_photo': driver.passport_photo,
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