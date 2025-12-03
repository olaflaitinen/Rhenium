import sqlite3
from contextlib import contextmanager
from typing import Generator

from backend.config.settings import settings


class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @contextmanager
    def get_cursor(self) -> Generator[sqlite3.Cursor, None, None]:
        conn = self.get_connection()
        try:
            yield conn.cursor()
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def execute_query(self, query: str, params: tuple = ()) -> list[dict]:
        """Executes a read-only query and returns a list of dicts."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            # If it's a SELECT query, fetch results
            if cursor.description:
                columns = [col[0] for col in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
            return []


db_manager = DatabaseManager(settings.DB_PATH)
