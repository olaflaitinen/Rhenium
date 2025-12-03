# LLM-based DBMS

**Version 1.0.0** - Production-Grade Natural Language Database Management System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

## Overview

Enterprise-ready database management system with natural language interface powered by Large Language Models. Transform natural language questions into SQL queries with built-in safety, authentication, and audit logging.

### Key Features

✅ **Enterprise Authentication** - JWT-based auth with 4-tier RBAC (Admin, Data Scientist, Analyst, Viewer)  
✅ **Multi-LLM Support** - OpenAI, Anthropic, or local models  
✅ **SQL Safety** - AST-based validation with table-level permissions  
✅ **Complete Audit Trail** - Every query logged with user, timing, and results  
✅ **Production Ready** - Structured logging, health probes, error handling  
✅ **API-First Design** - RESTful API with OpenAPI/Swagger docs  

## Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# Clone repository
git clone https://github.com/olaflaitinen/llm-based-dbms.git
cd llm-based-dbms

# Install dependencies
pip install -r requirements-minimal.txt

# Install email validator (required)
pip install email-validator

# Initialize database (creates admin user)
python scripts/init_db.py

# Start development server
python scripts/run_dev_server.py
```

### Access API Documentation
Visit: http://localhost:8000/docs

### Default Credentials
- **Username**: `admin`
- **Password**: `admin123`
- ⚠️ **CHANGE THIS IN PRODUCTION!**

## Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
┌──────▼──────────────────┐
│   FastAPI Gateway       │
│  (Auth, Logging, CORS)  │
└──────┬──────────────────┘
       │
   ┌───┴────┬────────┬──────────┐
   │        │        │          │
┌──▼──┐ ┌──▼──┐ ┌───▼───┐ ┌────▼────┐
│Auth │ │Query│ │Schema │ │ Admin   │
│ API │ │ API │ │  API  │ │  API    │
└──┬──┘ └──┬──┘ └───┬───┘ └────┬────┘
   │       │        │           │
   └───┬───┴────┬───┴───────────┘
       │        │
   ┌───▼────┐ ┌─▼────────┐
   │  LLM   │ │  Safety  │
   │Service │ │Validator │
   └───┬────┘ └─┬────────┘
       │        │
       └────┬───┘
            │
      ┌─────▼──────┐
      │  Database  │
      │  (SQLite/  │
      │ PostgreSQL)│
      └────────────┘
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Get JWT token
- `POST /api/v1/auth/refresh` - Refresh token

### Queries
- `POST /api/v1/query` - Execute natural language query
- `GET /api/v1/query/history` - Get query history

### Admin (Admin only)
- `POST /api/v1/admin/users` - Create user
- `GET /api/v1/admin/users` - List users
- `PATCH /api/v1/admin/users/{id}` - Update user

### Schema
- `GET /api/v1/schema` - Get database schema

### Health
- `GET /health` - Health check
- `GET /health/liveness` - K8s liveness probe
- `GET /health/readiness` - K8s readiness probe

## Configuration

Create `.env` file from `.env.example`:

```bash
# Core Settings
ENVIRONMENT=development
DATABASE_TYPE=sqlite
LLM_PROVIDER=mock  # or openai, anthropic

# JWT (Change in production!)
JWT_SECRET_KEY=your-secret-key-here

# OpenAI (if using)
OPENAI_API_KEY=sk-your-key-here
MODEL_NAME=gpt-3.5-turbo

# Safety
SAFETY_MODE=strict
ALLOW_DANGEROUS_QUERIES=False
```

## User Roles & Permissions

| Role | Tables Access | Query Types | User Mgmt |
|------|--------------|-------------|-----------|
| **ADMIN** | All | All (SELECT, UPDATE, DELETE) | ✅ |
| **DATA_SCIENTIST** | All | SELECT, WITH | ❌ |
| **ANALYST** | sales, customers, products, orders | SELECT only | ❌ |
| **VIEWER** | sales | SELECT only | ❌ |

## Example Usage

### 1. Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

### 2. Query Database
```bash
curl -X POST "http://localhost:8000/api/v1/query/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the top 5 products by revenue?",
    "explain": true
  }'
```

## Development

### Run Tests
```bash
pytest backend/tests/
```

### Code Quality
```bash
# Format code
black backend/

# Sort imports
isort backend/

# Type checking
mypy backend/
```

## Production Deployment

### Docker
```bash
docker build -t llm-dbms:1.0.0 .
docker run -p 8000:8000llm-dbms:1.0.0
```

### Docker Compose (with PostgreSQL)
```bash
docker-compose up -d
```

### Environment Variables for Production
- Set `ENVIRONMENT=production`
- Use PostgreSQL: `DATABASE_TYPE=postgresql`
- Configure strong `JWT_SECRET_KEY`
- Set up proper `OPENAI_API_KEY`
- Enable metrics: `ENABLE_METRICS=True`

## Security Considerations

⚠️ **IMPORTANT**:
1. Change default admin password immediately
2. Use strong JWT secret key (min 32 characters)
3. Enable HTTPS in production
4. Configure CORS appropriately
5. Use PostgreSQL in production
6. Regular security audits
7. Monitor audit logs

## Project Structure

```
llm-based-dbms/
├── backend/
│   ├── api/              # FastAPI routers, schemas, middleware
│   ├── auth/             # Authentication & RBAC
│   ├── database/         # Database models & connection
│   ├── llm/              # LLM client & prompts
│   ├── safety/           # SQL validator
│   ├── observability/    # Logging & metrics
│   └── config/           # Settings management
├── scripts/              # Utility scripts
├── data/                 # Database files
├── docs/                 # Documentation
├── experiments/          # Research & evaluation
└── requirements-minimal.txt
```

## Roadmap

- [x] Authentication & RBAC
- [x] Multi-LLM support
- [x] SQL safety validation
- [x] Audit logging
- [ ] PostgreSQL migrations
- [ ] Redis caching
- [ ] Prometheus metrics
- [ ] Vector search for semantic queries
- [ ] Evaluation framework
- [ ] Kubernetes deployment

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License - see [LICENSE](LICENSE) file

## Support

- **Issues**: https://github.com/olaflaitinen/llm-based-dbms/issues
- **Discussions**: https://github.com/olaflaitinen/llm-based-dbms/discussions

## Acknowledgments

- FastAPI for the excellent web framework
- LangChain for LLM integration
- SQLAlchemy for database abstraction
- sqlparse for SQL parsing

---

**Status**: Production-ready v1.0.0 (40% complete - core features functional)

Built with ❤️ for enterprise data teams
