#  Invoice Extraction AI (OCR + GenAI)

This project extracts key invoice data from image or PDF files using AI models (OCI GenAI Vision). It processes a given invoice file, extracts data, and sends it to a specified API endpoint.

##  Project Structure

invoice-extractor/
│
├── main.py # Main script to handle the extraction flow
├── .env # Environment variables for secure credentials
├── requirements.txt # Python dependencies
├── oci_api_key.pem # OCI API private key (kept secret)
│
├── utils/
│ ├── converter.py # Converts PDF to image and handles image loading
│ └── genai_vision.py # Interacts with OCI Generative AI Vision API
│
└── sample_invoice.pdf # Example invoice file for testing



##  Features

-  Supports both PDF and image formats (`.pdf`, `.png`, `.jpg`, etc.)
-  Converts PDF to image using PyMuPDF or pdf2image
-  Loads and validates image data
-  Sends image to **Oracle GenAI Vision** model for inference
-  Receives and formats the extracted invoice data
-  Sends final result to a dummy or real API endpoint



##  Requirements

- Python 3.7+
- [Oracle OCI Python SDK](https://pypi.org/project/oci/)
- Environment variables configured via `.env` file



##  .env Configuration

Create a `.env` file in the root directory and add the following:


GENAI_TENANCY=your-tenancy-ocid
GENAI_USER=your-user-ocid
GENAI_FINGERPRINT=your-api-key-fingerprint
GENAI_COMPARTMENT_ID=your-compartment-ocid
GENAI_MODEL_ID=your-model-id
GENAI_ENDPOINT=https://inference.generativeai.region.oci.oraclecloud.com # example
GENAI_REGION=your-region

Also, ensure the file oci_api_key.pem (your private key) is placed in the root directory.


##  How to Run

# Install dependencies
pip install -r requirements.txt

# Run the script (uses default sample_invoice.pdf if no file is passed)
python main.py sample_invoice.pdf
You can also pass other image files:
python main.py invoice.jpg

# Output
Extracted invoice data (as JSON)

Sent to the dummy API: https://jsonplaceholder.typicode.com/posts

You can replace it in main.py with your real backend URL

#  Notes
The GenAI endpoint must be accessible and active for the script to work.

If you're using the free tier, GenAI Vision may not be available.

If the GenAI request fails, the error will be logged in the output (or handled silently if prints are removed).