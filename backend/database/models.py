"""
Database models for application data (non-auth).

Includes:
- Sales data
- Audit logs
- Query cache
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class SalesOrder(Base):
    """Sales order data model."""
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ORDERNUMBER = Column(Integer, index=True)
    QUANTITYORDERED = Column(Integer)
    PRICEEACH = Column(Float)
    ORDERLINENUMBER = Column(Integer)
    SALES = Column(Float)
    ORDERDATE = Column(Date)
    STATUS = Column(String)
    QTR_ID = Column(Integer)
    MONTH_ID = Column(Integer)
    YEAR_ID = Column(Integer, index=True)
    PRODUCTLINE = Column(String, index=True)
    MSRP = Column(Integer)
    PRODUCTCODE = Column(String)
    CUSTOMERNAME = Column(String, index=True)
    PHONE = Column(String)
    ADDRESSLINE1 = Column(String)
    ADDRESSLINE2 = Column(String)
    CITY = Column(String)
    STATE = Column(String)
    POSTALCODE = Column(String)
    COUNTRY = Column(String, index=True)
    TERRITORY = Column(String)
    CONTACTLASTNAME = Column(String)
    CONTACTFIRSTNAME = Column(String)
    DEALSIZE = Column(String)


class AuditLog(Base):
    """Audit log for all database queries."""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True, index=True)  # Removed ForeignKey temporarily
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Request details
    natural_language_query = Column(Text)
    generated_sql = Column(Text)
    
    # Execution details
    execution_status = Column(String)  # success, error, blocked
    execution_time_ms = Column(Float)
    rows_returned = Column(Integer)
    error_message = Column(Text, nullable=True)
    
    # Validation details
    validation_status = Column(String)  # allowed, blocked
    validation_reason = Column(Text, nullable=True)
    
    # Context
    endpoint = Column(String)
    ip_address = Column(String)
    user_agent = Column(String, nullable=True)
    
    # Response
    response_sent = Column(Boolean, default=True)


class QueryCache(Base):
    """Cache for LLM-generated SQL queries."""
    __tablename__ = "query_cache"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Cache key (hash of natural language query + schema version)
    cache_key = Column(String, unique=True, index=True)
    
    # Input
    natural_language_query = Column(Text)
    schema_hash = Column(String)  # Hash of database schema
    
    # Output
    generated_sql = Column(Text)
    llm_provider = Column(String)
    model_name = Column(String)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    accessed_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    access_count = Column(Integer, default=0)
    
    # Performance
    generation_time_ms = Column(Float)
    tokens_used = Column(Integer, nullable=True)


class SchemaMetadata(Base):
    """Metadata about database schema for semantic search."""
    __tablename__ = "schema_metadata"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Schema object identification
    object_type = Column(String, index=True)  # table, column, view
    object_name = Column(String, index=True)
    parent_name = Column(String, nullable=True)  # For columns: parent table name
    
    # Descriptions
    description = Column(Text)
    business_glossary = Column(Text, nullable=True)
    example_values = Column(Text, nullable=True)
    
    # Embeddings (for semantic search)
    embedding = Column(JSON, nullable=True)  # Store as JSON array
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
