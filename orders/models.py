from django.db import models
from datetime import date
from customers.models import Customer
from prescription.models import Prescription

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


