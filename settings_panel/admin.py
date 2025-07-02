from django.contrib import admin
from .models import ShopProfile, TaxDetail, NotificationSetting, HelpSupport, AppPreference

@admin.register(ShopProfile)
class ShopProfileAdmin(admin.ModelAdmin):
    list_display = ['logo' ,'signature', 'name', 'address', 'city', 'pincode', 'telephone_number', 'mobile_number', 'gst_number', 'cst_number', 'order_confirmation_sms', 'order_completion_sms']


@admin.register(TaxDetail)
class TaxDetailAdmin(admin.ModelAdmin):
    list_display = ['tax_type', 'spectacles_tax', 'sunglasses_tax', 'frame_tax', 'spectacles_tax', 'contact_lens_tax']


@admin.register(NotificationSetting)
class NotificationSettingAdmin(admin.ModelAdmin):
    list_display = ['low_stock_alert', 'daily_sales_summary_alert', 'order_reminder_alert']


@admin.register(HelpSupport)
class HelpSupportAdmin(admin.ModelAdmin):
    list_display = ['faq', 'user_guide_link', 'contact_support_email', 'app_version', 'terms_and_conditions']
    readonly_fields = ['faq', 'user_guide_link', 'contact_support_email', 'app_version', 'terms_and_conditions']

@admin.register(AppPreference)
class AppPreferenceAdmin(admin.ModelAdmin):
    list_display = ['currency_preference', 'language_preference', 'app_lock_enabled', 'dark_mode']
