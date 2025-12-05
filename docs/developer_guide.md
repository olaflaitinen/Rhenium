# Developer Guide

## LLM-Based DBMS - Comprehensive Development Documentation

**For**: Eskişehir Technical University, Department of Electrical and Electronics Engineering 
**Project**: 2025-2026 Design Project | TÜBİTAK 2209-A Research Project 
**Team**: Derya Umut Kulalı, Anıl Aydın, Sıla Alhan | **Advisor**: Mehmet Fidan

---

## Table of Contents

1. [Development Environment Setup](#development-environment-setup)
2. [Project Architecture](#project-architecture)
3. [Code Organization](#code-organization)
4. [Development Workflow](#development-workflow)
5. [Testing](#testing)
6. [Code Style and Standards](#code-style-and-standards)
7. [Adding New Features](#adding-new-features)
8. [Debugging](#debugging)
9. [Performance Optimization](#performance-optimization)
10. [Common Development Tasks](#common-development-tasks)

---

## Development Environment Setup

### Prerequisites

- **Python**: 3.11 or higher
- **Git**: Latest version
- **IDE**: VS Code, PyCharm, or similar
- **Database**: SQLite (development) or PostgreSQL (production testing)
- **Optional**: Docker Desktop (for containerized development)

### Initial Setup

#### 1. Clone and Navigate

```bash
git clone https://github.com/Japyh/llm-based-dbms.git
cd llm-based-dbms
```

#### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3.11 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

**Minimal (for core development):**
```bash
pip install -r requirements-minimal.txt
pip install email-validator
```

**Full (with dev tools):**
```bash
pip install -r requirements.txt
pip install -e ".[dev]" # Editable install with dev dependencies
```

#### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` for development:
```ini
ENVIRONMENT=development
DEBUG=True
DATABASE_TYPE=sqlite
LLM_PROVIDER=mock # No API key needed for testing
LOG_LEVEL=DEBUG
```

#### 5. Initialize Database

```bash
python scripts/init_db.py
```

#### 6. Verify Setup

```bash
# Run tests
pytest backend/tests/ -v

# Start dev server
python scripts/run_dev_server.py
```

Visit http://localhost:8000/docs to confirm API is running.

---

## Project Architecture

### High-Level Architecture

```
┌─────────────┐
│ Client │
└──────┬──────┘
 │ HTTP/REST
┌──────▼──────────┐
│ API Layer │ (FastAPI)
│ - Routers │
│ - Middleware │
│ - Schemas │
└──────┬──────────┘
 │
┌──────▼──────────┐
│ Business Logic │
│ - LLM Client │
│ - Safety │
│ - Auth/RBAC │
└──────┬──────────┘
 │
┌──────▼──────────┐
│ Data Layer │
│ - Database │
│ - Repository │
│ - Models │
└─────────────────┘
```

### Module Breakdown

#### `backend/api/`
- **Purpose**: HTTP request handling
- **Key Files**:
 - `main.py`: Application factory
 - `routers/`: Endpoint definitions
 - `schemas/`: Pydantic models
 - `middleware/`: Custom middleware

#### `backend/llm/`
- **Purpose**: LLM integration and prompt management
- **Key Files**:
 - `client.py`: Multi-provider LLM client
 - `prompts.py`: Prompt templates
 - `cache.py`: Response caching
 - `token_tracking.py`: Usage monitoring

#### `backend/safety/`
- **Purpose**: SQL validation and security
- **Key Files**:
 - `validator.py`: AST-based SQL validator
 - `policies.py`: Safety policy definitions
 - `access_control.py`: RBAC enforcement
 - `explainer.py`: Validation explanations

#### `backend/database/`
- **Purpose**: Data persistence
- **Key Files**:
 - `connection.py`: Connection pooling
 - `models.py`: SQLAlchemy ORM models
 - `executor.py`: Query execution
 - `migrations/`: Alembic migrations

#### `backend/auth/`
- **Purpose**: Authentication and authorization
- **Key Files**:
 - `service.py`: Auth business logic
 - `models.py`: User and Role models
 - `rbac.py`: Role-based access control
 - `dependencies.py`: FastAPI dependencies

---

## Code Organization

### Directory Structure

```
backend/
├── __init__.py
├── api/
│ ├── __init__.py
│ ├── main.py # App factory
│ ├── routes.py # Legacy router
│ ├── routers/
│ │ ├── __init__.py
│ │ ├── query.py # Query endpoints
│ │ ├── auth.py # Auth endpoints
│ │ ├── admin.py # Admin endpoints
│ │ ├── health.py # Health checks
│ │ └── schema.py # Schema endpoints
│ ├── schemas/
│ │ ├── __init__.py
│ │ ├── query.py # Query request/response
│ │ ├── auth.py # Auth schemas
│ │ └── common.py # Shared schemas
│ └── middleware/
│ ├── __init__.py
│ ├── logging.py # Request logging
│ └── error_handler.py
├── llm/
│ ├── __init__.py
│ ├── client.py # LLM abstraction
│ ├── prompts.py # Prompt templates
│ ├── cache.py # Response caching
│ └── token_tracking.py
├── safety/
│ ├── __init__.py
│ ├── validator.py # SQL validation
│ ├── policies.py # Safety policies
│ ├── access_control.py
│ └── explainer.py
├── database/
│ ├── __init__.py
│ ├── connection.py # DB connection
│ ├── models.py # ORM models
│ ├── executor.py # Query executor
│ ├── repository.py # Data access
│ ├── schema.py # Schema definitions
│ └── migrations/ # Alembic
├── auth/
│ ├── __init__.py
│ ├── models.py # User, Role models
│ ├── service.py # Auth logic
│ ├── rbac.py # RBAC
│ └── dependencies.py # FastAPI deps
├── observability/
│ ├── __init__.py
│ ├── logging_config.py
│ └── metrics.py # Prometheus
├── config/
│ ├── __init__.py
│ └── settings.py # Configuration
├── semantic/
│ ├── __init__.py
│ ├── interface.py
│ ├── embeddings.py
│ └── chroma_store.py
└── tests/
 ├── __init__.py
 ├── test_api.py
 └── test_safety.py
```

### Naming Conventions

- **Files**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions/Methods**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`
- **Type Variables**: `T`, `K`, `V`

---

## Development Workflow

### 1. Feature Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/your-feature-name

# 2. Make changes
# Edit code...

# 3. Add tests
# backend/tests/test_your_feature.py

# 4. Run tests
pytest backend/tests/ -v --cov=backend

# 5. Format code
black backend/
isort backend/

# 6. Lint
ruff check backend/
mypy backend/

# 7. Commit
git add .
git commit -m "feat: add your feature"

# 8. Push and create PR
git push origin feature/your-feature-name
```

### 2. Git Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Build/config changes
- `perf`: Performance improvements

**Examples:**
```
feat(llm): add support for local Ollama models

fix(safety): prevent SQL injection in LIKE clauses

docs(api): update endpoint documentation

test(auth): add unit tests for JWT validation
```

---

## Testing

### Test Structure

```
backend/tests/
├── __init__.py
├── conftest.py # Pytest fixtures
├── test_api.py # API endpoint tests
├── test_safety.py # Safety validator tests
├── test_llm.py # LLM client tests
├── test_auth.py # Auth tests
└── test_integration.py # Integration tests
```

### Running Tests

**All tests:**
```bash
pytest backend/tests/ -v
```

**With coverage:**
```bash
pytest backend/tests/ -v --cov=backend --cov-report=html
```

**Specific test file:**
```bash
pytest backend/tests/test_safety.py -v
```

**Specific test:**
```bash
pytest backend/tests/test_api.py::TestAPI::test_health_check -v
```

**Test markers:**
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

### Writing Tests

**Example - API Test:**
```python
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)

def test_query_endpoint():
 # Login
 response = client.post(
 "/api/v1/auth/login",
 data={"username": "admin", "password": "admin123"}
 )
 token = response.json()["access_token"]
 
 # Query
 response = client.post(
 "/api/v1/query/",
 headers={"Authorization": f"Bearer {token}"},
 json={"question": "What is total revenue?"}
 )
 
 assert response.status_code == 200
 data = response.json()
 assert "generated_sql" in data
 assert "results" in data
```

**Example - Unit Test:**
```python
import pytest
from backend.safety.validator import SQLValidator
from backend.auth.models import User, RoleEnum

def test_sql_validator_blocks_drop():
 user = User(username="test", roles=[RoleEnum.ANALYST])
 validator = SQLValidator(user)
 
 is_valid, error = validator.validate("DROP TABLE users;")
 
 assert is_valid is False
 assert "DROP" in error
```

### Test Fixtures

**In `conftest.py`:**
```python
import pytest
from backend.database.connection import SessionLocal

@pytest.fixture
def db_session():
 """Provide a database session for tests."""
 session = SessionLocal()
 try:
 yield session
 finally:
 session.close()

@pytest.fixture
def admin_user(db_session):
 """Create an admin user for testing."""
 from backend.auth.models import User, RoleEnum
 
 user = User(
 username="test_admin",
 email="admin@test.com",
 roles=[RoleEnum.ADMIN]
 )
 db_session.add(user)
 db_session.commit()
 return user
```

---

## Code Style and Standards

### Python Style Guide

Follow **PEP 8** with these additions:

- **Line length**: 100 characters (configured in `pyproject.toml`)
- **Docstrings**: Google style
- **Type hints**: Required for all public functions
- **Imports**: Organized by `isort`

### Code Formatting

**Black** (automatic formatting):
```bash
black backend/
```

**isort** (import sorting):
```bash
isort backend/
```

**Combined:**
```bash
black backend/ && isort backend/
```

### Linting

**Ruff** (fast Python linter):
```bash
ruff check backend/
```

**Fix automatically:**
```bash
ruff check backend/ --fix
```

**mypy** (type checking):
```bash
mypy backend/
```

### Docstring Format

```python
def execute_query(sql: str, user: User) -> List[Dict[str, Any]]:
 """
 Execute a validated SQL query and return results.
 
 Args:
 sql: The SQL query to execute
 user: The user executing the query (for access control)
 
 Returns:
 List of dictionaries representing rows
 
 Raises:
 QueryExecutionError: If query execution fails
 ValidationError: If query doesn't pass safety checks
 
 Example:
 >>> result = execute_query("SELECT * FROM sales LIMIT 5;", admin_user)
 >>> len(result)
 5
 """
 pass
```

---

## Adding New Features

### Adding a New LLM Provider

1. **Extend `LLMClient` base class:**

```python
# backend/llm/client.py

class LocalLLMClient(LLMClient):
 """Client for local LLM server (e.g., Ollama)."""
 
 def __init__(self):
 self.base_url = settings.LOCAL_LLM_URL
 self.model = settings.LOCAL_LLM_MODEL
 
 def generate_sql(self, prompt: str) -> str:
 import requests
 
 response = requests.post(
 f"{self.base_url}/generate",
 json={"prompt": prompt, "model": self.model}
 )
 return response.json()["text"]
 
 def explain_sql(self, sql: str, question: str) -> str:
 # Implementation
 pass
```

2. **Register in factory:**

```python
def get_llm_client() -> LLMClient:
 provider = settings.LLM_PROVIDER.lower()
 
 if provider == "openai":
 return OpenAILLMClient()
 elif provider == "anthropic":
 return AnthropicLLMClient()
 elif provider == "local": # NEW
 return LocalLLMClient()
 else:
 return MockLLMClient()
```

3. **Add configuration:**

```python
# backend/config/settings.py

class Settings(BaseSettings):
 # ... existing settings ...
 
 LOCAL_LLM_URL: str = "http://localhost:11434"
 LOCAL_LLM_MODEL: str = "llama2"
```

4. **Add tests:**

```python
# backend/tests/test_llm.py

def test_local_llm_client():
 client = LocalLLMClient()
 sql = client.generate_sql("What is total revenue?")
 assert isinstance(sql, str)
```

### Adding a New API Endpoint

1. **Create router function:**

```python
# backend/api/routers/new_feature.py

from fastapi import APIRouter, Depends
from backend.auth.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/feature", tags=["Feature"])

@router.get("/")
async def get_feature(current_user = Depends(get_current_user)):
 """Get feature data."""
 return {"message": "Feature endpoint"}
```

2. **Register router:**

```python
# backend/api/main.py

from backend.api.routers import new_feature

app.include_router(new_feature.router)
```

3. **Add tests:**

```python
# backend/tests/test_api.py

def test_new_feature_endpoint():
 response = client.get("/api/v1/feature/")
 assert response.status_code == 200
```

---

## Debugging

### Local Debugging

**VS Code - launch.json:**
```json
{
 "version": "0.2.0",
 "configurations": [
 {
 "name": "Python: FastAPI",
 "type": "python",
 "request": "launch",
 "module": "uvicorn",
 "args": [
 "backend.api.main:app",
 "--reload",
 "--port", "8000"
 ],
 "jinja": true,
 "justMyCode": false
 }
 ]
}
```

**PyCharm:**
- Run Configuration → FastAPI
- Script path: `uvicorn`
- Parameters: `backend.api.main:app --reload`

### Logging

**Enable debug logging:**
```python
# .env
LOG_LEVEL=DEBUG
```

**View structured logs:**
```bash
tail -f logs/app.log | jq
```

### Database Debugging

**View generated SQL:**
```python
# .env
DEBUG=True # Enables SQLAlchemy echo
```

**Inspect database:**
```bash
sqlite3 data/processed/sales.db
.tables
.schema sales
SELECT * FROM sales LIMIT 5;
```

---

## Performance Optimization

### Profiling

**cProfile:**
```bash
python -m cProfile -o profile.stats scripts/run_dev_server.py
```

**Analyze:**
```python
import pstats
p = pstats.Stats('profile.stats')
p.sort_stats('cumulative').print_stats(20)
```

### Query Optimization

**Use database indexes:**
```python
# backend/database/models.py

class SalesOrder(Base):
 __tablename__ = "sales"
 
 ORDERNUMBER = Column(Integer, primary_key=True, index=True)
 COUNTRY = Column(String, index=True) # Add index
```

**Connection pooling:**
```python
# Already configured in backend/database/connection.py
pool_size=5
max_overflow=10
```

### Caching

**LLM response caching:**
```python
# Enabled by default when Redis is available
ENABLE_LLM_CACHE=True
CACHE_TTL_SECONDS=3600
```

---

## Common Development Tasks

### Database Migrations

**Create migration:**
```bash
alembic revision --autogenerate -m "Add new column"
```

**Apply migration:**
```bash
alembic upgrade head
```

**Rollback:**
```bash
alembic downgrade -1
```

### Adding Dependencies

```bash
# Add to requirements.txt
echo "new-package==1.0.0" >> requirements.txt

# Install
pip install new-package

# Update pyproject.toml if needed
```

### Environment Variables

**Add new setting:**
```python
# backend/config/settings.py

class Settings(BaseSettings):
 NEW_SETTING: str = Field(default="value", env="NEW_SETTING")
```

**Use in code:**
```python
from backend.config.settings import settings

value = settings.NEW_SETTING
```

---

## IDE Configuration

### VS Code

**.vscode/settings.json:**
```json
{
 "python.linting.enabled": true,
 "python.linting.pylintEnabled": false,
 "python.linting.flake8Enabled": false,
 "python.formatting.provider": "black",
 "python.linting.mypyEnabled": true,
 "editor.formatOnSave": true,
 "editor.rulers": [100]
}
```

### PyCharm

- Enable Black formatting: File → Settings → Tools → Black
- Set line length to 100
- Enable type checking with mypy

---

## Troubleshooting

### Common Issues

**Import errors:**
```bash
# Ensure you're in project root
cd /path/to/llm-based-dbms

# Activate venv
source venv/bin/activate # or .\venv\Scripts\activate
```

**Database locked:**
```bash
# SQLite issue - close all connections
rm data/processed/sales.db
python scripts/init_db.py
```

**Port already in use:**
```bash
# Change port in .env
API_PORT=8001
```

---

## Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org
- **LangChain Documentation**: https://python.langchain.com
- **Pydantic Documentation**: https://docs.pydantic.dev

---

For questions or issues, contact the development team through Eskişehir Technical University's Department of Electrical and Electronics Engineering.

**Team**: Derya Umut Kulalı, Anıl Aydın, Sıla Alhan 
**Advisor**: Mehmet Fidan 
**Project**: TÜBİTAK 2209-A Research Project
