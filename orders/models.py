from django.db import models
from datetime import date
from customers.models import Customer
from prescription.models import Prescription
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import TextChoices
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

class ProductTypes(TextChoices):
    FULL_SPECS = "Full Specs (frame with power)"
    ONLY_FRAME_OR_SUNGLASSES = "Only Frame/Sunglasses"
    ONLY_LENS_OR_CONTACT_LENS = "Only Lens/Contact Lens"

class PaymentMethods(TextChoices):
    CASH = "Cash"
    CARD = "Card"
    UPI = "Upi"
    BANK_TRANSFER = "Bank Transfer"

class Order(models.Model):
    customer = models.ForeignKey(
            Customer,
            on_delete=models.CASCADE,
            help_text="Select the customer placing this order."
        )
    prescription = models.ForeignKey(
            Prescription,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            help_text="Attach a prescription if applicable (optional)."
        )
    date = models.DateField(
            default=date.today,
            help_text="Date when the order was placed."
        )
    product_purchased = models.CharField(
            max_length=100,
            choices=ProductTypes.choices,
            help_text="Select the type of product purchased in this order."
        )
    discount = models.DecimalField(
            max_digits=3,
            decimal_places=2,
            default=0.0,
            help_text="Any discount applied to this order (₹)."
        )
    advancePaid = models.DecimalField(
            max_digits=8,
            decimal_places=2,
            default=0.0,
            help_text="Advance payment received for the order (₹)."
        )
    payment_method = models.CharField(
            max_length=20,
            choices=PaymentMethods.choices,
            help_text="Mode of payment used for this order."
        )
    medicines = models.CharField(
            max_length=1000,
            blank=True,
            null=True,
            help_text="Optional: list of medicines included in this order."
        )
    total = models.DecimalField(
            default=0.0,
            max_digits=8,
            decimal_places=2,
            validators=[MinValueValidator(0.0)],
            editable=False,
            help_text="Automatically calculated total price of all items (₹)."
        )
    final_amount = models.DecimalField(
            default=0.0,
            max_digits=8,
            decimal_places=2,
            validators=[MinValueValidator(0.0)],
            editable=False, help_text="Total after applying discount (₹)."
        )

    def __str__(self):
        return f"Order #{self.pk} for {self.customer}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey("content_type", "object_id")

    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.0)])
    total = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.0)], editable=False)

    def clean(self):
        if hasattr(self.product, 'quantity'):
            if self.quantity > self.product.quantity:
                raise ValidationError(f"Insufficient stock for {self.product}")

    def save(self, *args, **kwargs):
        self.full_clean()
        self.total = self.quantity * self.price
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.quantity} x {self.price} (Order #{self.order.id})"


