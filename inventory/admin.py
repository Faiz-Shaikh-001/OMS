from django.contrib import admin
from .models import Frame, SingleVision, Bifocal, ContactLens, Progressive

@admin.register(Frame)
class FrameAdmin(admin.ModelAdmin):
    list_display = ['name', 'frame_type', 'color', 'size', 'quantity', 'purchase_price', 'sales_price']
    search_fields = ['name', 'frame_type', 'color']
    list_filter = ['frame_type', 'color']
    ordering = ['name', 'frame_type']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(SingleVision)
class SingleVisionAdmin(admin.ModelAdmin):
    list_display = ['name', 'company_name', 'material_type', 'index', 'spherical', 'cylindrical', 'pair', 'purchase_price', 'sales_price']
    search_fields = ['name', 'company_name']
    list_filter = ['material_type']
    ordering = ['name', 'company_name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Bifocal)
class BifocalAdmin(admin.ModelAdmin):
    list_display = ['name', 'company_name', 'material_type', 'index', 'spherical', 'cylindrical', 'axis', 'add', 'pair']
    search_fields = ['name', 'company_name']
    list_filter = ['material_type']
    ordering = ['name', 'company_name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ContactLens)
class ContactLensAdmin(admin.ModelAdmin):
    list_display = ['name', 'company_name', 'spherical', 'cylindrical', 'axis', 'base_curve', 'diameter', 'pair']
    search_fields = ['name', 'company_name']
    ordering = ['name', 'company_name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Progressive)
class ProgressiveAdmin(admin.ModelAdmin):
    list_display = ['name', 'company_name', 'material_type', 'index', 'spherical', 'cylindrical', 'axis', 'add', 'side', 'pair']
    search_fields = ['name', 'company_name']
    list_filter = ['side', 'material_type']
    ordering = ['name', 'company_name']
    readonly_fields = ['created_at', 'updated_at']
