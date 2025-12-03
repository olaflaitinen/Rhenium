from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from backend.llm.client import get_llm_client, LLMClient
from backend.llm.prompts import get_text_to_sql_prompt
from backend.safety.validator import SQLValidator
from backend.database.executor import execute_sql_query, QueryExecutionError
from backend.database.schema import sales_table
from sqlalchemy.schema import CreateTable
from sqlalchemy.engine import mock

router = APIRouter()

# --- Pydantic Models ---

class QueryRequest(BaseModel):
    question: str
    user_id: Optional[str] = None

class QueryResponse(BaseModel):
    question: str
    generated_sql: str
    results: List[Dict[str, Any]]
    error: Optional[str] = None

class SchemaResponse(BaseModel):
    schema_ddl: str

# --- Endpoints ---

@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "Service is running"}

@router.get("/schema", response_model=SchemaResponse)
async def get_schema():
    """
    Returns the current database schema DDL.
    """
    # Helper to generate DDL string
    def dump(sql, *multiparams, **params):
        return sql.compile(dialect=mock.engine.dialect)
    
    engine = mock.create_mock_engine("sqlite://", dump)
    ddl = CreateTable(sales_table).compile(engine)
    return SchemaResponse(schema_ddl=str(ddl))

@router.post("/query", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    llm_client: LLMClient = Depends(get_llm_client)
):
    """
    Processes a natural language query:
    1. Translates NL to SQL using LLM.
    2. Validates the SQL.
    3. Executes the SQL.
    4. Returns results.
    """
    try:
        # 1. Generate SQL
        prompt = get_text_to_sql_prompt(request.question)
        generated_sql = llm_client.generate_sql(prompt)
        
        # Clean up SQL (remove markdown if present, though prompt says not to)
        generated_sql = generated_sql.replace("```sql", "").replace("```", "").strip()

        # 2. Validate SQL
        is_valid, error_msg = SQLValidator.validate(generated_sql)
        if not is_valid:
            return QueryResponse(
                question=request.question,
                generated_sql=generated_sql,
                results=[],
                error=f"Safety Violation: {error_msg}"
            )

        # 3. Execute SQL
        results = execute_sql_query(generated_sql)
        
        return QueryResponse(
            question=request.question,
            generated_sql=generated_sql,
            results=results
        )

    except QueryExecutionError as e:
        return QueryResponse(
            question=request.question,
            generated_sql=generated_sql if 'generated_sql' in locals() else "",
            results=[],
            error=f"Execution Error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
