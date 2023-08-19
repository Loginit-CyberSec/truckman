from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Vehicle, Vehicle_Make, Vehicle_Model, Driver, Customer, Consignee, Shipper, Load, Trip
from .forms import VehicleMakeForm, VehicleModelForm, VehicleForm, DriverForm, CustomerForm, ConsigneeForm, ShipperForm, LoadForm, TripForm
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
def update_trip(request, pk):
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

#---------------------------------- Trip views------------------------------------------