# API Usage Examples

Comprehensive examples for using the LLM-Based DBMS API.

## Table of Contents

1. [Authentication](#authentication)
2. [Natural Language Queries](#natural-language-queries)
3. [Schema Exploration](#schema-exploration)
4. [Query History](#query-history)
5. [User Management](#user-management)
6. [Health Checks](#health-checks)
7. [Error Handling](#error-handling)
8. [Advanced Use Cases](#advanced-use-cases)

---

## Authentication

### Login and Get Token

**curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin123"
```

**Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    data={"username": "admin", "password": "admin123"}
)

token = response.json()["access_token"]
print(f"Token: {token}")
```

**JavaScript:**
```javascript
const formData = new URLSearchParams();
formData.append('username', 'admin');
formData.append('password', 'admin123');

fetch('http://localhost:8000/api/v1/auth/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/x-www-form-urlencoded'},
  body: formData
})
.then(res => res.json())
.then(data => console.log('Token:', data.access_token));
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

---

## Natural Language Queries

### Basic Query

**curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/query/" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "What is the total revenue?",
       "explain": false
     }'
```

**Python:**
```python
headers = {"Authorization": f"Bearer {token}"}
payload = {
    "question": "What is the total revenue?",
    "explain": False
}

response = requests.post(
    "http://localhost:8000/api/v1/query/",
    headers=headers,
    json=payload
)

result = response.json()
print(f"SQL: {result['generated_sql']}")
print(f"Results: {result['results']}")
```

**Response:**
```json
{
  "question": "What is the total revenue?",
  "generated_sql": "SELECT SUM(SALES) as total_revenue FROM sales;",
  "validation": {
    "is_valid": true,
    "sql": "SELECT SUM(SALES) as total_revenue FROM sales;",
    "safety_explanation": "Query passed all safety checks."
  },
  "results": [
    {"total_revenue": 9600.0}
  ],
  "row_count": 1,
  "execution_time_ms": 42.5,
  "explanation": null,
  "error": null
}
```

### Query with Explanation

**curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/query/" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "Show top 3 products by sales",
       "explain": true
     }'
```

**Response:**
```json
{
  "question": "Show top 3 products by sales",
  "generated_sql": "SELECT PRODUCTCODE, SUM(SALES) as total_sales FROM sales GROUP BY PRODUCTCODE ORDER BY total_sales DESC LIMIT 3;",
  "validation": {
    "is_valid": true,
    "safety_explanation": "Query passed all safety checks."
  },
  "results": [
    {"PRODUCTCODE": "S18_3232", "total_sales": 3600.0},
    {"PRODUCTCODE": "S24_2022", "total_sales": 3000.0},
    {"PRODUCTCODE": "S18_1749", "total_sales": 3000.0}
  ],
  "row_count": 3,
  "execution_time_ms": 55.3,
  "explanation": "This query groups sales by product code, calculates the total sales for each product, and returns the top 3 products ordered by their total sales in descending order."
}
```

### Dry Run (Validation Only)

**curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/query/" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "Delete all sales records",
       "dry_run": true
     }'
```

**Python:**
```python
payload = {
    "question": "Delete all sales records",
    "dry_run": True  # Won't execute, just validate
}

response = requests.post(
    "http://localhost:8000/api/v1/query/",
    headers=headers,
    json=payload
)

result = response.json()
print(f"Valid: {result['validation']['is_valid']}")
print(f"Reason: {result['validation']['error_message']}")
```

**Response:**
```json
{
  "question": "Delete all sales records",
  "generated_sql": "DELETE FROM sales;",
  "validation": {
    "is_valid": false,
    "sql": "DELETE FROM sales;",
    "error_message": "Forbidden command 'DELETE'. Allowed: ['SELECT']",
    "safety_explanation": "This query was blocked because DELETE operations are not permitted..."
  },
  "results": null,
  "row_count": null,
  "execution_time_ms": 15.0,
  "explanation": null,
  "error": null
}
```

---

## Schema Exploration

### Get Database Schema

**curl:**
```bash
curl -X GET "http://localhost:8000/api/v1/schema/" \
     -H "Authorization: Bearer YOUR_TOKEN"
```

**Python:**
```python
response = requests.get(
    "http://localhost:8000/api/v1/schema/",
    headers=headers
)

schema = response.json()
print("Tables:", schema['tables'])
print("DDL:", schema['schema_ddl'])
```

**Response:**
```json
{
  "database_type": "sqlite",
  "tables": [
    {
      "name": "sales",
      "columns": [
        {"name": "ORDERNUMBER", "type": "INTEGER"},
        {"name": "QUANTITYORDERED", "type": "INTEGER"},
        {"name": "PRICEEACH", "type": "FLOAT"},
        {"name": "SALES", "type": "FLOAT"},
        {"name": "ORDERDATE", "type": "DATE"},
        {"name": "STATUS", "type": "VARCHAR"},
        {"name": "PRODUCTCODE", "type": "VARCHAR"},
        {"name": "CUSTOMERNAME", "type": "VARCHAR"},
        {"name": "COUNTRY", "type": "VARCHAR"}
      ],
      "row_count": 3
    }
  ],
  "schema_ddl": "CREATE TABLE sales (\n  ORDERNUMBER INTEGER PRIMARY KEY,\n  ..."
}
```

---

## Query History

### Get User's Query History

**curl:**
```bash
curl -X GET "http://localhost:8000/api/v1/query/history?page=1&page_size=10" \
     -H "Authorization: Bearer YOUR_TOKEN"
```

**Python:**
```python
params = {"page": 1, "page_size": 10}
response = requests.get(
    "http://localhost:8000/api/v1/query/history",
    headers=headers,
    params=params
)

history = response.json()
for query in history['queries']:
    print(f"Question: {query['question']}")
    print(f"SQL: {query['generated_sql']}")
    print(f"Status: {query['execution_status']}")
    print("---")
```

**Response:**
```json
{
  "queries": [
    {
      "id": 1,
      "question": "What is the total revenue?",
      "generated_sql": "SELECT SUM(SALES) FROM sales;",
      "execution_status": "success",
      "execution_time_ms": 42.5,
      "rows_returned": 1,
      "timestamp": "2025-12-03T14:30:00",
      "user_id": 1
    },
    {
      "id": 2,
      "question": "Show top products",
      "generated_sql": "SELECT * FROM sales LIMIT 5;",
      "execution_status": "success",
      "execution_time_ms": 38.2,
      "rows_returned": 5,
      "timestamp": "2025-12-03T14:35:00",
      "user_id": 1
    }
  ],
  "total": 2
}
```

---

## User Management

### List All Users (Admin Only)

**curl:**
```bash
curl -X GET "http://localhost:8000/api/v1/admin/users" \
     -H "Authorization: Bearer ADMIN_TOKEN"
```

**Response:**
```json
{
  "users": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@llmdbms.local",
      "full_name": "System Administrator",
      "is_active": true,
      "is_superuser": true,
      "roles": ["ADMIN"]
    },
    {
      "id": 2,
      "username": "analyst1",
      "email": "analyst@company.com",
      "full_name": "Data Analyst",
      "is_active": true,
      "is_superuser": false,
      "roles": ["ANALYST"]
    }
  ]
}
```

### Create New User (Admin Only)

**curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/admin/users" \
     -H "Authorization: Bearer ADMIN_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "newuser",
       "email": "newuser@example.com",
       "password": "secure_password",
       "full_name": "New User",
       "roles": ["ANALYST"]
     }'
```

**Python:**
```python
new_user = {
    "username": "analyst2",
    "email": "analyst2@company.com",
    "password": "SecurePass123!",
    "full_name": "Junior Analyst",
    "roles": ["ANALYST"]
}

response = requests.post(
    "http://localhost:8000/api/v1/admin/users",
    headers=headers,
    json=new_user
)

created_user = response.json()
print(f"Created user: {created_user['username']}")
```

---

## Health Checks

### Liveness Probe

**curl:**
```bash
curl -X GET "http://localhost:8000/health/liveness"
```

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-12-03T14:30:00"
}
```

### Readiness Probe

**curl:**
```bash
curl -X GET "http://localhost:8000/health/readiness"
```

**Response:**
```json
{
  "status": "ready",
  "checks": {
    "database": "ok",
    "redis": "ok",
    "llm_provider": "configured"
  },
  "timestamp": "2025-12-03T14:30:00"
}
```

---

## Error Handling

### Handle Authentication Errors

**Python:**
```python
try:
    response = requests.post(
        "http://localhost:8000/api/v1/auth/login",
        data={"username": "wrong", "password": "wrong"}
    )
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    if response.status_code == 401:
        print("Invalid credentials")
    else:
        print(f"Error: {e}")
```

**Response (401 Unauthorized):**
```json
{
  "detail": "Incorrect username or password"
}
```

### Handle Validation Errors

**Python:**
```python
payload = {
    "question": "",  # Empty question
    "explain": False
}

try:
    response = requests.post(
        "http://localhost:8000/api/v1/query/",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    error_detail = response.json()
    print(f"Validation error: {error_detail}")
```

**Response (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "loc": ["body", "question"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Advanced Use Cases

### Batch Queries

**Python:**
```python
questions = [
    "What is the total revenue?",
    "How many orders in 2003?",
    "Show top 3 customers"
]

results = []
for question in questions:
    response = requests.post(
        "http://localhost:8000/api/v1/query/",
        headers=headers,
        json={"question": question, "explain": False}
    )
    results.append(response.json())

# Analyze results
for result in results:
    print(f"Q: {result['question']}")
    print(f"SQL: {result['generated_sql']}")
    print(f"Time: {result['execution_time_ms']}ms")
    print("---")
```

### Async Requests

**Python (async):**
```python
import asyncio
import aiohttp

async def query(session, question):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"question": question, "explain": False}
    
    async with session.post(
        "http://localhost:8000/api/v1/query/",
        headers=headers,
        json=payload
    ) as response:
        return await response.json()

async def main():
    questions = [
        "Total revenue?",
        "Orders in 2003?",
        "Top customers?"
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = [query(session, q) for q in questions]
        results = await asyncio.gather(*tasks)
        
        for result in results:
            print(f"{result['question']}: {result['execution_time_ms']}ms")

asyncio.run(main())
```

### Retry Logic with Exponential Backoff

**Python:**
```python
import time
import requests

def query_with_retry(question, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(
                "http://localhost:8000/api/v1/query/",
                headers=headers,
                json={"question": question},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retry {attempt + 1} after {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise

result = query_with_retry("What is the total revenue?")
```

### Session Management

**Python:**
```python
class LLMDBMSClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.session = requests.Session()
        self.login(username, password)
    
    def login(self, username, password):
        response = self.session.post(
            f"{self.base_url}/api/v1/auth/login",
            data={"username": username, "password": password}
        )
        token = response.json()["access_token"]
        self.session.headers.update({"Authorization": f"Bearer {token}"})
    
    def query(self, question, explain=False, dry_run=False):
        response = self.session.post(
            f"{self.base_url}/api/v1/query/",
            json={
                "question": question,
                "explain": explain,
                "dry_run": dry_run
            }
        )
        return response.json()
    
    def get_schema(self):
        response = self.session.get(f"{self.base_url}/api/v1/schema/")
        return response.json()

# Usage
client = LLMDBMSClient(
    "http://localhost:8000",
    "admin",
    "admin123"
)

result = client.query("What is the total revenue?", explain=True)
print(result)
```

---

## Best Practices

1. **Always use HTTPS in production**
2. **Store tokens securely** (environment variables, secure storage)
3. **Implement token refresh** if using long-running sessions
4. **Handle rate limits** with exponential backoff
5. **Validate responses** before using data
6. **Log errors** for debugging
7. **Use dry_run** to test queries safely
8. **Cache responses** when appropriate

---

For more examples, see the [test suite](../backend/tests/) and [experiments](../experiments/) directory.
