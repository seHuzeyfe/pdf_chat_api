import io
import pytest
from fastapi.testclient import TestClient

def test_upload_pdf_endpoint(test_client: TestClient, test_pdf):
    # Arrange
    files = {"file": ("test.pdf", io.BytesIO(test_pdf), "application/pdf")}
    
    # Act
    response = test_client.post("/api/v1/pdf/upload", files=files)
    
    # Assert
    assert response.status_code == 200
    assert "pdf_id" in response.json()

def test_upload_invalid_file_type(test_client: TestClient):
    # Arrange
    files = {"file": ("test.txt", io.BytesIO(b"test"), "text/plain")}
    
    # Act
    response = test_client.post("/api/v1/pdf/upload", files=files)
    
    # Assert
    assert response.status_code == 400

def test_chat_with_pdf(test_client: TestClient, test_pdf):
    # Arrange
    files = {"file": ("test.pdf", io.BytesIO(test_pdf), "application/pdf")}
    upload_response = test_client.post("/api/v1/pdf/upload", files=files)
    assert upload_response.status_code == 200  # Add this check
    
    pdf_id = upload_response.json()["pdf_id"]
    
    # Act
    chat_response = test_client.post(
        f"/api/v1/chat/{pdf_id}",
        json={"message": "What is this about?"}
    )
    
    # Assert
    assert chat_response.status_code == 200
    assert "response" in chat_response.json()