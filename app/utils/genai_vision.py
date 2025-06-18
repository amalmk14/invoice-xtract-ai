import os
import json
import base64
import oci
import requests
from dotenv import load_dotenv

load_dotenv()

# Get required GenAI configuration from environment
ENDPOINT = os.getenv("GENAI_ENDPOINT", "").rstrip("/")  
MODEL_ID = os.getenv("GENAI_MODEL_ID")                  
TENANCY_ID = os.getenv("GENAI_TENANCY")                 
USER_ID = os.getenv("GENAI_USER")                       
COMPARTMENT_ID = os.getenv("GENAI_COMPARTMENT_ID")      
FINGERPRINT = os.getenv("GENAI_FINGERPRINT")           
REGION = os.getenv("GENAI_REGION")                     
PRIVATE_KEY_PATH = os.path.join(os.getcwd(), "oci_api_key.pem") 

def extract_invoice_data(image_data: bytes):
    """
    Send image data to OCI GenAI endpoint for invoice data extraction.
    Accepts raw image bytes, encodes them to base64, and sends to GenAI model.
    Returns the parsed JSON response or error info.
    """

    try:
        # Prepare the signer for OCI authentication using the above credentials
        signer = oci.signer.Signer(
            tenancy=TENANCY_ID,
            user=USER_ID,
            fingerprint=FINGERPRINT,
            private_key_file_location=PRIVATE_KEY_PATH
        )

        # Convert raw image bytes into base64-encoded string (required by GenAI)
        image_base64 = base64.b64encode(image_data).decode("utf-8")

        # Create the JSON payload to send to GenAI's inference API
        payload = {
            "compartmentId": COMPARTMENT_ID,
            "modelId": MODEL_ID,
            "servingMode": "HTTPS",  # Specifies how the model is being accessed
            "inferenceRequest": {
                "input": {
                    "mimeType": "image/png",  # Format of the image
                    "content": image_base64   # Encoded image content
                }
            }
        }

        # Set HTTP headers to indicate we are sending JSON
        headers = {
            "Content-Type": "application/json"
        }

        # Send POST request to GenAI inference API with image payload
        response = requests.post(
            url=f"{ENDPOINT}/20231130/actions/inference",  
            auth=signer,                                   
            headers=headers,                               
            json=payload,                                  
            timeout=60                                   
        )

        # If request was successful (200 OK or 201 Created), return the result as JSON
        if response.status_code in [200, 201]:
            return response.json()
        else:
            # If response was not successful, return a formatted error
            return {
                "error": f"GenAI API call failed: {response.status_code} {response.text}",
                "error_type": "APIError"
            }

    except Exception as e:
        # If any unexpected error occurs (like timeout, missing env, etc.), return it
        return {
            "error": f"GenAI API call failed: {e}",
            "error_type": type(e).__name__
        }
