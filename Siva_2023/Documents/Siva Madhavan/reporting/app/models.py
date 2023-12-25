from __future__ import unicode_literals
from django.db import models
from uuid import uuid4
from django.contrib.admin.widgets import AdminDateWidget


class MedicalProblems(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'Medical_problems'
        verbose_name_plural = "Medical Problems"

    def __str__(self):
        return self.name


class medical_conditions(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    medicalprobs = models.ForeignKey('MedicalProblems', on_delete=models.SET_NULL, null=True)
    ICD_code = models.CharField(max_length=100)

    class Meta:
        db_table = 'medical_conditions'
        verbose_name_plural = "Medical Conditions"

    def __str__(self):
        return self.medicalprobs.name


class insurance(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    individualID = models.CharField(max_length=100)
    insurance_name = models.CharField(max_length=100)
    claim = models.CharField(max_length=100)
    effective_date = models.DateField()

    class Meta:
        db_table = 'Insurance'
        verbose_name_plural = "Insurance Modules"

    def __str__(self):
        return self.insurance_name


class Patient(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=12)
    email = models.EmailField(max_length=50)
    fitplus_user_id = models.UUIDField(default=uuid4, null=True, editable=False)
    created_date = models.DateField(auto_now=True)
    modified_date = models.DateField(auto_now_add=True)
    created_by_id = models.UUIDField(default=uuid4, null=True, editable=False)
    facility_id = models.UUIDField(default=uuid4, null=True, editable=False)
    modified_by_id = models.UUIDField(default=uuid4, null=True, editable=False)
    primary_provider_id = models.UUIDField(default=uuid4, null=True, editable=False)
    full_name = models.CharField(max_length=200, editable=False)
    Insurance = models.ManyToManyField('insurance',blank=True, null=True)
    Medical_conditions = models.ManyToManyField('medical_conditions', blank=True, null=True)

    class Meta:
        db_table = 'Patient'
        verbose_name_plural = "Patients"

    def save(self, *args, **kwargs):
        self.full_name = str(self.last_name) + ', ' + str(self.first_name)
        super(Patient, self).save(*args, **kwargs)
