import google.generativeai as genai
import json
from .prompts import BLACK_BOX_SYSTEM_PROMPT
from .config import MODEL_NAME

class BlackBox:
    def __init__(self, api_key):
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(MODEL_NAME, system_instruction=BLACK_BOX_SYSTEM_PROMPT)
        else:
            self.model = None

    def generate_report(self, profile):
        if not self.model:
            return "Error: API Key missing."
        
        try:
            response = self.model.generate_content(
                f"GENERATE FINAL DOSSIER FOR PROFILE:\n{json.dumps(profile)}"
            )
            return response.text
        except Exception as e:
            return f"Report Generation Failed: {str(e)}"

