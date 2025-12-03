# API Reference

The LLM-based DBMS API follows RESTful principles.

## Base URL
`http://localhost:8000/api/v1`

## Authentication
All protected endpoints require a Bearer Token.
`Authorization: Bearer <token>`

## Endpoints

### Query
- **POST /query/**
  - Process a natural language query.
  - Body: `{"question": "string", "explain": boolean, "dry_run": boolean}`
  - Response: `{"sql": "string", "results": [], ...}`

- **GET /query/history**
  - Get past queries.

### Schema
- **GET /schema/**
  - Get database schema information.

### Auth
- **POST /auth/login**
  - Get access token.
  - Body: `username`, `password` (form-data)

### Admin
- **GET /admin/users**
  - List users (Admin only).

### Health
- **GET /health/liveness**
- **GET /health/readiness**
