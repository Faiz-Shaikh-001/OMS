from django.db import models
from utils.barcode_utils import generate_barcode

# Create your models here.
class BarcodeModel(models.Model):
    barcode = models.CharField(max_length=100, unique=True, blank=True)
    barcode_image = models.ImageField(upload_to='images/barcodes/', blank=True, unique=True)

    class Meta:
        abstract = True  # Doesn't create a database table

    def save(self, *args, **kwargs):
        product_code = self.get_product_code()

        if not self.barcode:
            self.barcode = product_code

        if not self.barcode_image:
            filename, content = generate_barcode(self.get_product_code())
            self.barcode_image.save(filename, content, save=False)

        return super().save(*args, **kwargs)

    def get_product_code(self):
        return "UNKNOWN"

    def __str__(self):
        return getattr(self, 'barcode', 'No Barcode')
