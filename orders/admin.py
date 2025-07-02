from django.contrib import admin

from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product_purchased', 'date', 'payment_method')
    search_fields = ('customer__first_name', 'product_purchased')
