from django.contrib import admin
from .models import Customer
from django.utils.html import format_html

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'city')
    search_fields = ('first_name', 'last_name', 'phone_number')
    list_filter = ('gender', 'age_group', 'city')

    def image_tag(self, obj):
        if obj.customer_image:
            return format_html('<img src="{}" style="height:50px; border-radius:5px;"/>', obj.customer_image.url)
        return "No image"
    image_tag.short_description = "Profile Image"
