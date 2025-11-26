import google.generativeai as genai
import pandas as pd
import json
from .prompts import MIND_FLAYER_SYSTEM_PROMPT
import streamlit as st
from .config import MODEL_NAME

class MindFlayer:
    def __init__(self, api_key):
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(MODEL_NAME, system_instruction=MIND_FLAYER_SYSTEM_PROMPT)
        else:
            self.model = None

    def ingest_file(self, uploaded_file):
        if uploaded_file is None:
            return None
        
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                return df.to_string()
            elif uploaded_file.name.endswith('.txt'):
                return uploaded_file.read().decode("utf-8")
            else:
                return "Unsupported file format."
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def analyze(self, text, input_type="RAW_LOGS"):
        if not self.model:
            return {"error": "API Key not configured."}
        
        if not text:
            return {"error": "No text provided."}

        prompt_prefix = "ANALYZE THIS TARGET DATA:"
        if input_type == "WEB_SCRAPE":
             prompt_prefix = "ANALYZE THIS PUBLIC WEB DATA FOR PERSONALITY SIGNALS:"

        try:
            response = self.model.generate_content(
                f"{prompt_prefix}\n\n{text}",
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            return {"error": f"Gemini Analysis Failed: {str(e)}"}

