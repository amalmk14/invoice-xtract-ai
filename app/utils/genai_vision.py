import os
import json
import base64
import oci
from dotenv import load_dotenv
import requests

load_dotenv()

# Load config from environment variables
ENDPOINT = os.getenv("GENAI_ENDPOINT")
MODEL_ID = os.getenv("GENAI_MODEL_ID")
TENANCY_ID = os.getenv("GENAI_TENANCY")
USER_ID = os.getenv("GENAI_USER")
COMPARTMENT_ID = os.getenv("GENAI_COMPARTMENT_ID")
FINGERPRINT = os.getenv("GENAI_FINGERPRINT")
REGION = os.getenv("GENAI_REGION")
PRIVATE_KEY_PATH = os.path.join(os.path.dirname(__file__), "oci_private_key.pem") 



def extract_invoice_data(image_data: bytes):
    try:
        config = {
            "tenancy": os.getenv("GENAI_TENANCY"),
            "user": os.getenv("GENAI_USER"),
            "fingerprint": os.getenv("GENAI_FINGERPRINT"),
            "key_file": os.path.join(os.getcwd(), "oci_api_key.pem"), 
        }

        model_id = os.getenv("GENAI_MODEL_ID")
        compartment_id = os.getenv("GENAI_COMPARTMENT_ID")
        endpoint = os.getenv("GENAI_ENDPOINT").rstrip("/")

        signer = oci.signer.Signer(
            tenancy=config["tenancy"],
            user=config["user"],
            fingerprint=config["fingerprint"],
            private_key_file_location=config["key_file"]
        )

        # Prepare base64 image string
        image_base64 = base64.b64encode(image_data).decode("utf-8")

        body = {
            "compartmentId": compartment_id,
            "modelId": model_id,
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

        print("Making request to OCI GenAI endpoint...")
        response = requests.post(
            url=f"{endpoint}/20231130/actions/inference",
            auth=signer,
            headers=headers,
            json=body,
            timeout=60
        )

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

