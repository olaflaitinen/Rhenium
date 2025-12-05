# Changelog

All notable changes to the LLM-Based DBMS project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-03

### Added

#### Core Features
- **Natural Language to SQL Pipeline**: Complete implementation of NL → LLM → SQL → Safety → DB flow
- **Multi-Provider LLM Support**: OpenAI (GPT-3.5/4), Anthropic (Claude), and Mock providers via LangChain
- **Advanced Safety Engine**: AST-based SQL validation using sqlparse with policy-based rules
- **Role-Based Access Control (RBAC)**: Four permission levels (Admin, Data Scientist, Analyst, Viewer)
- **JWT Authentication**: Secure token-based authentication with configurable expiration
- **Audit Logging**: Complete tracking of all query attempts with validation status
- **Response Caching**: Redis-based LLM response caching to reduce costs and latency
- **Prometheus Metrics**: Comprehensive observability with request counts, latencies, and error rates

#### API Endpoints
- `POST /api/v1/query/`: Process natural language queries
- `GET /api/v1/query/history`: Retrieve query history
- `POST /api/v1/auth/login`: User authentication
- `GET /api/v1/schema/`: Database schema introspection
- `GET /api/v1/admin/users`: User management (Admin only)
- `GET /health/liveness`: Liveness probe
- `GET /health/readiness`: Readiness probe

#### Database Features
- **Multi-Backend Support**: SQLite (development) and PostgreSQL (production)
- **Sample Sales Database**: Pre-populated with sales orders data
- **Alembic Migrations**: Database version control
- **Connection Pooling**: Efficient database connection management
- **Default User Creation**: Automatic admin user setup

#### Developer Experience
- **Comprehensive Documentation**: README, architecture docs, API reference, deployment guide
- **Docker Support**: Multi-stage Dockerfile with health checks
- **Docker Compose**: Full stack orchestration (API + PostgreSQL + Redis)
- **Kubernetes Manifests**: Deployment, Service, ConfigMap for K8s deployments
- **GitHub Actions CI/CD**: Automated testing, linting, and Docker builds
- **Development Scripts**: Database initialization, development server launcher
- **Testing Framework**: pytest with coverage reporting

#### Security Features
- **SQL Injection Prevention**: Multiple layers of protection
- **Destructive Operation Blocking**: Prevents DROP, DELETE, UPDATE by default
- **Table-Level Access Control**: RBAC-enforced table permissions
- **Environment-Based Configuration**: No hardcoded secrets
- **CORS Configuration**: Production-ready CORS settings
- **Input Validation**: Pydantic models for all API requests

### Documentation
- **README.md**: Comprehensive project overview with academic context
- **Architecture Documentation**: Detailed system design and data flow
- **API Reference**: Complete endpoint documentation
- **Deployment Guide**: Docker, Docker Compose, and Kubernetes instructions
- **Developer Guide**: Setup and contribution guidelines
- **Research Background**: Text-to-SQL literature review
- **Project Plan**: Milestone tracking
- **CONTRIBUTING.md**: Contribution guidelines
- **SECURITY.md**: Security policy and best practices
- **CHANGELOG.md**: Version history

### Academic Attribution
- **Team Members**: Derya Umut Kulalı (Principal Investigator), Anıl Aydın, Sıla Alhan
- **Academic Advisor**: Mehmet Fidan
- **Institution**: Eskişehir Technical University, Department of Electrical and Electronics Engineering
- **Funding**: TÜBİTAK 2209-A University Students Research Projects Support Program
- **Academic Context**: 2025-2026 Design Project
- **Citation**: BibTeX format with all team members

### Infrastructure
- **Python 3.11+**: Modern Python with type hints throughout
- **FastAPI**: High-performance async API framework
- **SQLAlchemy 2.0**: Modern ORM with async support
- **Pydantic V2**: Advanced data validation
- **Structured Logging**: JSON-formatted logs with structlog
- **Prometheus Client**: Metrics export for monitoring

### Configuration Files
- `.env.example`: Template for environment variables
- `pyproject.toml`: Modern Python project configuration
- `requirements.txt`: Production dependencies
- `requirements-minimal.txt`: Minimal dependency set
- `docker-compose.yml`: Multi-container orchestration
- `.gitignore`: Comprehensive ignore patterns
- `.gitattributes`: Line ending normalization
- `alembic.ini`: Database migration configuration

### Fixed
- **Duplicate Directory Structure**: Removed duplicate `backend/db/` directory, consolidated to `backend/database/`
- **Import Inconsistencies**: Unified all imports to use `backend.database.*`
- **Documentation References**: Updated architecture.md to reference correct directory structure
- **Team Attribution**: Added all three student team members to README and documentation
- **Project Metadata**: Updated pyproject.toml with individual team member names
- **License**: Updated copyright to include all team members

### Changed
- **README Structure**: Reorganized with clear sections and table of contents
- **Team Section**: Expanded to list all team members with roles
- **Citation**: Updated BibTeX to include all authors
- **Safety Mode**: Default changed to "strict" for better security

## [Unreleased]

### Planned Features
- [ ] Column-level RBAC
- [ ] Multi-turn conversation support with context management
- [ ] Vector search for schema documentation
- [ ] Web-based UI (React/Next.js)
- [ ] Support for local LLM providers (Ollama, vLLM)
- [ ] Query result visualization
- [ ] Advanced caching strategies
- [ ] Performance optimizations
- [ ] MySQL/MariaDB support
- [ ] Query explanation with visual diagrams
- [ ] Fine-tuned models for Turkish language support

### Under Consideration
- GraphQL API support
- Real-time query execution with WebSocket
- Interactive query builder
- Query performance analytics
- Automated query optimization suggestions
- Integration with BI tools (Tableau, Power BI)
- Voice interface for queries

## Version History

### Version 1.0.0 (2025-12-03)
- Initial production-ready release
- Complete NL-to-SQL pipeline implementation
- Comprehensive security and safety features
- Full documentation and academic attribution
- Docker and Kubernetes deployment support
- CI/CD pipeline with automated testing

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## Team & Contact

**Student Team Members:**
- Derya Umut Kulalı (Principal Investigator)
- Anıl Aydın
- Sıla Alhan

**Academic Advisor:**
- Mehmet Fidan

**Institution:**
Eskişehir Technical University  
Department of Electrical and Electronics Engineering

**Project:**
2025-2026 Design Project  
TÜBİTAK 2209-A Research Project

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
