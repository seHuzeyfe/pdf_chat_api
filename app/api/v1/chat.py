from fastapi import APIRouter, HTTPException, Depends
from app.services.chat_service import ChatService
from app.services.pdf_service import PDFService
from app.models.schemes import ChatRequest,ChatResponse,ErrorResponse
from app.core.logging import logger

router = APIRouter()

# Dependency Injection
def get_chat_service():
    pdf_service = PDFService()
    return ChatService(pdf_service)

@router.post("/{pdf_id}",
             response_model=ChatResponse,
             responses={
                 404: {"model": ErrorResponse},
                 400: {"model": ErrorResponse}
             })

async def chat_with_pdf(
    pdf_id: str,
    chat_request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    try:
        # Update this line to match the correct method name
        if not await chat_service.validate_pdf_exists(pdf_id):
            raise HTTPException(
                status_code=404,
                detail="PDF not found"
            )
        
        # Generate response
        response = await chat_service.generate_response(
            pdf_id=pdf_id,
            query=chat_request.message
        )

        return ChatResponse(response=response)
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occured while processing your request"
        )