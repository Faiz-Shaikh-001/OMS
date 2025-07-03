from django.db import models
from datetime import date
from utils.models import BarcodeModel
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import TextChoices
from datetime import datetime as d

def generate_decimal_choices(start, end, step):
    """
    Generate a list of tuples for DecimalField choices.
    Each tuple is (value, string_representation)
    """
    values = []
    current = Decimal(str(start))
    step = Decimal(str(step))
    while current <= Decimal(str(end)):
        values.append((current, str(current)))
        current += step
    return values


# Choices
class FrameTypes(TextChoices):
    RIMLESS = "3 Piece/Rimless"
    HALF_RIMLESS = "Half Rimless/Supra"
    FULL_METAL = "Full metal"
    FULL_SHELL = "Full Shell/Plastic"
    GOGGLES = "Goggles"


class MaterialTypes(TextChoices):
    MINERAL_LENS = "Mineral Lens"
    PLASTIC_LENS = "Plastic Lens"
    POLYCARBONATE_LENS = "Polycarbonate Lens"
    TRIVEX_LENS = "Trivex Lens"
    ORGANIC_LENS = "Organic Lens"


# Frame Model
class Frame(BarcodeModel):
    class Meta:
        verbose_name = "Frame Product"
        verbose_name_plural = "Frame Products"
        ordering = ['name', 'frame_type']

    PRODUCT_PREFIX = 'FRAME'

    FRAME_TYPES_CODES = {
        "3 Piece/Rimless": 1,
        "Half Rimless/Supra": 2,
        "Full metal": 3,
        "Full Shell/Plastic": 4,
        "Goggles": 5,
    }

    date = models.DateField(default=date.today)
    frame_type = models.CharField(max_length=20, choices=FrameTypes.choices, help_text="Frame Type")
    name = models.CharField(max_length=2000, help_text="Product name or description.")
    code = models.CharField(max_length=2000)
    color = models.CharField(max_length=100)
    size = models.IntegerField()
    quantity = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.0)])
    sales_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    def get_product_code(self):
        code = self.FRAME_TYPES_CODES.get(self.frame_type, 0)
        return f"{self.PRODUCT_PREFIX}-{code}-{self.code}-{self.color[:4]}-{self.size}"


class BaseLensProduct(BarcodeModel):
    class Meta:
        abstract = True

    company_name = models.CharField(
        max_length=1000,
        help_text="Manufacture or brand of the lens product.",
        verbose_name="Lens Brand"
    )

    name = models.CharField(
        max_length=100,
        help_text="Product name or description."
    )

    spherical = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        help_text="Spherical power in diopters. 0.00 means Plano."
    )

    cylindrical = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        help_text="Cylindrical power in diopters. Used for astigmatism."
    )

    pair = models.PositiveIntegerField(
        help_text="Number of lens pairs in stock."
    )

    diameter = models.IntegerField(
        help_text="Diameter of the lens in mm."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    purchase_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.0)])
    sales_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.0)])

    PRODUCT_PREFIX = 'LENS'

    def __str__(self):
        return str(self.name)

    def get_product_code(self):
        return "Unknown"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class SingleVision(BaseLensProduct):
    class Meta:
        verbose_name = "Single Vision Lens"
        verbose_name_plural = "Single Vision Lenses"
        ordering = ['name', 'company_name']

    material_type = models.CharField(
        max_length=20,
        choices=MaterialTypes.choices,
        help_text="Material of the lens. Only required for non-contact lenses."
    )

    index = models.IntegerField(
        help_text="Refractive index of the lens material."
    )

    def get_product_code(self):
        return f"{self.PRODUCT_PREFIX}-SV-{self.name[:5].upper()}-{self.company_name[:5].upper()}"


class Bifocal(SingleVision):
    class Meta:
        verbose_name = "Bifocal Lens"
        verbose_name_plural = "Bifocal Lenses"
        ordering = ['name', 'company_name']

    axis = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(180)],
        help_text="Axis of cylindrical power (0-180 degrees). Only applicable for lenses with astigmatism correction."
    )

    add = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        help_text="Additional power for reading. Only for bifocal/progressive lenses."
    )

    def get_product_code(self):
        return f"{self.PRODUCT_PREFIX}-BF-{self.name[:5].upper()}-{self.company_name[:5].upper()}"


class ContactLens(BaseLensProduct):
    class Meta:
        verbose_name = "Contact Lens"
        verbose_name_plural = "Contact Lenses"
        ordering = ['name', 'company_name']

    axis = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(180)],
        help_text="Axis of cylindrical power (0-180 degrees). Only applicable for lenses with astigmatism correction."
    )

    base_curve = models.IntegerField(
        help_text="Base Curve. Only applicable for contact lenses."
    )

    def get_product_code(self):
        return f"{self.PRODUCT_PREFIX}-CL-{self.name[:5].upper()}-{self.company_name[:5].upper()}"


class Progressive(Bifocal):
    class Meta:
        verbose_name = "Progressive Lens"
        verbose_name_plural = "Progressive Lenses"
        ordering = ['name', 'company_name']

    side = models.CharField(
        max_length=20,
        choices=(('RIGHT', 'RIGHT'), ('LEFT', 'LEFT')),
        help_text="Only applicable for progressive lenses."
    )

    def get_product_code(self):
        return f"{self.PRODUCT_PREFIX}-PG-{self.name[:5].upper()}-{self.company_name[:5].upper()}"
