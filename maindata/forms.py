
# from django import forms
# from .models import User
# class ClientForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super(ClientForm, self).__init__(*args, **kwargs)
#         # Filter the authors by name "Ahmed"
#         self.fields['client'].queryset = User.objects.filter(type="C")

from django import forms
from .models import Employee, EmployeeCategory

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'national_id', 'phone_number', 'address', 'notes', 'type', 'category']

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        if self.instance.type == 'E':
            self.fields['category'].queryset = EmployeeCategory.objects.filter(category_type='E')
        if self.instance.type == 'W':
            self.fields['category'].queryset = EmployeeCategory.objects.filter(category_type='T')
