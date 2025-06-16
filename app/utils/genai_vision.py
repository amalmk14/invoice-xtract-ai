import os
import json
import base64
import oci
import requests
from dotenv import load_dotenv

load_dotenv()

# Load config from environment variables
ENDPOINT = os.getenv("GENAI_ENDPOINT", "").rstrip("/")
MODEL_ID = os.getenv("GENAI_MODEL_ID")
TENANCY_ID = os.getenv("GENAI_TENANCY")
USER_ID = os.getenv("GENAI_USER")
COMPARTMENT_ID = os.getenv("GENAI_COMPARTMENT_ID")
FINGERPRINT = os.getenv("GENAI_FINGERPRINT")
REGION = os.getenv("GENAI_REGION")
PRIVATE_KEY_PATH = os.path.join(os.getcwd(), "oci_api_key.pem")


def extract_invoice_data(image_data: bytes):

    try:
        # Prepare signer config
        signer = oci.signer.Signer(
            tenancy=TENANCY_ID,
            user=USER_ID,
            fingerprint=FINGERPRINT,
            private_key_file_location=PRIVATE_KEY_PATH
        )

        # Encode image to base64 string
        image_base64 = base64.b64encode(image_data).decode("utf-8")

        # Prepare request body
        payload = {
            "compartmentId": COMPARTMENT_ID,
            "modelId": MODEL_ID,
            "servingMode": "HTTPS",
            "inferenceRequest": {
                "input": {
                    "mimeType": "image/png",
                    "content": image_base64
                }
            }
        }

        headers = {
            "Content-Type": "application/json"
        }

        # Make the request
        response = requests.post(
            url=f"{ENDPOINT}/20231130/actions/inference",
            auth=signer,
            headers=headers,
            json=payload,
            timeout=60
        )

        # Return result
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return {
                "error": f"GenAI API call failed: {response.status_code} {response.text}",
                "error_type": "APIError"
            }

    except Exception as e:
        return {
            "error": f"GenAI API call failed: {e}",
            "error_type": type(e).__name__
        }
