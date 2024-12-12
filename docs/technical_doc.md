# PDF Chat API - Technical Documentation

## Main Application Files

### main.py
Entry point of the application. Sets up FastAPI application, includes routers, configures middleware, and initializes core components.

**Key components:**
- FastAPI application initialization
- CORS middleware configuration
- Router registration
- Lifespan event handlers

## Core Components (`app/core/`)

### config.py
Manages application configuration using Pydantic. Handles environment variables and application settings.

**Key components:**
- Settings class with Pydantic
- Environment variable management
- Application constants (MAX_FILE_SIZE, UPLOAD_FOLDER, etc.)

### logging.py
Implements structured logging with JSON formatting for better log management.

**Key components:**
- Custom JSON formatter
- File and console logging handlers
- Log level configuration

### error_handlers.py
Custom error handling middleware and exception handlers.

**Key components:**
- Custom exception classes
- Error handling middleware
- Request/response logging

## API Endpoints (`app/api/v1/`)

### pdf.py
Handles PDF upload functionality.

**Key components:**
- Upload endpoint (/upload)
- File validation
- PDF processing initialization

### chat.py
Manages chat interactions with uploaded PDFs.

**Key components:**
- Chat endpoint (/chat/{pdf_id})
- Query processing
- Response generation

## Services (`app/services/`)

### pdf_service.py
Handles PDF processing and storage.

**Key components:**
- PDF text extraction
- File storage management
- Validation checks

### chat_service.py
Manages interactions with Gemini API and chat functionality.

**Key components:**
- Gemini API integration
- Context management
- Response generation

## Models (`app/models/`)

### schemas.py
Defines Pydantic models for request/response validation.

**Key components:**
- Request models
- Response models
- Validation rules

## Test Files (`tests/`)

### test_api/test_endpoints.py
Tests for API endpoints.

**Key components:**
- Upload endpoint tests
- Chat endpoint tests
- Error handling tests

### test_services/test_pdf_service.py
Tests for PDF processing service.

**Key components:**
- PDF upload tests
- Text extraction tests
- Error handling tests

### test_services/test_chat_service.py
Tests for chat functionality.

**Key components:**
- Chat response tests
- Gemini API integration tests
- Error handling tests

### conftest.py
Test fixtures and configurations.

**Key components:**
- Test client setup
- Mock data
- Shared fixtures

## Configuration Files

### requirements.txt
Lists all Python dependencies:
```plaintext
fastapi
uvicorn
python-multipart
PyPDF2
google-generativeai
pytest
...