import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import os
import shutil
from app.core.config import get_settings
from main import app

settings = get_settings()

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def test_storage():
    """Create and clean up test storage directory"""
    test_storage_path = Path("test_storage/pdfs")
    test_storage_path.mkdir(parents=True, exist_ok=True)
    
    # Override storage path for tests
    settings.UPLOAD_FOLDER = str(test_storage_path)
    
    yield test_storage_path
    
    # Cleanup after tests
    shutil.rmtree(test_storage_path.parent)

@pytest.fixture
def test_pdf():
    """Create a minimal valid PDF file"""
    return b'''%PDF-1.4
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj
3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R>>endobj
xref
0 4
0000000000 65535 f
0000000009 00000 n
0000000052 00000 n
0000000101 00000 n
trailer<</Size 4/Root 1 0 R>>
startxref
171
%%EOF'''