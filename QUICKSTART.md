# Quick Start Guide

Get the LLM-Based DBMS up and running in 5 minutes!

## Quick Installation

### Prerequisites
- Python 3.11 or higher
- Git
- (Optional) Docker & Docker Compose

### Step 1: Clone Repository

```bash
git clone https://github.com/Japyh/llm-based-dbms.git
cd llm-based-dbms
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements-minimal.txt
pip install email-validator
```

### Step 4: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file (optional for quick start)
# LLM_PROVIDER=mock # No API key needed for testing
```

### Step 5: Initialize Database

```bash
python scripts/init_db.py
```

You should see:
```
 Database schema created.
 Default roles created (ADMIN, DATA_SCIENTIST, ANALYST, VIEWER).
 Created admin user:
 Username: admin
 Password: admin123
```

### Step 6: Start the Server

```bash
python scripts/run_dev_server.py
```

Server will start at: `http://localhost:8000`

---

## Your First Query

### Option 1: Using the API Docs (Easiest)

1. Open browser: http://localhost:8000/docs
2. Click on `POST /api/v1/auth/login`
3. Click "Try it out"
4. Fill in credentials:
 - username: `admin`
 - password: `admin123`
5. Click "Execute"
6. Copy the `access_token` from the response

7. Click on `POST /api/v1/query/`
8. Click "Try it out"
9. Click the icon and paste your token
10. Enter your question in the request body:
```json
{
 "question": "What is the total revenue?",
 "explain": true
}
```
11. Click "Execute"

### Option 2: Using curl

**1. Get Access Token:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
 -H "Content-Type: application/x-www-form-urlencoded" \
 -d "username=admin&password=admin123"
```

Response:
```json
{
 "access_token": "eyJ0eXAiOiJKV1...",
 "token_type": "bearer"
}
```

**2. Query with Natural Language:**
```bash
curl -X POST "http://localhost:8000/api/v1/query/" \
 -H "Authorization: Bearer YOUR_TOKEN_HERE" \
 -H "Content-Type: application/json" \
 -d '{
 "question": "What is the total revenue?",
 "explain": true
 }'
```

Response:
```json
{
 "question": "What is the total revenue?",
 "generated_sql": "SELECT SUM(SALES) FROM sales;",
 "validation": {
 "is_valid": true,
 "safety_explanation": "Query passed all safety checks."
 },
 "results": [
 {"SUM(SALES)": 9600.0}
 ],
 "row_count": 1,
 "execution_time_ms": 45.2,
 "explanation": "This query calculates the sum of all sales..."
}
```

### Option 3: Using Python

```python
import requests

# 1. Login
login_url = "http://localhost:8000/api/v1/auth/login"
login_data = {"username": "admin", "password": "admin123"}
response = requests.post(login_url, data=login_data)
token = response.json()["access_token"]

# 2. Query
query_url = "http://localhost:8000/api/v1/query/"
headers = {"Authorization": f"Bearer {token}"}
query_data = {
 "question": "How many orders were placed in 2003?",
 "explain": True
}
response = requests.post(query_url, json=query_data, headers=headers)
result = response.json()

print(f"SQL: {result['generated_sql']}")
print(f"Results: {result['results']}")
```

---

## Docker Quick Start (Alternative)

If you prefer Docker:

### Step 1: Clone and Configure

```bash
git clone https://github.com/Japyh/llm-based-dbms.git
cd llm-based-dbms
cp .env.example .env
```

### Step 2: Start Services

```bash
docker-compose up -d --build
```

This starts:
- API server (port 8000)
- PostgreSQL database (port 5432)
- Redis cache (port 6379)

### Step 3: Initialize Database

```bash
docker-compose exec api python scripts/init_db.py
```

### Step 4: Use the API

API is now available at: http://localhost:8000/docs

---

## Sample Queries to Try

Once you're authenticated, try these natural language questions:

1. **Basic Aggregation**
 ```
 "What is the total revenue from all sales?"
 ```

2. **Filtering**
 ```
 "Show me all orders from USA"
 ```

3. **Grouping**
 ```
 "What is the total sales per country?"
 ```

4. **Top N Queries**
 ```
 "Show the top 3 customers by total spending"
 ```

5. **Date Filtering**
 ```
 "How many orders were placed in 2003?"
 ```

6. **Product Analysis**
 ```
 "What are the most popular product lines?"
 ```

---

## Common Issues

### Issue: Module Import Errors

**Solution:**
```bash
# Make sure you're in the project root directory
cd llm-based-dbms

# Activate virtual environment
source venv/bin/activate # Linux/macOS
.\venv\Scripts\activate # Windows
```

### Issue: Database Not Found

**Solution:**
```bash
# Re-initialize database
python scripts/init_db.py
```

### Issue: API Not Starting

**Solution:**
```bash
# Check if port 8000 is already in use
# Windows:
netstat -ano | findstr :8000

# Linux/macOS:
lsof -i :8000

# Change port in .env:
API_PORT=8080
```

### Issue: LLM Provider Errors

**Solution:**
```bash
# Use mock provider (no API key needed)
# Edit .env:
LLM_PROVIDER=mock
```

For real LLM providers:
```bash
# OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here

# Anthropic
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

---

## Next Steps

### Learn More

1. **Architecture**: Read [docs/architecture.md](docs/architecture.md)
2. **API Reference**: See [docs/api_reference.md](docs/api_reference.md)
3. **Development**: Check [docs/developer_guide.md](docs/developer_guide.md)
4. **Deployment**: Read [docs/deployment_guide.md](docs/deployment_guide.md)

### Explore Features

1. **View Query History**:
 ```bash
 curl -H "Authorization: Bearer YOUR_TOKEN" \
 http://localhost:8000/api/v1/query/history
 ```

2. **Check Database Schema**:
 ```bash
 curl -H "Authorization: Bearer YOUR_TOKEN" \
 http://localhost:8000/api/v1/schema/
 ```

3. **Test Safety Validation**:
 ```json
 {
 "question": "DROP TABLE sales",
 "dry_run": true
 }
 ```
 This will be blocked by the safety engine!

### Customize

1. **Add Your Own Data**: Edit `scripts/init_db.py`
2. **Modify Safety Rules**: See `backend/safety/policies.py`
3. **Change LLM Provider**: Update `.env` file
4. **Add New Roles**: Edit `backend/auth/models.py`

### Run Tests

```bash
# Install dev dependencies
pip install pytest pytest-cov

# Run tests
pytest backend/tests/ -v
```

### Evaluate Performance

```bash
# Run evaluation script
python -m experiments.evaluate_text_to_sql
```

---

## 🆘 Getting Help

- **Documentation**: See `docs/` directory
- **Issues**: https://github.com/Japyh/llm-based-dbms/issues
- **Academic Contact**: Eskişehir Technical University, EEE Department

---

## Success!

You now have a working LLM-Based DBMS! 

**What you've set up:**
- Natural Language to SQL translation
- Multi-LLM provider support
- SQL safety validation
- Role-based access control
- Audit logging
- API with authentication
- Sample database with data

**Try it out and explore!**

For production deployment, security hardening, and advanced features, see the full documentation.
