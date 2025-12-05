import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from backend.api.app import app

client = TestClient(app)


class TestAPI:
    """Test suite for API endpoints."""

    def test_health_check(self):
        """Test the /health endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

    def test_schema_endpoint(self):
        """Test the /schema endpoint."""
        response = client.get("/schema")
        assert response.status_code == 200
        data = response.json()
        assert "schema_ddl" in data
        assert "sales" in data["schema_ddl"].lower()

    def test_query_endpoint_with_mock(self):
        """Test the /query endpoint with mock LLM."""
        payload = {"question": "What is the total revenue?"}
        response = client.post("/query", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "question" in data
        assert "generated_sql" in data
        assert data["question"] == "What is the total revenue?"
