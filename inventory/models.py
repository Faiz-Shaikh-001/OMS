from django.db import models
from datetime import date
from utils.models import BarcodeModel

class Frame(BarcodeModel):
    FRAME_TYPES = (
        ("3 Piece/Rimless", "3 Piece/Rimless"),
        ("Half Rimless/Supra", "Half Rimless/Supra"),
        ("Full metal", "Full metal"),
        ("Full Shell/Plastic", "Full Shell/Plastic"),
        ("Goggles", "Goggles"),
    )

    FRAME_TYPES_CODES = {
        "3 Piece/Rimless": 1,
        "Half Rimless/Supra": 2,
        "Full metal": 3,
        "Full Shell/Plastic": 4,
        "Goggles": 5,
    }

    date = models.DateField(default=date.today)
    frame_type = models.CharField(max_length=20, choices=FRAME_TYPES)
    name = models.CharField(max_length=2000)
    code = models.CharField(max_length=2000)
    color = models.CharField(max_length=100)
    size = models.IntegerField()
    quantity = models.IntegerField()
    purchase_price = models.FloatField()
    sales_price = models.FloatField()

    def __str__(self):
        return str(self.name)

    def get_product_code(self):
        code = self.FRAME_TYPES_CODES.get(self.frame_type, 0)
        return f"FRAME-{code}-{self.code}-{self.color[:4]}-{self.size}"


class LensProduct(BarcodeModel):
    LENS_TYPES = (
        ("Single Vision", "Single Vision"),
        ("Bifocal", "Bifocal"),
        ("Contact Lens", "Contact Lens"),
        ("Progressive", "Progressive"),
    )

    MATERIAL_TYPES = (
        ("Mineral Lens", "Mineral Lens"),
        ("Plastic Lens", "Plastic Lens"),
        ("Polycarbonate Lens", "Polycarbonate Lens"),
        ("Trivex Lens", "Trivex Lens"),
        ("Organic Lens", "Organic Lens"),
    )

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

    lens_type = models.CharField(max_length=20, choices=LENS_TYPES)
    company_name = models.CharField(max_length=1000)
    product_name = models.CharField(max_length=1000)
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPES, blank=True, null=True)
    side = models.CharField(max_length=20, choices={'RIGHT': 'RIGHT', 'LEFT': 'LEFT'}, blank=True, null=True)
    b_c = models.IntegerField(blank=True, null=True)
    index = models.IntegerField(blank=True, null=True)
    dia = models.IntegerField()
    spherical = models.FloatField()
    cylindrical = models.FloatField()
    axis = models.FloatField(blank=True, null=True)

    # Implementation pending...
    add = models.FloatField(blank=True, null=True)

    pair = models.IntegerField()
    purchase_price = models.FloatField()
    sales_price = models.FloatField()

    def __str__(self):
        return str(self.product_name)

    def get_product_code(self):
        lens_type_code = self.LENS_TYPES_CODES.get(self.lens_type, 0)
        material_type_code = self.MATERIAL_TYPES_CODES.get(self.material_type, 0)
        return f"LENS-{lens_type_code}-{self.product_name[:5]}-{self.company_name[:5]}-{material_type_code}"
