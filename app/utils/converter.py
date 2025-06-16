import os
from PIL import Image

def convert_pdf_to_image_pymupdf(pdf_path):
    """Convert PDF using PyMuPDF (fitz) - Primary method"""
    try:
        import fitz  # PyMuPDF

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        try:
            doc = fitz.open(pdf_path)
        except AttributeError:
            try:
                doc = fitz.Document(pdf_path)
            except AttributeError:
                raise RuntimeError("PyMuPDF installation is corrupted")

        if doc.page_count == 0:
            raise RuntimeError("PDF has no pages")

        page = doc.load_page(0)
        pix = page.get_pixmap(dpi=200)
        image_path = pdf_path.replace(".pdf", ".png")
        pix.save(image_path)
        doc.close()

        return image_path

    except ImportError:
        raise ImportError("PyMuPDF not installed. Install with: pip install PyMuPDF")
    except Exception as e:
        raise RuntimeError(f"PyMuPDF conversion failed: {str(e)}")

def convert_pdf_to_image_pdf2image(pdf_path):
    """Convert PDF using pdf2image - Backup method"""
    try:
        from pdf2image import convert_from_path

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        pages = convert_from_path(pdf_path, first_page=1, last_page=1, dpi=200, fmt='PNG')
        if not pages:
            raise RuntimeError("No pages extracted from PDF")

        image_path = pdf_path.replace(".pdf", ".png")
        pages[0].save(image_path, 'PNG', optimize=True)

        return image_path

    except ImportError:
        raise ImportError("pdf2image not installed. Install with: pip install pdf2image")
    except Exception as e:
        raise RuntimeError(f"pdf2image conversion failed: {str(e)}")

def convert_pdf_to_image(pdf_path):
    """Main PDF conversion function with fallback methods"""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if not pdf_path.lower().endswith('.pdf'):
        raise ValueError(f"File is not a PDF: {pdf_path}")

    methods = [
        ("PyMuPDF (fitz)", convert_pdf_to_image_pymupdf),
        ("pdf2image", convert_pdf_to_image_pdf2image)
    ]

    last_error = None

    for _, method_func in methods:
        try:
            result = method_func(pdf_path)
            if os.path.exists(result) and os.path.getsize(result) > 0:
                return result
            else:
                raise RuntimeError("Output file was not created or is empty")
        except Exception as e:
            last_error = e
            continue

    error_msg = f"All PDF conversion methods failed. Last error: {last_error}"
    error_msg += "\n\n Try these solutions:"
    error_msg += "\n1. pip install PyMuPDF"
    error_msg += "\n2. pip install pdf2image"
    error_msg += "\n3. Check if the PDF file is corrupted"
    error_msg += "\n4. Try converting the PDF manually first"

    raise RuntimeError(error_msg)

def load_image_bytes(image_path):
    """Load image file as bytes for AI processing"""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    if os.path.getsize(image_path) == 0:
        raise RuntimeError(f"Image file is empty: {image_path}")

    try:
        with open(image_path, "rb") as f:
            data = f.read()
        if len(data) == 0:
            raise RuntimeError("No data read from image file")
        return data
    except Exception as e:
        raise RuntimeError(f"Failed to load image bytes: {str(e)}")

def validate_image(image_path):
    """Validate that the image file is readable and valid"""
    try:
        with Image.open(image_path) as img:
            img.verify()
            return True
    except Exception:
        return False

def get_image_info(image_path):
    """Get information about the image file"""
    try:
        with Image.open(image_path) as img:
            return {
                "format": img.format,
                "mode": img.mode,
                "size": img.size,
                "file_size": os.path.getsize(image_path)
            }
    except Exception as e:
        return {"error": str(e)}
    


