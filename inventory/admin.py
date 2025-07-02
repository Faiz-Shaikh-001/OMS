from django.contrib import admin
from .models import Frame, LensProduct

@admin.register(Frame)
class FrameAdmin(admin.ModelAdmin):
    list_display = ['name', 'frame_type', 'code', 'color', 'size', 'quantity', 'sales_price', 'purchase_price']
    search_fields = ['name', 'code', 'color']
    list_filter = ['frame_type', 'date']
    readonly_fields = ['barcode_image']


@admin.register(LensProduct)
class LensProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'lens_type', 'company_name', 'material_type', 'side', 'spherical', 'cylindrical', 'sales_price']
    search_fields = ['product_name', 'company_name']
    list_filter = ['lens_type', 'material_type']
    readonly_fields = ['barcode_image']


