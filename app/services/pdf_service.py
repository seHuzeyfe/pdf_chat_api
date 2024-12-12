import os
from typing import Optional
from PyPDF2 import PdfReader
from fastapi import UploadFile
import uuid
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()

class PDFService:
    def __init__(self):
        # Create upload directory if it doesn't exist
        os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
    
    async def save_pdf(self, file: UploadFile) -> tuple[str, str]:
        """
        Save uploaded PDF and extract its text content.
        Returns tuple of (file_id, extracted_text)
        """
        try:
            # Generate unique ID for the PDF
            file_id = str(uuid.uuid4())
            
            # Create file path
            file_path = os.path.join(settings.UPLOAD_FOLDER, f"{file_id}.pdf")
            
            # Save the uploaded file
            content = await file.read()
            if len(content) > settings.MAX_FILE_SIZE:
                raise ValueError("File size exceeds maximum limit")
                
            with open(file_path, "wb") as pdf_file:
                pdf_file.write(content)
            
            # Extract text from PDF
            text_content = self.extract_text(file_path)
            
            logger.info(f"Successfully saved and processed PDF with ID: {file_id}")
            return file_id, text_content
            
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise
    
    def extract_text(self, file_path: str) -> str:
        """Extract text content from a PDF file"""
        try:
            with open(file_path, "rb") as file:
                reader = PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise