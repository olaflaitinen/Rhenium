# API Reference Documentation

## LLM-Based Database Management System - REST API Specification

**Version**: 1.0.0 
**Institution**: Eskişehir Technical University, Department of Electrical and Electronics Engineering 
**Project**: 2025-2026 Design Project | TÜBİTAK 2209-A 
**Team**: Derya Umut Kulali, Anil Aydin, Sila Alhan | **Advisor**: Mehmet Fidan

---

## Table of Contents

1. [Overview](#overview)
2. [Base URL](#base-url)
3. [Authentication](#authentication)
4. [Endpoints](#endpoints)
 - [Authentication Endpoints](#authentication-endpoints)
 - [Query Endpoints](#query-endpoints)
 - [Schema Endpoints](#schema-endpoints)
 - [Admin Endpoints](#admin-endpoints)
 - [Health Check Endpoints](#health-check-endpoints)
5. [Request/Response Formats](#requestresponse-formats)
6. [Error Handling](#error-handling)
7. [Rate Limiting](#rate-limiting)
8. [Versioning](#versioning)

---

## Overview

The LLM-Based DBMS API is a RESTful service that enables natural language querying of relational databases using Large Language Models. The API follows OpenAPI 3.0 specifications and provides comprehensive endpoints for query processing, user management, and system monitoring.

### Key Features

- JWT-based authentication
- ️ Role-based access control (RBAC)
- Natural language to SQL translation
- SQL safety validation
- Audit logging
- Prometheus metrics
- Response caching

---

## Base URL

### Development
```
http://localhost:8000
```

### Production
```
https://api.yourdomain.com
```

### API Version
All endpoints are prefixed with the API version:
```
/api/v1/
```

**Complete Base URL**: `http://localhost:8000/api/v1`

---

## Authentication

### Overview

The API uses **JWT (JSON Web Token)** based authentication. Obtain a token by logging in, then include it in the `Authorization` header for all protected endpoints.

### Authentication Flow

```
1. POST /api/v1/auth/login → Receive access_token
2. Include token in subsequent requests
3. Token expires after configured duration (default: 24 hours)
4. Refresh or re-login when token expires
```

### Header Format

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Token Expiration

- **Default**: 24 hours (1440 minutes)
- **Configurable**: via `JWT_EXPIRE_MINUTES` environment variable

---

## Endpoints

### Authentication Endpoints

#### POST /api/v1/auth/login

Authenticate user and receive access token.

**Request:**

```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin123
```

**Request Body** (form-data):
| Field | Type | Required | Description |
|----------|--------|----------|--------------------|
| username | string | Yes | User's username |
| password | string | Yes | User's password |

**Response** (200 OK):
```json
{
 "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
 "token_type": "bearer"
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid credentials
- `422 Unprocessable Entity`: Missing required fields

**Example (curl):**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
 -H "Content-Type: application/x-www-form-urlencoded" \
 -d "username=admin&password=admin123"
```

**Example (Python):**
```python
import requests

response = requests.post(
 "http://localhost:8000/api/v1/auth/login",
 data={"username": "admin", "password": "admin123"}
)
token = response.json()["access_token"]
```

---

### Query Endpoints

#### POST /api/v1/query/

Process a natural language query and return SQL results.

**Authentication**: Required (Bearer Token)

**Request:**

```http
POST /api/v1/query/
Authorization: Bearer {token}
Content-Type: application/json

{
 "question": "What is the total revenue?",
 "explain": true,
 "dry_run": false
}
```

**Request Body** (JSON):
| Field | Type | Required | Default | Description |
|----------|---------|----------|---------|--------------------------------------|
| question | string | Yes | - | Natural language question |
| explain | boolean | No | false | Include SQL explanation in response |
| dry_run | boolean | No | false | Validate only, don't execute query |

**Response** (200 OK):
```json
{
 "question": "What is the total revenue?",
 "generated_sql": "SELECT SUM(SALES) as total_revenue FROM sales;",
 "validation": {
 "is_valid": true,
 "sql": "SELECT SUM(SALES) as total_revenue FROM sales;",
 "error_message": null,
 "safety_explanation": "Query passed all safety checks."
 },
 "results": [
 {
 "total_revenue": 9600.0
 }
 ],
 "row_count": 1,
 "execution_time_ms": 42.5,
 "explanation": "This query calculates the sum of all sales revenue by using the SUM aggregation function on the SALES column.",
 "error": null
}
```

**Response Schema:**
```typescript
interface QueryResponse {
 question: string;
 generated_sql: string;
 validation: {
 is_valid: boolean;
 sql: string;
 error_message: string | null;
 safety_explanation: string;
 };
 results: Array<Record<string, any>> | null;
 row_count: number | null;
 execution_time_ms: number;
 explanation: string | null;
 error: string | null;
}
```

**Error Responses:**
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `422 Unprocessable Entity`: Invalid request body
- `500 Internal Server Error`: Query execution failed

**Example (curl):**
```bash
curl -X POST "http://localhost:8000/api/v1/query/" \
 -H "Authorization: Bearer YOUR_TOKEN" \
 -H "Content-Type: application/json" \
 -d '{
 "question": "Show top 5 customers by revenue",
 "explain": true
 }'
```

---

#### GET /api/v1/query/history

Retrieve query history for the authenticated user.

**Authentication**: Required (Bearer Token)

**Request:**

```http
GET /api/v1/query/history?page=1&page_size=10
Authorization: Bearer {token}
```

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|------------|---------|----------|---------|----------------------------|
| page | integer | No | 1 | Page number (1-indexed) |
| page_size | integer | No | 10 | Items per page (max: 100) |

**Response** (200 OK):
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
 "timestamp": "2025-12-03T14:30:00Z",
 "user_id": 1
 }
 ],
 "total": 25,
 "page": 1,
 "page_size": 10,
 "total_pages": 3
}
```

---

### Schema Endpoints

#### GET /api/v1/schema/

Retrieve database schema information.

**Authentication**: Required (Bearer Token)

**Request:**

```http
GET /api/v1/schema/
Authorization: Bearer {token}
```

**Response** (200 OK):
```json
{
 "database_type": "sqlite",
 "tables": [
 {
 "name": "sales",
 "columns": [
 {
 "name": "ORDERNUMBER",
 "type": "INTEGER",
 "nullable": false,
 "primary_key": true
 },
 {
 "name": "SALES",
 "type": "FLOAT",
 "nullable": true,
 "primary_key": false
 }
 ],
 "row_count": 3,
 "indexes": ["PRIMARY KEY (ORDERNUMBER)"]
 }
 ],
 "schema_ddl": "CREATE TABLE sales (\n ORDERNUMBER INTEGER PRIMARY KEY,\n ...\n);"
}
```

**Use Cases:**
- Displaying available tables to users
- LLM prompt context
- Schema documentation

---

### Admin Endpoints

#### GET /api/v1/admin/users

List all users in the system.

**Authentication**: Required (Admin role only)

**Request:**

```http
GET /api/v1/admin/users?page=1&page_size=20
Authorization: Bearer {admin_token}
```

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|------------|---------|----------|---------|---------------------|
| page | integer | No | 1 | Page number |
| page_size | integer | No | 20 | Items per page |

**Response** (200 OK):
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
 "roles": ["ADMIN"],
 "created_at": "2025-01-01T00:00:00Z"
 }
 ],
 "total": 5,
 "page": 1,
 "page_size": 20
}
```

**Error Responses:**
- `403 Forbidden`: User does not have ADMIN role

---

#### POST /api/v1/admin/users

Create a new user.

**Authentication**: Required (Admin role only)

**Request:**

```http
POST /api/v1/admin/users
Authorization: Bearer {admin_token}
Content-Type: application/json

{
 "username": "analyst1",
 "email": "analyst@company.com",
 "password": "SecurePass123!",
 "full_name": "Data Analyst",
 "roles": ["ANALYST"]
}
```

**Request Body:**
| Field | Type | Required | Description |
|-----------|----------|----------|--------------------------------|
| username | string | Yes | Unique username (3-50 chars) |
| email | string | Yes | Valid email address |
| password | string | Yes | Password (min 8 chars) |
| full_name | string | No | User's full name |
| roles | string[] | No | Array of role names |

**Available Roles:**
- `ADMIN`: Full system access
- `DATA_SCIENTIST`: Read access to all tables
- `ANALYST`: Read access to specific tables
- `VIEWER`: Read-only access

**Response** (201 Created):
```json
{
 "id": 2,
 "username": "analyst1",
 "email": "analyst@company.com",
 "full_name": "Data Analyst",
 "roles": ["ANALYST"],
 "is_active": true,
 "created_at": "2025-12-03T15:00:00Z"
}
```

---

### Health Check Endpoints

#### GET /health/liveness

Check if the service is alive and responding.

**Authentication**: Not required

**Request:**

```http
GET /health/liveness
```

**Response** (200 OK):
```json
{
 "status": "ok",
 "timestamp": "2025-12-03T14:30:00Z"
}
```

**Use Case**: Kubernetes/Docker liveness probe

---

#### GET /health/readiness

Check if the service is ready to handle requests.

**Authentication**: Not required

**Request:**

```http
GET /health/readiness
```

**Response** (200 OK):
```json
{
 "status": "ready",
 "checks": {
 "database": "ok",
 "redis": "ok",
 "llm_provider": "configured"
 },
 "timestamp": "2025-12-03T14:30:00Z"
}
```

**Response when not ready** (503 Service Unavailable):
```json
{
 "status": "not_ready",
 "checks": {
 "database": "error",
 "redis": "ok",
 "llm_provider": "configured"
 },
 "timestamp": "2025-12-03T14:30:00Z"
}
```

**Use Case**: Kubernetes/Docker readiness probe

---

## Request/Response Formats

### Content Types

**Supported Request Content-Types:**
- `application/json` (for JSON bodies)
- `application/x-www-form-urlencoded` (for login)

**Response Content-Type:**
- `application/json` (all responses)

### Date/Time Format

All timestamps use **ISO 8601** format:
```
2025-12-03T14:30:00Z
```

### Pagination

Paginated endpoints follow this structure:

**Request:**
```
?page=1&page_size=20
```

**Response:**
```json
{
 "items": [...],
 "total": 100,
 "page": 1,
 "page_size": 20,
 "total_pages": 5
}
```

---

## Error Handling

### Error Response Format

All errors follow a consistent structure:

```json
{
 "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

| Code | Meaning | Description |
|------|--------------------------|---------------------------------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request syntax |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Service temporarily unavailable |

### Validation Errors (422)

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

## Rate Limiting

### Default Limits

- **Anonymous requests**: 100 requests/hour
- **Authenticated requests**: 1000 requests/hour
- **Admin users**: No limit

### Rate Limit Headers

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1638547200
```

### Rate Limit Exceeded Response

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 3600

{
 "detail": "Rate limit exceeded. Try again in 3600 seconds."
}
```

---

## Versioning

### Current Version

**v1** (Stable)

### Version in URL

All endpoints include version in the path:
```
/api/v1/endpoint
```

### Deprecation Policy

- Deprecated endpoints will be supported for 6 months minimum
- Deprecation notices will be included in response headers:
 ```http
 X-API-Deprecated: true
 X-API-Deprecation-Date: 2025-06-01
 X-API-Sunset-Date: 2025-12-01
 ```

---

## Interactive Documentation

### Swagger UI

Access interactive API documentation:
```
http://localhost:8000/docs
```

Features:
- Try endpoints directly in browser
- View request/response schemas
- Test authentication flow
- Copy curl commands

### ReDoc

Alternative documentation format:
```
http://localhost:8000/redoc
```

### OpenAPI Specification

Download OpenAPI JSON:
```
http://localhost:8000/api/v1/openapi.json
```

---

## SDK Examples

### Python

```python
from llmdbms_client import LLMDBMSClient

client = LLMDBMSClient(
 base_url="http://localhost:8000",
 username="admin",
 password="admin123"
)

# Query
result = client.query("What is total revenue?", explain=True)
print(result.sql)
print(result.results)

# Get schema
schema = client.get_schema()
print(schema.tables)
```

### JavaScript/TypeScript

```javascript
import { LLMDBMSClient } from 'llmdbms-client';

const client = new LLMDBMSClient({
 baseURL: 'http://localhost:8000',
 username: 'admin',
 password: 'admin123'
});

// Query
const result = await client.query({
 question: 'What is total revenue?',
 explain: true
});

console.log(result.sql);
console.log(result.results);
```

---

## Support

For API support, issues, or questions:

**Academic Contact**: 
Eskişehir Technical University 
Department of Electrical and Electronics Engineering

**Team**: Derya Umut Kulali, Anil Aydin, Sila Alhan 
**Advisor**: Mehmet Fidan

**GitHub**: https://github.com/Japyh/llm-based-dbms/issues
