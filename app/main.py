import os
import sys
import json
import requests
from dotenv import load_dotenv

# Import helper functions from the utils directory
from utils.converter import convert_pdf_to_image, load_image_bytes
from utils.genai_vision import extract_invoice_data
import fitz  # Used for PDF handling

# Load environment variables from the .env file
load_dotenv()

# Placeholder API endpoint to simulate sending extracted invoice data
API_ENDPOINT = "https://jsonplaceholder.typicode.com/posts" 

# Supported image formats for direct processing (no conversion needed)
SUPPORTED_IMAGE_TYPES = [".png", ".jpg", ".jpeg", ".webp"]

def main(filename):
    """Main function to process invoice files"""
    try:
        # Get the absolute path of the current script
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Build the full path to the input file
        input_path = os.path.join(base_dir, filename)

        # Check if the input file exists
        if not os.path.exists(input_path):
            return False

        # Get the file extension (e.g., .pdf, .png)
        ext = os.path.splitext(input_path)[-1].lower()

        # If the file is a PDF, convert it to a PNG image
        if ext == ".pdf":
            try:
                input_path = convert_pdf_to_image(input_path)
            except Exception:
                # If PDF conversion fails, exit
                return False

        # If file type is unsupported (not image or PDF), exit
        elif ext not in SUPPORTED_IMAGE_TYPES:
            return False

        # Try to load the image file as raw bytes
        try:
            image_data = load_image_bytes(input_path)
        except Exception:
            return False

        # Send image data to GenAI for invoice extraction
        try:
            extracted_data = extract_invoice_data(image_data)

            # If data was successfully extracted
            if isinstance(extracted_data, dict) and "error" not in extracted_data:
                try:
                    # Send extracted data to the API endpoint
                    response = requests.post(API_ENDPOINT, json=extracted_data, timeout=30)
                    
                    # If the API returns an error, ignore for now (could be logged)
                    if response.status_code not in [200, 201]:
                        pass  
                except requests.exceptions.RequestException:
                    pass  
            else:
                return False  # If GenAI returned an error
        except Exception:
            return False  # Catch-all for any processing failures

        return True  # All steps completed successfully

    except Exception:
        return False  # Catch any unexpected global errors

# Entry point: allows running the script from command line
if __name__ == "__main__":
    # If a filename is passed as an argument, use it; else, default to sample
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "sample_invoice.pdf"

    # Run the main function
    success = main(filename)

    # Exit with error code 1 if the process failed
    if not success:
        sys.exit(1)
