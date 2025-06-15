import fitz  
from PIL import Image

def convert_pdf_to_image(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    pix = page.get_pixmap(dpi=200)
    image_path = pdf_path.replace(".pdf", ".png")
    pix.save(image_path)
    return image_path

def load_image_bytes(image_path):
    with open(image_path, "rb") as f:
        return f.read()
