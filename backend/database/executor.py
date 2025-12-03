"""
Enhanced database executor with better error handling and result formatting.
"""
from typing import List, Dict, Any, Optional
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from backend.database.connection import engine


class QueryExecutionError(Exception):
    """Custom exception for query execution failures."""
    pass


def execute_sql_query(
    query: str,
    parameters: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Execute a raw SQL query against the database and return results.
    
    Args:
        query: The SQL query to execute
        parameters: Optional query parameters for safe parameterization
        
    Returns:
        List of rows as dictionaries
        
    Raises:
        QueryExecutionError: If the query fails to execute
    """
    try:
        with engine.connect() as connection:
            # Use text() for raw SQL with optional parameter binding
            stmt = text(query)
            
            if parameters:
                result = connection.execute(stmt, parameters)
            else:
                result = connection.execute(stmt)
            
            # Check if query returns rows
            if result.returns_rows:
                keys = list(result.keys())
                rows = result.fetchall()
                
                # Convert to list of dictionaries
                return [dict(zip(keys, row)) for row in rows]
            else:
                # For non-returning queries (shouldn't happen with our validators)
                connection.commit()
                return []
                
    except SQLAlchemyError as e:
        raise QueryExecutionError(f"Database error: {str(e)}") from e
    except Exception as e:
        raise QueryExecutionError(f"Unexpected error: {str(e)}") from e
