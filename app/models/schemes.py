from pydantic import BaseModel

class PDFResponse(BaseModel):
    pdf_id: str
    message: str = "PDF uploaded successfully"

class ErrorResponse(BaseModel):
    detail: str

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str