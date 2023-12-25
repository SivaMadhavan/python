from django.contrib import admin
from . models import *
admin.site.register(Patient)
admin.site.register(insurance)
admin.site.register(medical_conditions)
admin.site.register(MedicalProblems)
