from backend.database.schema import sales_table
from sqlalchemy.schema import CreateTable
from sqlalchemy.engine import mock

def get_schema_string():
    """
    Returns the DDL (CREATE TABLE statement) for the sales table
    to be included in the prompt.
    """
    # Use a mock engine to generate DDL without connecting to a DB
    def dump(sql, *multiparams, **params):
        return sql.compile(dialect=mock.engine.dialect)
    
    engine = mock.create_mock_engine("sqlite://", dump)
    ddl = CreateTable(sales_table).compile(engine)
    return str(ddl)

TEXT_TO_SQL_PROMPT_TEMPLATE = """
You are an expert SQL data analyst. Your task is to translate a natural language question into a valid SQLite SQL query.

### Database Schema
The query will run against a database with the following schema:

{schema}

### Rules
1. Return ONLY the SQL query. No explanations, no markdown code blocks.
2. Use SQLite syntax.
3. Do not use dangerous commands like DROP, DELETE, UPDATE.
4. If the question cannot be answered with the given schema, return "SELECT 'Cannot answer question' as error;".
5. Use 'sales' as the table name.

### Examples
Question: What is the total revenue?
SQL: SELECT SUM(SALES) FROM sales;

Question: How many orders were placed in 2004?
SQL: SELECT COUNT(DISTINCT ORDERNUMBER) FROM sales WHERE YEAR_ID = 2004;

### Task
Question: {question}
SQL:
"""

def get_text_to_sql_prompt(question: str) -> str:
    schema_str = get_schema_string()
    return TEXT_TO_SQL_PROMPT_TEMPLATE.format(schema=schema_str, question=question)
