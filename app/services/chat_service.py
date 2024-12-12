import google.generativeai as genai
from typing import Optional
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()
genai.configure(api_key=settings.GEMINI_API_KEY)

class ChatService:
    def __init__(self, pdf_service):
        self.pdf_service = pdf_service
        self.model = genai.GenerativeModel('gemini-pro')
        
    async def generate_response(self, pdf_id: str, query: str) -> str:
        """
        Generate a response based on PDF content and user query
        """
        try:
            # Construct prompt with context
            system_prompt = """You are a helpful AI assistant that answers questions about PDF documents.
            Please provide accurate, relevant information based on the document content provided.
            If the answer cannot be found in the document, please say so."""
            
            # Get PDF content from storage
            pdf_path = f"{settings.UPLOAD_FOLDER}/{pdf_id}.pdf"
            text_content = self.pdf_service.extract_text(pdf_path)
            
            # Construct the full prompt
            full_prompt = f"{system_prompt}\n\nDocument content:\n{text_content}\n\nUser question: {query}"
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating chat response: {str(e)}")
            raise

    async def validate_pdf_exists(self, pdf_id: str) -> bool:
        """Check if PDF exists in storage"""
        import os
        pdf_path = f"{settings.UPLOAD_FOLDER}/{pdf_id}.pdf"
        return os.path.exists(pdf_path)

