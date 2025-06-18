import os
from PIL import Image

def convert_pdf_to_image_pymupdf(pdf_path):
    """Convert the first page of a PDF to an image using PyMuPDF (fitz)"""
    try:
        import fitz  # PyMuPDF

        # Check if the PDF file exists
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # Open the PDF file (handle different versions of PyMuPDF)
        try:
            doc = fitz.open(pdf_path)
        except AttributeError:
            try:
                doc = fitz.Document(pdf_path)
            except AttributeError:
                raise RuntimeError("PyMuPDF installation is corrupted")

        # Ensure the PDF has at least one page
        if doc.page_count == 0:
            raise RuntimeError("PDF has no pages")

        # Render the first page to an image
        page = doc.load_page(0)
        pix = page.get_pixmap(dpi=200)

        # Save the image
        image_path = pdf_path.replace(".pdf", ".png")
        pix.save(image_path)
        doc.close()

        return image_path

    # Handle missing library
    except ImportError:
        raise ImportError("PyMuPDF not installed. Install with: pip install PyMuPDF")

    # Handle other errors
    except Exception as e:
        raise RuntimeError(f"PyMuPDF conversion failed: {str(e)}")


def convert_pdf_to_image_pdf2image(pdf_path):
    """Convert the first page of a PDF into an image using pdf2image (backup method)"""
    try:
        from pdf2image import convert_from_path  # Import the library

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")  # Check if file exists

        pages = convert_from_path(pdf_path, first_page=1, last_page=1, dpi=200, fmt='PNG')  # Convert page to image
        if not pages:
            raise RuntimeError("No pages extracted from PDF")  # Check conversion success

        image_path = pdf_path.replace(".pdf", ".png")  # Set image output path
        pages[0].save(image_path, 'PNG', optimize=True)  # Save image

        return image_path  # Return path to saved image

    except ImportError:
        raise ImportError("pdf2image not installed. Install with: pip install pdf2image")  # Missing lib error

    except Exception as e:
        raise RuntimeError(f"pdf2image conversion failed: {str(e)}")  # Handle all other errors


def convert_pdf_to_image(pdf_path):
    """Main PDF conversion function with fallback methods."""
    
    # Check if the provided file path exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    # Check if the file is actually a PDF
    if not pdf_path.lower().endswith('.pdf'):
        raise ValueError(f"File is not a PDF: {pdf_path}")

    # List of conversion methods (primary and fallback)
    methods = [
        ("PyMuPDF (fitz)", convert_pdf_to_image_pymupdf),   # Primary method
        ("pdf2image", convert_pdf_to_image_pdf2image)       # Fallback method
    ]

    last_error = None  # Store the last encountered error

    # Try each method in order
    for _, method_func in methods:
        try:
            result = method_func(pdf_path)  # Attempt to convert
            # Check if the resulting image file exists and is not empty
            if os.path.exists(result) and os.path.getsize(result) > 0:
                return result  # Successful conversion
            else:
                raise RuntimeError("Output file was not created or is empty")
        except Exception as e:
            last_error = e  # Store the error and try the next method
            continue

    # If all methods fail, raise a detailed error message
    error_msg = f"All PDF conversion methods failed. Last error: {last_error}"
    error_msg += "\n\n Try these solutions:"
    error_msg += "\n1. pip install PyMuPDF"
    error_msg += "\n2. pip install pdf2image"
    error_msg += "\n3. Check if the PDF file is corrupted"
    error_msg += "\n4. Try converting the PDF manually first"

    raise RuntimeError(error_msg)



def load_image_bytes(image_path):
    """Load an image file and return its raw bytes, typically for AI or API processing."""

    # Check if the file exists at the given path
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Check if the file exists but is empty (size = 0 bytes)
    if os.path.getsize(image_path) == 0:
        raise RuntimeError(f"Image file is empty: {image_path}")

    try:
        # Open the file in binary mode and read its contents
        with open(image_path, "rb") as f:
            data = f.read()

        # Verify that data was actually read from the file
        if len(data) == 0:
            raise RuntimeError("No data read from image file")

        # Return the image as bytes
        return data

    except Exception as e:
        # Handle any unexpected errors during file reading
        raise RuntimeError(f"Failed to load image bytes: {str(e)}")



    

