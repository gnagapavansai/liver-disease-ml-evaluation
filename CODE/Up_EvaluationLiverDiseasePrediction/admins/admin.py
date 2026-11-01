from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Patient, Prediction

admin.site.register(Patient)
admin.site.register(Prediction)