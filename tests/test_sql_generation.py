import pytest
from backend.llm.client import MockLLMClient

def test_mock_generation():
    client = MockLLMClient()
    sql = client.generate_sql("Show me all users")
    assert "SELECT" in sql
    assert "sales" in sql # Mock client returns sales table query

def test_mock_explanation():
    client = MockLLMClient()
    explanation = client.explain_sql("SELECT * FROM users", "Show me all users")
    assert "Show me all users" in explanation
