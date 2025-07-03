from phonenumber_field.modelfields import PhoneNumberField
from django.db import models


class Customer(models.Model):
    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

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

    customer_image = models.ImageField(
            blank=True,
            null=True,
            verbose_name="Customer Photo",
        )
    first_name = models.CharField(
            max_length=100,
            verbose_name="First name",
            help_text="Enter the customer's first name."
        )
    last_name = models.CharField(
            max_length=100,
            verbose_name="Last name",
            help_text="Enter the customer's last name."
        )
    gender = models.CharField(
            max_length=20,
            choices=GENDERS,
            verbose_name="Gender",
            help_text="Enter the customer's gender."
        )
    age_group = models.CharField(
            max_length=20,
            choices=AGE_GROUP,
            help_text="Select the age group that the customer belongs to."
        )
    city = models.CharField(
            max_length=100,
            help_text="Enter the city the customer is from."
        )
    phone_number = PhoneNumberField(
            unique=True,
            null=False,
            blank=False,
            help_text="Enter the customer's primary phone number."
        )
    second_phone_number = PhoneNumberField(
            null=True,
            blank=True,
            help_text="Enter the customer's secondary phone number."
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.phone_number}"
