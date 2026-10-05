import google.generativeai as genai

class GeminiDocumentGenerator:
    def __init__(self, api_key: str = None, model_name: str = "gemini-1.5-pro"):
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        self.model_name = model_name

    def generate_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        prompt = (
            f"Generate a comprehensive legal document titled '{document_type}'.\n"
            f"Involved parties: {parties}\n"
            f"Effective Date: {dates}\n"
            f"Terms and conditions: {terms}\n"
            f"Ensure formal legal structure with multiple sections and legal clauses."
        )
        
        model = genai.GenerativeModel(self.model_name)
        response = model.generate_content(prompt)
        return response.text
