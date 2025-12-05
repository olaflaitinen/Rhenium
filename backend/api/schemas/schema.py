"""
Database schema-related API schemas.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ColumnInfo(BaseModel):
    """Information about a database column."""
    name: str
    type: str
    nullable: bool = True
    primary_key: bool = False
    foreign_key: Optional[str] = None
    description: Optional[str] = None


class TableInfo(BaseModel):
    """Information about a database table."""
    name: str
    columns: List[ColumnInfo]
    row_count: Optional[int] = None
    description: Optional[str] = None


class SchemaResponse(BaseModel):
    """Database schema response."""
    database_type: str
    tables: List[TableInfo]
    total_tables: int
    ddl: Optional[str] = Field(None, description="Full DDL (CREATE TABLE statements)")


class SchemaMetadataRequest(BaseModel):
    """Request to update schema metadata."""
    object_type: str = Field(..., description="table or column")
    object_name: str
    parent_name: Optional[str] = None
    description: str
    business_glossary: Optional[str] = None
    example_values: Optional[str] = None
