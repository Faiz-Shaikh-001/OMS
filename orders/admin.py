from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product_purchased', 'date', 'payment_method')
    search_fields = ('customer__first_name', 'product_purchased')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('object_id', 'product', 'quantity', 'price', 'total')
    search_fields = ('order__customer__first_name', 'product__name')
