from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging import logger
from app.core.config import get_settings
from app.core.error_handlers import (
    PDFChatException,
    pdf_chat_exception_handler,
    log_request_middleware
)
from app.api.v1 import pdf, chat

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    logger.info("Starting up PDF Chat API")

    yield
    # Shutdown code
    logger.info("Shutting down pdf Chat API")

app = FastAPI(
    title = settings.PROJECT_NAME,
    description= "An API for chatting with PDF documents",
    version= "1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers=["*"],
)

app.include_router(
    pdf.router,
    prefix=f"{settings.API_V1_STR}/pdf",
    tags=["pdf"]
)

app.include_router(
    chat.router,
    prefix=f"{settings.API_V1_STR}/chat",
    tags=["chat"]
)


@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "Welcome to PDF Chat API"}

app.add_exception_handler(PDFChatException, pdf_chat_exception_handler)

app.middleware("http")(log_request_middleware)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

