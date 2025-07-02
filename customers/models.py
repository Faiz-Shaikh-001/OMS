from datetime import date
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

# Create your models here.
class Customer(models.Model):
    GENDERS = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Do not specify', 'Do not specify'),
    )

    AGE_GROUP = (
        ('Children (0-14)', 'Children'),
        ('Youth (15-24)', 'Youth'),
        ('Adult (25-59)', 'Adult'),
        ('Senior (60+)', 'Senior'),
    )

    customer_image = models.ImageField(blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20, choices=GENDERS)
    age_group = models.CharField(max_length=20, choices=AGE_GROUP)
    city = models.CharField(max_length=100)
    phone_number = PhoneNumberField(unique=True, null=False, blank=False)
    second_phone_number = PhoneNumberField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}\n{self.city}\n{self.phone_number}\n{self.second_phone_number}"
