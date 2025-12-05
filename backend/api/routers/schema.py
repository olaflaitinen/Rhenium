"""
Schema router for database schema inspection and management.

Provides endpoints to:
- View database schema
- Get table information
- Update schema metadata for semantic search
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import inspect, text

from backend.api.schemas.schema import (
    SchemaResponse,
    TableInfo,
    ColumnInfo,
    SchemaMetadataRequest
)
from backend.auth.dependencies import get_current_user
from backend.auth.models import User
from backend.database.connection import get_db, engine
from backend.database.models import SchemaMetadata

router = APIRouter(prefix="/api/v1/schema", tags=["Schema"])


@router.get("/", response_model=SchemaResponse)
async def get_database_schema(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the current database schema.
    
    Returns information about all tables, columns, and types.
    """
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    
    tables: List[TableInfo] = []
    
    for table_name in table_names:
        columns_info = inspector.get_columns(table_name)
        pk_constraint = inspector.get_pk_constraint(table_name)
        fk_constraints = inspector.get_foreign_keys(table_name)
        
        # Build column information
        columns: List[ColumnInfo] = []
        for col in columns_info:
            # Check if primary key
            is_pk = col['name'] in pk_constraint.get('constrained_columns', [])
            
            # Check for foreign keys
            fk = None
            for fk_constraint in fk_constraints:
                if col['name'] in fk_constraint['constrained_columns']:
                    fk = f"{fk_constraint['referred_table']}.{fk_constraint['referred_columns'][0]}"
                    break
            
            columns.append(ColumnInfo(
                name=col['name'],
                type=str(col['type']),
                nullable=col.get('nullable', True),
                primary_key=is_pk,
                foreign_key=fk
            ))
        
        # Get row count (optional - can be expensive for large tables)
        try:
            result = db.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            row_count = result.scalar()
        except:
            row_count = None
        
        tables.append(TableInfo(
            name=table_name,
            columns=columns,
            row_count=row_count
        ))
    
    return SchemaResponse(
        database_type=str(engine.url.drivername),
        tables=tables,
        total_tables=len(tables)
    )


@router.post("/metadata", status_code=201)
async def create_schema_metadata(
    metadata: SchemaMetadataRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add or update metadata for a schema object (table or column).
    
    This metadata is used for semantic search and better query understanding.
    """
    # Check if metadata already exists
    existing = db.query(SchemaMetadata).filter(
        SchemaMetadata.object_type == metadata.object_type,
        SchemaMetadata.object_name == metadata.object_name,
        SchemaMetadata.parent_name == metadata.parent_name
    ).first()
    
    if existing:
        # Update existing
        existing.description = metadata.description
        existing.business_glossary = metadata.business_glossary
        existing.example_values = metadata.example_values
    else:
        # Create new
        new_metadata = SchemaMetadata(
            object_type=metadata.object_type,
            object_name=metadata.object_name,
            parent_name=metadata.parent_name,
            description=metadata.description,
            business_glossary=metadata.business_glossary,
            example_values=metadata.example_values
        )
        db.add(new_metadata)
    
    db.commit()
    
    return {"message": "Metadata saved successfully"}
