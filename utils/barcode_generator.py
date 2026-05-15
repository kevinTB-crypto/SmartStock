import barcode
from barcode.writer import ImageWriter
from io import BytesIO

def generar_codigo(codigo):
    ean = barcode.get("code128", str(codigo), writer=ImageWriter())
    buffer = BytesIO()
    ean.write(buffer)
    return buffer