import google.generativeai as genai
from .prompts import INQUISITOR_SYSTEM_PROMPT
from .config import MODEL_NAME

class Inquisitor:
    def __init__(self, api_key):
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(MODEL_NAME, system_instruction=INQUISITOR_SYSTEM_PROMPT)
            self.chat_session = None
        else:
            self.model = None

    def start_interrogation(self, context_data):
        if not self.model:
            return "Error: API Key missing."
        
        history = [
            {"role": "user", "parts": [f"Here is the current intelligence data on the target:\n{context_data}\n\nReview this and ask me about any missing critical information."]}
        ]
        self.chat_session = self.model.start_chat(history=history)
        response = self.chat_session.send_message("Proceed.")
        return response.text

    def send_reply(self, user_input):
        if not self.chat_session:
            return "Error: Session not started."
        
        try:
            response = self.chat_session.send_message(user_input)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

