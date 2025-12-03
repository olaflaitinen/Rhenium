from typing import List, Dict, Any
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from backend.db.connection import engine

class QueryExecutionError(Exception):
    """Custom exception for query execution failures."""
    pass

def execute_sql_query(query: str) -> List[Dict[str, Any]]:
    """
    Executes a raw SQL query against the database and returns the results as a list of dictionaries.
    
    Args:
        query (str): The SQL query to execute.
        
    Returns:
        List[Dict[str, Any]]: A list of rows, where each row is a dictionary mapping column names to values.
        
    Raises:
        QueryExecutionError: If the query fails to execute.
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            
            # If the query is not a SELECT statement (e.g. INSERT, UPDATE, DELETE), 
            # it might not return rows. In this system, we mostly expect SELECTs,
            # but we should handle cases where there are no rows to fetch.
            if result.returns_rows:
                keys = result.keys()
                return [dict(zip(keys, row)) for row in result.fetchall()]
            else:
                # For non-returning queries, we can return an empty list or a success message.
                # Since this is primarily a read-only interface for now, empty list is safe.
                connection.commit()
                return []
                
    except SQLAlchemyError as e:
        raise QueryExecutionError(f"Database error: {str(e)}") from e
    except Exception as e:
        raise QueryExecutionError(f"Unexpected error: {str(e)}") from e
