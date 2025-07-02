from django.db import models
from datetime import date
from utils.models import BarcodeModel
from utils.is_effectively_filled import is_effectively_filled
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db.models import TextChoices


def generate_decimal_choices(start, end, step):
    """
    Generate a list of tuples for DecimalField choices.
    Each tuple is (value, string_representation)
    """
    values = []
    current = start
    while current <= end:
        values.append((Decimal(str(current)), str(current)))
        current += step
    return values


# Choices
class FrameTypes(TextChoices):
    RIMLESS = "3 Piece/Rimless"
    HALF_RIMLESS = "Half Rimless/Supra"
    FULL_METAL = "Full metal"
    FULL_SHELL = "Full Shell/Plastic"
    GOGGLES = "Goggles"

class LensTypes(TextChoices):
    SINGLE_VISION = "Single Vision"
    BIFOCAL = "Bifocal"
    CONTACT_LENS = "Contact Lens"
    PROGRESSIVE = "Progressive"

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


    def __str__(self):
        return str(self.name)

    def get_product_code(self):
        code = self.FRAME_TYPES_CODES.get(self.frame_type, 0)
        return f"{self.PRODUCT_PREFIX}-{code}-{self.code}-{self.color[:4]}-{self.size}"


# Lens Model
class LensProduct(BarcodeModel):
    class Meta:
        verbose_name = "Lens Product"
        verbose_name_plural = "Lens Products"
        ordering = ['name', 'company_name']

    PRODUCT_PREFIX = 'LENS'

    LENS_TYPES_CODES = {
        "Single Vision": 1,
        "Bifocal": 2,
        "Contact Lens": 3,
        "Progressive": 4,
    }

    MATERIAL_TYPES_CODES = {
        "Mineral Lens": 1,
        "Plastic Lens": 2,
        "Polycarbonate Lens": 3,
        "Trivex Lens": 4,
        "Organic Lens": 5,
    }


    CYLINDER_CHOICES = generate_decimal_choices(-12.75, 12.75, 0.25)
    SPHERE_CHOICES = [(Decimal("0.00"), "Plano")] + generate_decimal_choices(-24.75, -0.25, 0.25) + generate_decimal_choices(0.25, 24.75, 0.25)
    ADD_CHOICES = generate_decimal_choices(0.00, 4.75, 0.25)

    lens_type = models.CharField(
            max_length=20,
            choices=LensTypes.choices,
            help_text="Select the type of lens to automatically validate allowed fields."
        )
    company_name = models.CharField(
            max_length=1000,
            help_text="Manufacturer or brand of the lens product.",
            verbose_name="Lens Brand"
        )
    name = models.CharField(
            default="Unnamed Lens",
            max_length=1000,
            help_text="Product name or description."
        )
    material_type = models.CharField(
            max_length=20,
            choices=MaterialTypes.choices,
            blank=True,
            null=True,
            help_text="Material of the lens. Only required for non-contact lenses."
        )
    side = models.CharField(
            max_length=20,
            choices=(('RIGHT', 'RIGHT'), ('LEFT', 'LEFT')),
            blank=True,
            null=True,
            help_text="Only applicable for progressive lenses."
        )
    base_curve = models.IntegerField(
            blank=True,
            null=True,
            help_text="Base Curve. Only applicable for contact lenses."
        )
    index = models.IntegerField(
            blank=True,
            null=True,
            help_text="Refractive index of the lens material."
        )
    dia = models.IntegerField(
            blank=True,
            null=True,
            help_text="Diameter of the lens in mm."
        )
    spherical = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        choices=SPHERE_CHOICES,
        default=0.0,
        help_text="Spherical power in diopters. 0.00 means Plano."
    )
    cylindrical = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        choices=CYLINDER_CHOICES,
        default=0.0,
        help_text="Cylindrical power in diopters. Used for astigmatism."
    )
    axis = models.DecimalField(
            max_digits=3,
            decimal_places=2,
            blank=True,
            null=True,
            help_text="Axis of cylindrical power (0-180 degrees). Only applicable for lenses with astigmatism correction."
        )
    add = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
        choices=ADD_CHOICES,
        default=0.0,
        help_text="Additional power for reading. Only for bifocal/progressive lenses."
    )

    pair = models.PositiveIntegerField(
        help_text="Number of lens pairs in stock."
    )
    purchase_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.0)])
    sales_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.0)])


    def clean(self):
        errors = {}

        # Set of allowed fields per lens_type
        allowed_fields = {
            "Single Vision": {"index", "dia", "spherical", "cylindrical", "pair", "purchase_price", "sales_price"},
            "Bifocal": {"index", "dia", "spherical", "cylindrical", "axis", "add", "pair", "purchase_price", "sales_price"},
            "Contact Lens": {"base_curve", "dia", "spherical", "cylindrical", "axis", "pair", "purchase_price", "sales_price"},
            "Progressive": {"index", "dia", "spherical", "cylindrical", "axis", "add", "pair", "side", "purchase_price", "sales_price"},
        }

        base_fields = {"company_name", "name"}  # Required for all types
        current_type = self.lens_type

        # If lens_type is invalid or empty, skip validation
        if not current_type or current_type not in allowed_fields:
            return

        # Compute all allowed for current lens type
        allowed = allowed_fields[current_type] | base_fields

        # Collect all model fields with values
        for field in self._meta.fields:
            field_name = field.name
            if field_name in allowed or field.auto_created or field.primary_key:
                continue

            value = getattr(self, field_name)
            if is_effectively_filled(value):
                errors[field_name] = f"'{field_name}' is not allowed for lens type '{current_type}'."

        required_fields = allowed_fields[current_type] | base_fields
        for field in required_fields:
            value = getattr(self, field, None)
            if not is_effectively_filled(value):
                errors[field] = f"'{field}' is required for lens type '{current_type}'."


        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return str(self.name)

    def get_product_code(self):
        lens_type_code = self.LENS_TYPES_CODES.get(self.lens_type, 0)
        material_type_code = self.MATERIAL_TYPES_CODES.get(self.material_type, 0)
        return f"{self.PRODUCT_PREFIX}-{lens_type_code}-{self.name[:5]}-{self.company_name[:5]}-{material_type_code}"
