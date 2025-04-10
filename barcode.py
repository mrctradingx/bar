import pdf417gen
from PIL import Image
import base64
from io import BytesIO

def generate_barcode_image(token):
    codes = pdf417gen.encode(token, columns=6, security_level=5)
    image = pdf417gen.render_image(codes)  # PIL Image
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()
