import requests
import json
import base64
from dotenv import load_dotenv
import os


def init(path):
    load_dotenv()
    def encode_image_to_base64(path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    API_KEY = os.getenv("VISION_KEY")

    # Encode the image
    image_base64 = encode_image_to_base64(rf"{path}")

    # Prepare the request payload
    url = f"https://vision.googleapis.com/v1/images:annotate?key={API_KEY}"
    headers = {"Content-Type": "application/json"}

    payload = {
        "requests": [
            {
                "image": {"content": image_base64},
                "features": [{"type": "TEXT_DETECTION"}]
            }
        ]
    }

    # Send the request
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    data = []

    if "textAnnotations" in result["responses"][0]:
        data.append(result["responses"][0]["textAnnotations"][0]["description"])
    else:
        print("No text found or error:", result)
    

    return data


