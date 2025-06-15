import os
import sys
import json
import requests
from dotenv import load_dotenv
from utils.converter import convert_pdf_to_image, load_image_bytes
from utils.openai_vision import extract_invoice_data

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_ENDPOINT = "https://jsonplaceholder.typicode.com/posts"
SUPPORTED_IMAGE_TYPES = [".png", ".jpg", ".jpeg", ".webp"]

def main(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, "invoice_agent", filename)
    ext = os.path.splitext(input_path)[-1].lower()

    if ext == ".pdf":
        input_path = convert_pdf_to_image(input_path)
    elif ext not in SUPPORTED_IMAGE_TYPES:
        return

    image_data = load_image_bytes(input_path)
    extracted_data = extract_invoice_data(image_data, OPENAI_API_KEY)
    requests.post(API_ENDPOINT, json=extracted_data)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("sample_invoice.pdf")


