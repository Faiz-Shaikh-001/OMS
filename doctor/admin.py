from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'hospital_name', 'city')
    search_fields = ('name', 'hospital_name')
    list_filter = ('hospital_name', 'city')

