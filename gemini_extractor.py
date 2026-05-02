import google.generativeai as genai
from config import GEMINI_API_KEY
import json
import os
import re

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

PROMPT = """
Extract the following details from the electricity bill:

- Consumer ID
- Customer Name
- Billing Date
- Units Consumed
- Total Amount
- Due Date

Return ONLY valid JSON.
Do not include markdown, code blocks, or the word 'json'.

Format:
{
  "consumer_id": "",
  "name": "",
  "billing_date": "",
  "units": "",
  "amount": "",
  "due_date": ""
}

If any field is missing, return null.
"""


def extract_from_file(file_path):
    mime_type = get_mime_type(file_path)

    with open(file_path, "rb") as f:
        file_data = f.read()

    response = model.generate_content([
        PROMPT,
        {
            "mime_type": mime_type,
            "data": file_data
        }
    ])

    return clean_json(response.text)


def get_mime_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".png", ".jpg", ".jpeg"]:
        return "image/png"
    elif ext == ".pdf":
        return "application/pdf"
    else:
        raise ValueError("Unsupported file type")


def clean_json(text):
    try:
        text = text.strip()

        # Extract JSON block
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            text = match.group()

        return json.loads(text)

    except Exception as e:
        print("JSON parsing error:", e)
        return {"error": "Invalid JSON", "raw": text}