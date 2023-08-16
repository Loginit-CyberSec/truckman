from django import forms
from .models import Vehicle, Vehicle_Make, Vehicle_Model



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
        


        
       