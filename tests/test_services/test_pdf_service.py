# tests/test_services/test_pdf_service.py
import pytest
from fastapi import UploadFile
from app.core.config import Settings
from app.services.pdf_service import PDFService
import io
from app.core.config import get_settings

@pytest.mark.asyncio
async def test_pdf_service_save_pdf(test_storage, test_pdf):
    # Arrange
    service = PDFService()
    # Fix: Update UploadFile creation
    file = UploadFile(
        filename="test.pdf",
        file=io.BytesIO(test_pdf),
        headers={"content-type": "application/pdf"}  # Changed from content_type
    )
    
    # Act
    file_id, text_content = await service.save_pdf(file)
    
    # Assert
    assert file_id is not None
    assert len(file_id) > 0
    assert text_content is not None

@pytest.mark.asyncio
async def test_pdf_service_file_size_limit(test_storage):
    # Arrange
    settings = get_settings()
    service = PDFService()
    large_content = b"x" * (settings.MAX_FILE_SIZE + 1)
    
    # Updated UploadFile creation
    file = UploadFile(
        filename="large.pdf",
        file=io.BytesIO(large_content),
        headers={"content-type": "application/pdf"}  # Use headers instead of content_type
    )
    
    # Act & Assert
    with pytest.raises(ValueError, match="File size exceeds maximum limit"):
        await service.save_pdf(file)