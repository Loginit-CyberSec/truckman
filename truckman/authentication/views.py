from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm  
from .models import Client, CustomUser



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
