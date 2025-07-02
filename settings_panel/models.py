from django.db import models

# Create your models here.
class ShopProfile(models.Model):
    logo = models.ImageField(blank=True)
    signature = models.ImageField(blank=True)

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=100)
    pincode = models.IntegerField()
    telephone_number = models.IntegerField()
    mobile_number = models.IntegerField()
    gst_number = models.CharField(max_length=100)
    cst_number = models.CharField(max_length=100)

    order_confirmation_sms = models.CharField(max_length=1000)
    order_completion_sms = models.CharField(max_length=1000)


class TaxDetail(models.Model):
    TAX_TYPES = (
        ('Tax', 'Tax'),
        ('GST (SGST + CGST)', 'GST (SGST + CGST)'),
        ('GST', 'GST'),
        ('VAT', 'VAT'),
    )

    tax_type = models.CharField(max_length=100, choices=TAX_TYPES)
    spectacles_tax = models.FloatField()
    sunglasses_tax = models.FloatField()
    frame_tax = models.FloatField()
    spectacles_tax = models.FloatField()
    contact_lens_tax = models.FloatField()


class NotificationSetting(models.Model):
    low_stock_alert = models.BooleanField(default=True)
    daily_sales_summary_alert = models.BooleanField(default=False)
    order_reminder_alert = models.BooleanField(default=False)


class HelpSupport(models.Model):
    faq = models.TextField(blank=True, null=True)
    user_guide_link = models.URLField(blank=True, null=True)
    contact_support_email = models.EmailField()
    app_version = models.CharField(max_length=20)
    terms_and_conditions = models.TextField(blank=True)


class AppPreference(models.Model):
    LANGUAGES = LANGUAGE_CHOICES = (
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('mr', 'Marathi'),
        ('gu', 'Gujarati'),
        ('pa', 'Punjabi'),
        ('bn', 'Bengali'),
        ('ta', 'Tamil'),
        ('te', 'Telugu'),
        ('ml', 'Malayalam'),
        ('kn', 'Kannada'),
        ('ur', 'Urdu'),
        ('ne', 'Nepali'),
        ('as', 'Assamese'),
        ('or', 'Odia'),
    )

    CURRENCY_CHOICES = (
        ("INR", "₹ Indian Rupee"),
        ("USD", "$ US Dollar"),
        ("EUR", "€ Euro"),
        ("GBP", "£ British Pound"),
        ("JPY", "¥ Japanese Yen"),
        ("CNY", "¥ Chinese Yuan"),
        ("AUD", "$ Australian Dollar"),
        ("CAD", "$ Canadian Dollar"),
        ("SGD", "$ Singapore Dollar"),
        ("AED", "د.إ UAE Dirham"),
        ("MYR", "RM Malaysian Ringgit"),
        ("ZAR", "R South African Rand"),
    )

    currency_preference = models.CharField(max_length=100, choices=CURRENCY_CHOICES, default='INR')
    language_preference = models.CharField(max_length=100, choices=LANGUAGES, default='en')
    app_lock_enabled = models.BooleanField(default=False)
    dark_mode = models.BooleanField(default=False)
