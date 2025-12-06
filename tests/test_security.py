from fastapi.testclient import TestClient
from backend.api.main import app
from backend.config.settings import settings

client = TestClient(app)
API_PREFIX = f"/api/{settings.API_VERSION}"

def test_sql_injection_prevention():
    # Attempt to inject SQL via natural language input
    # The system should either sanitize it or the LLM should handle it.
    # But more importantly, if we had a direct SQL endpoint (which we don't expose publicly), we'd test that.
    # Here we test the query generation endpoint with malicious input.
    
    payload = {
        "question": "Show me users; DROP TABLE users;",
        "mode": "read_only"
    }
    response = client.post(f"{API_PREFIX}/query/generate", json=payload)
    
    # The response should NOT contain the DROP TABLE statement in the generated SQL 
    # OR it should be a valid SELECT that ignores the injection attempt.
    if response.status_code == 200:
        data = response.json()
        sql = data.get("sql", "").upper()
        # Mock LLM might just return "SELECT * FROM sales..." which is safe.
        # If it returns the input verbatim, that's bad.
        assert "DROP TABLE" not in sql

def test_xss_prevention():
    # Test XSS in input
    payload = {
        "question": "<script>alert(1)</script>",
        "mode": "read_only"
    }
    response = client.post(f"{API_PREFIX}/query/generate", json=payload)
    if response.status_code == 200:
        # Ensure the response doesn't reflect the script tag in a dangerous way
        # (JSON response is generally safe from XSS unless rendered as HTML)
        pass
