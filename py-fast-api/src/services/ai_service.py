import os
import google.generativeai as genai

class GenAIService:
    def __init__(self):
        api_key = os.getenv('GEMİNİ_API_KEY')
        if not api_key:
            raise ValueError("API_KEY ortam değişkeni ayarlanmalı!")
        genai.configure(api_key=api_key)

    def generate_summary(self, doc_data):
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = "Summarize this document"
        response = model.generate_content([doc_data, prompt])
        return response.text
