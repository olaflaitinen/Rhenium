import pytest
import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from backend.safety.validator import SQLValidator, SecurityError


class TestSQLValidator:
    """Test suite for SQL validator."""

    def test_valid_select_query(self):
        """Test that a valid SELECT query passes validation."""
        query = "SELECT * FROM sales WHERE YEAR_ID = 2003;"
        is_valid, error = SQLValidator.validate(query)
        assert is_valid is True
        assert error == ""

    def test_reject_drop_statement(self):
        """Test that DROP statements are rejected."""
        query = "DROP TABLE sales;"
        is_valid, error = SQLValidator.validate(query)
        assert is_valid is False
        assert "DROP" in error

    def test_reject_delete_statement(self):
        """Test that DELETE statements are rejected."""
        query = "DELETE FROM sales WHERE id = 1;"
        is_valid, error = SQLValidator.validate(query)
        assert is_valid is False
        assert "DELETE" in error

    def test_reject_update_statement(self):
        """Test that UPDATE statements are rejected."""
        query = "UPDATE sales SET price = 100 WHERE id = 1;"
        is_valid, error = SQLValidator.validate(query)
        assert is_valid is False
        assert "UPDATE" in error

    def test_reject_multiple_statements(self):
        """Test that multiple statements are rejected."""
        query = "SELECT * FROM sales; DROP TABLE sales;"
        is_valid, error = SQLValidator.validate(query)
        assert is_valid is False
        assert "Multiple statements" in error

    def test_validate_or_raise_success(self):
        """Test that validate_or_raise doesn't raise for valid queries."""
        query = "SELECT * FROM sales LIMIT 10;"
        try:
            SQLValidator.validate_or_raise(query)
        except SecurityError:
            pytest.fail("validate_or_raise raised SecurityError for a valid query")

    def test_validate_or_raise_failure(self):
        """Test that validate_or_raise raises SecurityError for invalid queries."""
        query = "DROP TABLE sales;"
        with pytest.raises(SecurityError):
            SQLValidator.validate_or_raise(query)
