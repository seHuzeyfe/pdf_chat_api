# PDF Chat API

A FastAPI-based service that enables users to chat with PDF documents using Google's Gemini LLM.

## Features

- PDF document upload and processing
- Interactive chat functionality using Gemini API
- Robust error handling and logging
- Comprehensive test coverage
- Secure API key management

## Tech Stack

- FastAPI
- Python 3.12+
- Google Gemini API
- PyPDF2
- pytest for testing

## Prerequisites

- Python 3.12 or higher
- Google Gemini API key

## Install dependencies

- create virtual environment > python -m venv pdf_chat_api_venv
- activate environment > pdf_chat_api_venv\Scripts\activate
- pip install -r requirements.txt
- Redis
    - on Linux : sudo apt-get install redis-server
    - on Windows Windows Subsystem for Linux install WSL

# Gemini API key

- Add your Gemini API key in .env file
- GEMINI_API_KEY=your_api_key_here

# Project Structure
pdf_chat_api/
├── app/                # Application package
│   ├── api/            # API endpoints
│   │   └── v1/         # API version 1
│   ├── core/           # Core functionality
│   ├── models/         # Data models
│   └── services/       # Business logic
├── tests/              # Test suite
├── docs/               # Documentation
└── storage/            # PDF storage
└── logs/               # Logs

- Check docs/technical_doc.md file for more details.

# Test

- Unit testing and integration testing applied
- Run in root directory > pytest --cov=app -v

# API Documentation

- Start the server > uvicorn main:app --reload
- Swagger UI : open http://127.0.0.1:8000/docs on browser

- POST /api/v1/pdf/upload : (upload a pdf file)
    - Response : {
                    "pdf_id": "unique_identifier",
                    "message": "PDF uploaded successfully"
                 }

- POST /api/v1/chat/{pdf_id}
    -  {
            "message": "What is this document about?"
       }
    -  {
            "response": "AI-generated response about the PDF content"
       }
### The API implements comprehensive error handling:

- 400: Bad Request (invalid file type, size limit exceeded)
- 404: Not Found (PDF not found)
- 500: Internal Server Error

### Configuration
- GEMINI_API_KEY: Google Gemini API key
- DEBUG: Enable debug mode (True/False)
- MAX_FILE_SIZE: Maximum PDF file size (bytes)

# Logging
- Logs are stored in logs/app.log with the following levels:
    - INFO: General application flow
    - ERROR: Application errors
    - DEBUG: Detailed debugging information

# Cache
- Redis used for caching
- Open Redis CLI : redis-cli
- List all keys : KEYS *
- Get specific cache entry : GET "chat:your_pdf_id:your_query_hash"
- Check TTL of a key : TTL "chat:your_pdf_id:your_query_hash"


