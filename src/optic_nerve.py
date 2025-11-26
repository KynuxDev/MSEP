import google.generativeai as genai
from PIL import Image
from .prompts import OPTIC_NERVE_SYSTEM_PROMPT
from .config import VISION_MODEL_NAME

class OpticNerve:
    def __init__(self, api_key):
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(VISION_MODEL_NAME, system_instruction=OPTIC_NERVE_SYSTEM_PROMPT)
        else:
            self.model = None

    def analyze_image(self, image_file):
        if not self.model:
            return "Error: API Key missing."
        
        try:
            image = Image.open(image_file)
            response = self.model.generate_content(
                ["ANALYZE THIS IMAGE FOR INTEL:", image]
            )
            return response.text
        except Exception as e:
            return f"Image Analysis Failed: {str(e)}"

