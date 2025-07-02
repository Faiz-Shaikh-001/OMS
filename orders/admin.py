from django.contrib import admin

from .models import Customer, Doctor, Prescription, Order

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'city')
    search_fields = ('first_name', 'last_name', 'phone_number')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'hospital_name', 'city')
    search_fields = ('name', 'hospital_name')

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'doctor', 'checkup_date')
    search_fields = ('customer__first_name', 'doctor__name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product_purchased', 'date', 'payment_method')
    search_fields = ('customer__first_name', 'product_purchased')
