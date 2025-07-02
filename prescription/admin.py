from django.contrib import admin
from .models import Prescription


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'doctor', 'checkup_date')
    search_fields = ('customer__first_name', 'doctor__name')
