"""
Database connection management with support for multiple backends.

Supports:
- SQLite (development)
- PostgreSQL (production)
"""
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool, QueuePool

from backend.config.settings import settings

# Create engine with appropriate configuration
if settings.DATABASE_TYPE == "sqlite":
    # SQLite configuration
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # SQLite works best with StaticPool
        echo=settings.DEBUG
    )
    
    # Enable foreign keys for SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
else:
    # PostgreSQL configuration
    engine = create_engine(
        settings.database_url,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,  # Verify connections before using
        echo=settings.DEBUG
    )

# Create SessionLocal class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get a database session.
    
    Yields:
        Database session
        
    Usage:
        @app.get("/")
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database schema.
    Should be called on application startup.
    """
    from backend.auth.models import Base as AuthBase
    from backend.database.models import Base as DatabaseBase
    
    # Create all tables
    AuthBase.metadata.create_all(bind=engine)
    DatabaseBase.metadata.create_all(bind=engine)

