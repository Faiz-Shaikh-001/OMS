from django.db import models
from utils.barcode_utils import generate_barcode

# Create your models here.
class BarcodeModel(models.Model):
    barcode_image = models.ImageField(upload_to='images/barcodes/', blank=True)

    class Meta:
        abstract = True  # Doesn't create a database table

    def save(self, *args, **kwargs):
        if not self.barcode_image:
            filename, content = generate_barcode(self.get_product_code())
            self.barcode_image.save(filename, content, save=False)

        return super().save(*args, **kwargs)

    def get_product_code(self):
        return "UNKNOWN"
