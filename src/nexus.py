import google.generativeai as genai
from .prompts import NEXUS_SYSTEM_PROMPT
from .config import MODEL_NAME

class NexusController:
    def __init__(self, api_key):
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(MODEL_NAME, system_instruction=NEXUS_SYSTEM_PROMPT)
        else:
            self.model = None

    def analyze_input(self, input_data, input_type):
        if not self.model:
            return "Error: API Key missing."
        
        prompt = f"INPUT TYPE: {input_type}\nINPUT DATA: {input_data}\n\nDECIDE STRATEGY."
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Nexus Error: {str(e)}"

