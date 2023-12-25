from django import forms
from .models import *


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'


class ModuleForm(forms.ModelForm):
    class Meta:
        model = insurance
        fields = '__all__'
        widgets = {
            'effective_date': forms.DateInput(format='%m/%d/%Y',
                                              attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                                     'type': 'date'}),
        }


class Module2Form(forms.ModelForm):
    class Meta:
        model = medical_conditions
        fields = '__all__'


class MedicalProblemsForm(forms.ModelForm):
    class Meta:
        model = MedicalProblems
        fields = '__all__'
