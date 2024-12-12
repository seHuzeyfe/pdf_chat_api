import pytest
from app.services.chat_service import ChatService
from app.services.pdf_service import PDFService
import os

@pytest.mark.asyncio
async def test_chat_service_validate_pdf_exists(test_storage, test_pdf):
    # Arrange
    pdf_service = PDFService()
    chat_service = ChatService(pdf_service)
    
    # Create test PDF with a known name
    test_file_name = "test123.pdf"  # Use a specific name
    test_pdf_path = os.path.join(test_storage, test_file_name)
    with open(test_pdf_path, "wb") as f:
        f.write(test_pdf)
    
    # Act & Assert
    # Extract just the filename without .pdf
    file_id = test_file_name.replace('.pdf', '')
    assert await chat_service.validate_pdf_exists(file_id) is True

@pytest.mark.asyncio
async def test_chat_service_generate_response(test_storage, test_pdf, mocker):
    # Arrange
    pdf_service = PDFService()
    chat_service = ChatService(pdf_service)
    
    # Mock Gemini API response
    mock_response = mocker.Mock()
    mock_response.text = "Test response"
    mocker.patch.object(
        chat_service.model,
        'generate_content',
        return_value=mock_response
    )
    
    # Create test PDF
    test_pdf_path = os.path.join(test_storage, "test.pdf")
    with open(test_pdf_path, "wb") as f:
        f.write(test_pdf)
    
    # Act
    response = await chat_service.generate_response("test", "What is this about?")
    
    # Assert
    assert response == "Test response"