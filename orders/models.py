from django.db import models
from datetime import date
from phonenumber_field.modelfields import PhoneNumberField

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


class Doctor(models.Model):
    DESIGNATIONS = (
        ('Dr.', 'Dr.'),
        ('Optician', 'Optician'),
    )
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=20, choices=DESIGNATIONS)
    hospital_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.designation} {self.name}\n{self.hospital_name}\n{self.city}"

class Prescription(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    checkup_date = models.DateField(default=date.today)

    # Distance vision presctiption
    distance_sphere = models.FloatField()
    distance_cylinder = models.FloatField()
    distance_axis = models.FloatField()
    distance_va = models.IntegerField()

    # Near vision prescription
    near_sphere = models.FloatField()
    near_cylinder = models.FloatField()
    near_axis = models.FloatField()
    near_va = models.IntegerField()

    # Additional magnifying power prescription for bifocal or progressive lens
    additional_sphere = models.FloatField()

    # Contact Lens values (if any)
    contact_sphere = models.FloatField()
    contact_cylinder = models.FloatField()
    contact_axis = models.FloatField()
    contact_va = models.IntegerField()

    # Pupilary Distance Adjustments
    pd_right = models.FloatField()
    pd_left = models.FloatField()

    @property
    def pd_total(self):
        return self.pd_right + self.pd_left

    def __str__(self):
        return f"Rx for {self.customer}"


class Order(models.Model):
    PRODUCTS = (
        ('Full Specs', 'Full Specs (frame with power)'),
        ('Only Frame/Sunglasses', 'Only Frame/Sunglasses'),
        ('Only Lens/Contact Lens', 'Only Lens/Contact Lens'),
    )

    PAYMENT_METHODS = (
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('Upi', 'Upi'),
        ('Bank Transfer', 'Bank Transfer'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    prescription = models.ForeignKey(Prescription, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(default=date.today)
    product_purchased = models.CharField(max_length=100, choices=PRODUCTS)
    discount = models.FloatField(default=0.0)
    advancePaid = models.FloatField(default=0.0)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    medicines = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.pk} for {self.customer}"


