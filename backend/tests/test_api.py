import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_upload_documents_unauthenticated():
    # This test will fail because it requires a logged-in user.
    # We'll need to set up a test user and authenticate for this to work.
    pass
