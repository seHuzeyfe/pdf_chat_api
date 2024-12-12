from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_service import PDFService
from app.models.schemes import PDFResponse, ErrorResponse
from app.core.logging import logger

router = APIRouter()
pdf_service = PDFService()

@router.post("/upload", 
             response_model=PDFResponse,
             responses={400: {"model": ErrorResponse}})
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file for processing.
    """
    # Validate file type
    if not file.content_type == "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )
    
    try:
        file_id, _ = await pdf_service.save_pdf(file)
        return PDFResponse(pdf_id=file_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error uploading PDF: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the PDF"
        )