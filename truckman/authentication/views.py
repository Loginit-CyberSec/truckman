from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required 
from truckman.decorators import permission_required 
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission
from .forms import CustomUserCreationForm, StaffForm, RoleForm, ClientForm
from .models import Client, CustomUser, Role
from truckman.utils import get_user_company

#----------------- User Views --------------------------
#sign up a user
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data['company_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # Create a new client/tenant
            client = Client.objects.create(
                name=company_name,
                email=email,
            )

            # Create a new user associated with the client
            user = CustomUser.objects.create_user(
                username=email,
                email=email,
                password=password,
                company=client
            )

            # Log in the user
            login(request, user)
            
            messages.success(request, 'Account created successfully.')
            # Redirect to a success page or the user's dashboard
            return redirect('home') 
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'authentication/auth-register.html', context)
    
#login a user
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home') 
            else:
                # Handle inactive user case
                messages.error(request, 'User is inactive!')
                return render(request, 'authentication/auth-login.html')
        else:
            # Handle invalid login case
            messages.error(request, 'Wrong email or password!')
            return render(request, 'authentication/auth-login.html')

    return render(request, 'authentication/auth-login.html') 

#logout a user
def logout_user(request):
    logout(request)
    return redirect('login')

#----------------- Role Views ---------------------------
#add role view
@login_required(login_url='login')
@permission_required('authentication.add_role')
def add_role(request):
    if request.method == 'POST':
        # Get all available permissions
        permissions = Permission.objects.filter(
                content_type__model__in=[
                    'client', 'customuser', 'role', 'vehicle_make',
                    'vehicle_model', 'vehicle', 'driver', 'customer',
                    'consignee', 'shipper', 'load', 'trip', 'estimate',
                    'invoice', 'payment', 'expense', 'expense_category', 'reminder' 
                ] 
            )
        company = get_user_company(request) 

        # Create a Role instance with form data
        role = Role(
            company=company,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        role.save()

        # Get the selected permissions from form 
        selected_permissions = request.POST.getlist('permissions')
        role.permissions.set(selected_permissions)  # Set the selected permissions to the ManyToManyField

        messages.success(request, 'Role created successfully')
        return redirect('list_roles')
    return render(request, 'authentication/role/roles-list.html')

# update role  view
@login_required(login_url='login')
@permission_required('authentication.change_role')
def update_role(request, pk):
    pass

# role list view
@login_required(login_url='login')
@permission_required('authentication.view_role')
def list_roles(request):
    company = get_user_company(request)
    roles = Role.objects.filter(company=company)
    form = RoleForm(request.POST)
    context = {
        'roles':roles,
        'form':form
    }
    return render(request, 'authentication/role/roles-list.html', context)

#  view role
@login_required(login_url='login')
@permission_required('authentication.view_role')
def view_role(request, pk):
    pass

#  remove role
@login_required(login_url='login')
@permission_required('authentication.delete_role')
def remove_role(request, pk):
    pass

#----------------- Staff Views ---------------------------
#add staff view
@login_required(login_url='login')
@permission_required('authentication.add_customuser')
def add_staff(request):
    company=get_user_company(request)
    form = StaffForm(request.POST, company=company)
    if request.method == 'POST':

        role_id = request.POST.get('role')
        role = Role.objects.get(company=company, id=role_id)

        #retrieve all permissions assigned to a role
        permissions = role.permissions.all() 

        #create instance of a staff
        staff = CustomUser.objects.create(
            company=company,
            username = request.POST.get('email').lower(),
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            email = request.POST.get('email').lower(),
            password = make_password(request.POST.get('password')),
            role = role,
            phone = request.POST.get('phone'),
            designation = request.POST.get('designation'),
            department = request.POST.get('department'),
            date_joined = request.POST.get('date_joined'),
            profile_photo = request.FILES.get('profile_photo'),
        )
        #assign staff role permissions
        staff.user_permissions.add(*permissions)

        messages.success(request, f'{staff.first_name} added as staff.')
        return redirect('list_staffs')
    context= {
        'form':form,
    }
    return render(request, 'authentication/staff/staffs-list.html', context)

# update staff  view
@login_required(login_url='login')
@permission_required('authentication.change_customuser')
def update_staff(request, pk):
    company = get_user_company(request) 
    staff = CustomUser.objects.get(id=pk, company=company)
    
    if request.method == 'POST':
        
        role_id = request.POST.get('role')
        role = Role.objects.get(id=role_id, company=company)

        #retrieve all permissions assigned to a role
        permissions = role.permissions.all() 

        staff.company= company
        staff.email = request.POST.get('email').lower()
        staff.username = request.POST.get('email').lower()
        staff.first_name = request.POST.get('first_name')
        staff.last_name = request.POST.get('last_name')
        staff.phone = request.POST.get('phone')
        staff.department = request.POST.get('department')
        staff.designation = request.POST.get('designation')
        staff.profile_photo = request.FILES.get('profile_photo')
        staff.role = role
        staff.save()

        #assign staff role permissions
        staff.user_permissions.add(*permissions)
        
        messages.success(request, 'Staff details updated')

        return redirect('list_staffs')
    else:
        form_data = {
            'email':staff.email,
            'first_name': staff.first_name,
            'last_name': staff.last_name,
            'phone': staff.phone, 
            'department':staff.department,
            'designation':staff.designation,
            'profile_photo':staff.profile_photo,
            'role':staff.role,
        }
    
        form = StaffForm(initial=form_data, company=company)

        context = {
            'form':form, 
            'staff':staff
        }

        return render(request,'authentication/staff/update-staff.html', context )
# -- ends 

# staff list view
@login_required(login_url='login')
@permission_required('authentication.view_customuser')
def list_staffs(request):
    company = get_user_company(request)
    staffs = CustomUser.objects.filter(company=company)
    form = StaffForm(request.POST, company=company)
    context = {
        'staffs':staffs,
        'form':form
    }
    return render(request, 'authentication/staff/staffs-list.html', context)

#  view staff
@login_required(login_url='login')
@permission_required('authentication.view_customuser')
def view_staff(request, pk):
    pass

#remove staff
@login_required(login_url='login')
@permission_required('authentication.delete_customuser')
def remove_staff(request, pk):
    pass

#----------------- User Views ---------------------------
# user profile
@login_required(login_url='login')
def user_profile(request, pk):
    company = get_user_company(request)
    user = CustomUser.objects.get(id=pk)
    
    form_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone
        }
    
    form = StaffForm(initial=form_data, company=company)

    context = {
        'form':form, 
        'user':user    
        }
    return render(request, 'authentication/user/user-profile.html', context)

# update user profile
@login_required(login_url='login')
def update_user_profile(request, pk):
    company = get_user_company(request)
    user = CustomUser.objects.get(id=pk)
    if request.method == "POST":
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone = request.POST.get('phone')
        user.save()

        messages.success(request, 'Profile updated succesfully.')

    return redirect('user_profile', user.id)
    #return render(request, 'authentication/user/user-profile.html', context)

# client global settings view
@login_required(login_url='login')
@permission_required('authentication.view_client')
def global_settings(request):
    company = get_user_company(request)
    form = ClientForm(request.POST)
    if request.method == 'POST':
        company.name = request.POST.get('name')
        company.address = request.POST.get('address')
        company.phone_no = request.POST.get('phone_no')
        company.invoice_payment_details = request.POST.get('invoice_payment_details')
        company.save()

    else:
        form_data = {
            'name':company.name,
            'name':company.address,
        }

    context = {
        'company':company,
        'form':form,
    }
    return render(request, 'authentication/settings/settings.html', context)