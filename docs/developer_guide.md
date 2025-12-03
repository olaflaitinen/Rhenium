# Developer Guide

## Setup

1. Clone repo
2. `python -m venv venv`
3. `source venv/bin/activate`
4. `pip install -r requirements-minimal.txt`

## Project Structure

- `backend/api`: FastAPI routers
- `backend/llm`: LLM integration
- `backend/safety`: SQL validation logic
- `backend/database`: Models and migrations

## Running Tests

```bash
pytest
```

## Adding a new LLM Provider

1. Extend `LLMClient` in `backend/llm/client.py`.
2. Register in `LLMClientFactory`.
