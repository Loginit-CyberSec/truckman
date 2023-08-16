
from django import forms
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError  
from .models import CustomUser, Client
from django.forms.widgets import CheckboxSelectMultiple


class CustomUserCreationForm(forms.Form): 
    company_name = forms.CharField(label='Enter Company Name')
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_company_name(self):
        company_name = self.cleaned_data['company_name'].lower()
        r = Client.objects.filter(name=company_name) 
        if r.count():
            raise  ValidationError("Company name already exists")
        return company_name

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = CustomUser.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2
    '''
    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            #self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user
    '''