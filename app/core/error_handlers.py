from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.logging import logger

class PDFChatException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

async def pdf_chat_exception_handler(request: Request, exc: PDFChatException):
    logger.error(f"PDFChatException: {exc.message}",
                 extra = {
                     "path": request.url.path,
                     "method": request.method,
                     "status_code": exc.status_code
                 })
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

# Custom middleware for request logging
async def log_request_middleware(requet: Request, call_next):
    logger.info(f"Request started",
                extra={
                    "path": requet.url.path,
                    "method": requet.method,
                    "client_host": requet.client.host if requet.client else None
                })
    
    try:
        response = await call_next(requet)
        logger.info(f"Request complated",
                    extra={
                        "path": requet.url.path,
                        "status_code": response.status_code
                    })
        return response
    except Exception as e:
        logger.error(f"Request failed: {str(e)}",
                     extra={
                         "path": requet.url.path,
                         "error": str(e)
                     })
        raise e
    
