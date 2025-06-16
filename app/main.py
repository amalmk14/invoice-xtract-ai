import os
import sys
import json
import requests
from dotenv import load_dotenv
from utils.converter import convert_pdf_to_image, load_image_bytes
from utils.genai_vision import extract_invoice_data
import fitz

load_dotenv()

API_ENDPOINT = "https://jsonplaceholder.typicode.com/posts" 
SUPPORTED_IMAGE_TYPES = [".png", ".jpg", ".jpeg", ".webp"]

def main(filename):
    """Main function to process invoice files"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        input_path = os.path.join(base_dir, filename)

        if not os.path.exists(input_path):
            return False

        ext = os.path.splitext(input_path)[-1].lower()

        if ext == ".pdf":
            try:
                input_path = convert_pdf_to_image(input_path)
            except Exception:
                return False

        elif ext not in SUPPORTED_IMAGE_TYPES:
            return False

        try:
            image_data = load_image_bytes(input_path)
        except Exception:
            return False

        try:
            extracted_data = extract_invoice_data(image_data)

            if isinstance(extracted_data, dict) and "error" not in extracted_data:
                try:
                    response = requests.post(API_ENDPOINT, json=extracted_data, timeout=30)
                    if response.status_code not in [200, 201]:
                        pass  
                except requests.exceptions.RequestException:
                    pass  
            else:
                return False

        except Exception:
            return False

        return True

    except Exception:
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "sample_invoice.pdf"

    success = main(filename)

    if not success:
        sys.exit(1)
