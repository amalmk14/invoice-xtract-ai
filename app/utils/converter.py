

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
            
        # Load first page
        page = doc.load_page(0)
        
        # Render page to pixmap with high DPI for better quality
        pix = page.get_pixmap(dpi=200)
        
        # Generate output path
        image_path = pdf_path.replace(".pdf", ".png")
        
        # Save the image
        pix.save(image_path)
        
        # Clean up
        doc.close()
        
        print(f" PyMuPDF: Converted to {image_path}")
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
        
        # Convert first page only with high DPI
        pages = convert_from_path(
            pdf_path, 
            first_page=1, 
            last_page=1, 
            dpi=200,
            fmt='PNG'
        )
        
        if not pages:
            raise RuntimeError("No pages extracted from PDF")
        
        # Save the first page
        image_path = pdf_path.replace(".pdf", ".png")
        pages[0].save(image_path, 'PNG', optimize=True)
        
        print(f" pdf2image: Converted to {image_path}")
        return image_path
            
    except ImportError:
        raise ImportError("pdf2image not installed. Install with: pip install pdf2image")
    except Exception as e:
        raise RuntimeError(f"pdf2image conversion failed: {str(e)}")

def convert_pdf_to_image(pdf_path):
    """
    Main PDF conversion function with fallback methods
    Tries PyMuPDF first, then pdf2image as backup
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    # Check if it's actually a PDF
    if not pdf_path.lower().endswith('.pdf'):
        raise ValueError(f"File is not a PDF: {pdf_path}")
    
    # Try multiple conversion methods
    methods = [
        ("PyMuPDF (fitz)", convert_pdf_to_image_pymupdf),
        ("pdf2image", convert_pdf_to_image_pdf2image)
    ]
    
    last_error = None
    
    for method_name, method_func in methods:
        try:
            print(f" Trying {method_name}...")
            result = method_func(pdf_path)
            
            # Verify the output file was created and is valid
            if os.path.exists(result) and os.path.getsize(result) > 0:
                return result
            else:
                raise RuntimeError("Output file was not created or is empty")
                
        except Exception as e:
            print(f" {method_name} failed: {e}")
            last_error = e
            continue
    
    # If all methods failed, provide helpful error message
    error_msg = f"All PDF conversion methods failed. Last error: {last_error}"
    error_msg += "\n\n🔧 Try these solutions:"
    error_msg += "\n1. pip install PyMuPDF"
    error_msg += "\n2. pip install pdf2image"
    error_msg += "\n3. Check if the PDF file is corrupted"
    error_msg += "\n4. Try converting the PDF manually first"
    
    raise RuntimeError(error_msg)

def load_image_bytes(image_path):
    """
    Load image file as bytes for AI processing
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    # Check if file is not empty
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
    """
    Validate that the image file is readable and valid
    """
    try:
        with Image.open(image_path) as img:
            # Try to load the image
            img.verify()
            return True
    except Exception as e:
        print(f"⚠️ Image validation failed: {e}")
        return False

def get_image_info(image_path):
    """
    Get information about the image file
    """
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

# Test function
def test_conversion():
    """Test PDF conversion capabilities"""
    print("🧪 Testing PDF conversion capabilities...")
    
    # Test PyMuPDF
    try:
        import fitz
        print(f"✅ PyMuPDF available")
        if hasattr(fitz, 'version'):
            print(f"   Version: {fitz.version}")
        elif hasattr(fitz, '__version__'):
            print(f"   Version: {fitz.__version__}")
    except ImportError:
        print("❌ PyMuPDF not available")
    except Exception as e:
        print(f"⚠️ PyMuPDF issue: {e}")
    
    # Test pdf2image
    try:
        from pdf2image import convert_from_path
        print("✅ pdf2image available")
    except ImportError:
        print("❌ pdf2image not available")
    
    # Test PIL
    try:
        from PIL import Image
        print(f"✅ PIL/Pillow available - Version: {Image.__version__}")
    except ImportError:
        print("❌ PIL/Pillow not available")

if __name__ == "__main__":
    test_conversion()