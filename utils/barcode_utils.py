# barcode module, used for generating various types of barcode.
from barcode import Code128

# ImageWriter is used for generating barcode images.
from barcode.writer import ImageWriter

# BytesIO provides a binary stream interface for in-memory byter buffers.
from io import BytesIO
from django.core.files.base import ContentFile

def generate_barcode(code: str, filename: str = None):
    if not filename:
        filename = f"{code}.png"

    buffer = BytesIO()
    barcode = Code128(code, writer=ImageWriter())
    barcode.write(buffer)

    return filename, ContentFile(buffer.getvalue())

