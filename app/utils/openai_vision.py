import base64
import json
from openai import OpenAI

def extract_invoice_data(image_bytes, api_key):
    client = OpenAI(api_key=api_key)
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    prompt = """
You are an intelligent invoice parser. Extract the following fields in JSON format:
{
  "vendor": "",
  "invoice_number": "",
  "invoice_date": "",
  "line_items": [
    {
      "description": "",
      "quantity": "",
      "unit_price": "",
      "total": ""
    }
  ],
  "subtotal": "",
  "tax": "",
  "total_amount": ""
}
If any field is missing, leave it empty. Output only valid JSON.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{encoded_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=1000,
    )
    content = response.choices[0].message.content
    try:
        return json.loads(content)
    except Exception:
        return {
            "error": "Failed to parse JSON from GPT response",
            "raw_response": content
        }


