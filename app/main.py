

import os
import sys
import json
import requests
from dotenv import load_dotenv
from utils.converter import convert_pdf_to_image, load_image_bytes
from utils.genai_vision import extract_invoice_data
import fitz

# Print PyMuPDF version
print(fitz.__doc__)

# Load environment variables
load_dotenv()

# Configuration
API_ENDPOINT = "https://jsonplaceholder.typicode.com/posts"  # Replace with real API if needed
SUPPORTED_IMAGE_TYPES = [".png", ".jpg", ".jpeg", ".webp"]

def main(filename):
    """Main function to process invoice files"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        input_path = os.path.join(base_dir, filename)

        if not os.path.exists(input_path):
            print(f"❌ Error: File not found: {input_path}")
            return False

        ext = os.path.splitext(input_path)[-1].lower()
        print(f"📄 Processing file: {filename}")
        print(f"🔍 File extension: {ext}")

        if ext == ".pdf":
            print("🔄 Converting PDF to image...")
            try:
                input_path = convert_pdf_to_image(input_path)
                print(f"✅ PDF converted successfully")
            except Exception as e:
                print(f"❌ PDF conversion failed: {e}")
                return False

        elif ext not in SUPPORTED_IMAGE_TYPES:
            print(f"❌ Error: Unsupported file type: {ext}")
            return False

        print("📖 Loading image data...")
        try:
            image_data = load_image_bytes(input_path)
            print(f"✅ Image loaded successfully. Size: {len(image_data):,} bytes")
        except Exception as e:
            print(f"❌ Failed to load image: {e}")
            return False

        print("🤖 Extracting invoice data with AI...")
        try:
            extracted_data = extract_invoice_data(image_data)

            print("\n" + "="*60)
            print("📊 EXTRACTED INVOICE DATA")
            print("="*60)

            if isinstance(extracted_data, dict) and "error" not in extracted_data:
                print(json.dumps(extracted_data, indent=2))

                print(f"\n📤 Sending data to API: {API_ENDPOINT}")
                try:
                    response = requests.post(API_ENDPOINT, json=extracted_data, timeout=30)
                    print(f"📡 API Response Status: {response.status_code}")

                    if response.status_code in [200, 201]:
                        print("✅ Data sent successfully to API")
                    else:
                        print(f"⚠️ API returned unexpected status: {response.text[:200]}")

                except requests.exceptions.RequestException as e:
                    print(f"❌ API request failed: {e}")

            else:
                print("❌ Extraction failed or returned errors:")
                print(json.dumps(extracted_data, indent=2))
                return False

        except Exception as e:
            print(f"❌ Invoice extraction failed: {e}")
            return False

        print(f"\n🎉 Processing completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Invoice Extractor AI")
    print("=" * 40)

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        print(f"📝 Processing file: {filename}")
    else:
        filename = "sample_invoice.pdf"
        print(f"📝 No filename provided. Using default: {filename}")

    success = main(filename)

    if success:
        print("\n✅ All done!")
    else:
        print("\n❌ Processing failed. Check the errors above.")
        sys.exit(1)
