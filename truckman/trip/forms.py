from django import forms
from .models import Vehicle, Vehicle_Make, Vehicle_Model, Driver, Customer


#---------------------------------- Vehicle forms ------------------------------------------
class VehicleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')# Get the company from kwargs
        super(VehicleForm, self).__init__(*args, **kwargs)
        self.fields['make'].queryset = Vehicle_Make.objects.filter(company=company)
        self.fields['model'].queryset = Vehicle_Model.objects.filter(company=company)

    class Meta:
        model = Vehicle
        fields = '__all__'
        exclude =['company']

        widgets = {
                'plate_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Registration number'}),
                'trailer_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Trailer number'}),
                'vin': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'1KZ-345678'}),
                'milage': forms.NumberInput(attrs={'class': 'form-control number-spinner','value': '0', 'placeholder':'345678'}),
                'make': forms.Select(attrs={'class': 'form-select js-select2'}),
                'model': forms.Select(attrs={'class': 'form-select js-select2'}),
                #'model': forms.Select(attrs={'class': 'form-select js-select2'}),
                'milage_unit': forms.Select(attrs={'class': 'form-select js-select2'}),
                'condition': forms.Select(attrs={'class': 'form-select js-select2'}),
                'insurance_expiry': forms.DateInput(attrs={'class': 'form-control  date-picker', 'data-date-format':'yyyy-mm-dd', 'placeholder':'yyyy-mm-dd'}),
                'manufacture_year': forms.DateInput(attrs={'class': 'form-control  date-picker-range', 'data-date-format':'yyyy-mm-dd', 'placeholder':'yyyy-mm-dd'}),
                'purchase_year': forms.DateInput(attrs={'class': 'form-control  date-picker-range', 'data-date-format':'yyyy-mm-dd', 'placeholder':'yyyy-mm-dd'}),
                'notes': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'cf-default-textarea' ,'placeholder':'Notes...'}),
                'image': forms.FileInput(attrs={'class': 'form-file-input', 'id': 'customFile'}),
            } 
        
#---------------------------------- Driver forms ------------------------------------------
class DriverForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')# Get the company from kwargs
        super(DriverForm, self).__init__(*args, **kwargs)
        self.fields['assigned_vehicle'].queryset = Vehicle.objects.filter(company=company)

    class Meta:
        model = Driver
        fields = '__all__'
        exclude =['company']

        widgets = {
                'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'John '}),
                'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Moriasi'}),
                'id_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'34567800'}),
                'dl_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'34K5678'}),
                'passport_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'KZ345678'}),
                'tel_home': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'0700000000'}),
                'tel_roam': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'0700000000'}),
                'date_hired': forms.DateInput(attrs={'class': 'form-control  date-picker', 'data-date-format':'yyyy-mm-dd', 'placeholder':'yyyy-mm-dd'}),
                'date_terminated': forms.DateInput(attrs={'class': 'form-control  date-picker-range', 'data-date-format':'yyyy-mm-dd', 'placeholder':'yyyy-mm-dd'}),
                'emergency_contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Moriasi Ndoyo'}),
                'emergency_contact_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'0700000000'}),
                'emergency_contact_two': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'0700000000'}),
                'passport_photo': forms.FileInput(attrs={'class': 'form-file-input', 'id': 'customFile'}),
                'assigned_vehicle': forms.Select(attrs={'class': 'form-select js-select2'}),
            } 
        
#---------------------------------- Customer forms ------------------------------------------   
class CustomerForm(forms.ModelForm):
    '''
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')# Get the company from kwargs
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['assigned_vehicle'].queryset = Customer.objects.filter(company=company) 
    '''
    class Meta:
        model = Customer
        fields = '__all__'
        exclude =['company', 'customer_id', 'date_added']

        widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'John Shippers'}),
                'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Moriasi Iteo'}),
                'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'034567800'}),
                'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'info@company.com'}),
                'address_one': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'ABC Road'}),
                'address_two': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'ABC Road'}),
                'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'KENYA'}),
                'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'MOMBASA'}),
                'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder':'www.company.com'}),
                'credit_limit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'20'}),
                'payment_term': forms.Select(attrs={'class': 'form-select js-select2'}),
                'logo': forms.FileInput(attrs={'class': 'form-file-input', 'id': 'customFile'}),
            }    
#---------------------------------- Consignee forms ------------------------------------------ 


