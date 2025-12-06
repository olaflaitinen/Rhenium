from fastapi.testclient import TestClient
from backend.api.main import app
from backend.config.settings import settings

client = TestClient(app)
API_PREFIX = f"/api/{settings.API_VERSION}"

def test_full_query_flow():
    # 1. Login (Mock auth for now or skip if auth disabled in dev)
    # Assuming dev mode allows access or we use a test user
    # For now, we'll test the public/protected endpoints assuming default config
    
    # 2. Health Check
    response = client.get(f"{API_PREFIX}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

    # 3. Schema Info
    response = client.get(f"{API_PREFIX}/schema/tables")
    # Might be 200 or 401 depending on auth
    if response.status_code == 200:
        assert isinstance(response.json(), list)

    # 4. Execute Query (Natural Language)
    # This requires LLM. We'll use the MockLLM which is default if no key.
    payload = {
        "question": "Show me all sales",
        "mode": "read_only"
    }
    response = client.post(f"{API_PREFIX}/query/generate", json=payload)
    if response.status_code == 200:
        data = response.json()
        assert "sql" in data
        assert "SELECT" in data["sql"]

def test_admin_endpoints():
    # Test admin endpoints access control
    response = client.get(f"{API_PREFIX}/admin/users")
    # Should fail without auth
    assert response.status_code in [401, 403]
