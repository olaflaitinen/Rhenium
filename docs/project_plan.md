# Project Plan and Roadmap

## LLM-Based Database Management System

**Institution**: Eskişehir Technical University 
**Department**: Electrical and Electronics Engineering 
**Project Type**: 2025–2026 Design Project 
**Funding**: TÜBİTAK 2209-A University Students Research Projects Support Programme 
**Duration**: 8 months (2 academic semesters)

---

## Team

### Student Researchers
- **Derya Umut Kulalı** - Principal Investigator / Project Lead
- **Anıl Aydın** - Research Team Member
- **Sıla Alhan** - Research Team Member

### Academic Supervision
- **Mehmet Fidan** - Academic Advisor, Department of Electrical and Electronics Engineering

---

## Project Overview

### Objective

Develop a production-grade Database Management System with a Natural Language Interface powered by Large Language Models, enabling non-technical users to query relational databases using natural language instead of SQL.

### Problem Statement

Traditional database systems require SQL knowledge, creating barriers for:
- Business analysts and stakeholders
- Domain experts without programming background
- Students and educators
- Decision makers needing quick data insights

### Proposed Solution

An intelligent DBMS that:
1. Accepts natural language questions
2. Translates them to SQL using LLMs
3. Validates queries for safety and access control
4. Executes queries securely
5. Returns results with explanations

---

## Project Scope

### In Scope

 **Core Features**
- Natural language to SQL translation
- Multi-provider LLM support (OpenAI, Anthropic, local models)
- Advanced SQL safety validation (AST-based)
- Role-based access control (RBAC)
- JWT authentication
- Audit logging
- Response caching
- REST API with FastAPI
- Docker deployment
- Kubernetes manifests

 **Database Support**
- SQLite (development)
- PostgreSQL (production)

 **Evaluation Framework**
- Text-to-SQL benchmarking
- Accuracy metrics (exact match, execution accuracy)
- Performance profiling

 **Documentation**
- Technical documentation
- API reference
- Deployment guides
- Research background

### Out of Scope (Future Work)

 GraphQL API support
 Real-time WebSocket queries
 Multi-database join queries
 Voice interface
 Mobile applications
 MySQL/MariaDB/SQL Server support
 Query result visualization (charts/graphs)
 Data modification operations (INSERT, UPDATE, DELETE)

---

## Timeline and Milestones

### Academic Year 2025-2026

#### Semester 1 (September 2025 - January 2026)

**Month 1-2: Planning and Research (September - October 2025)**
- [x] Literature review on Text-to-SQL systems
- [x] Technology stack selection
- [x] Architecture design
- [x] Project proposal submission to TÜBİTAK
- [x] Repository setup
- [x] Development environment configuration

**Month 3-4: Core Implementation (November - December 2025)**
- [x] Database layer implementation
- [x] LLM integration (OpenAI, Anthropic)
- [x] Basic API endpoints
- [x] Authentication system
- [x] SQL safety validator (basic)
- [x] Unit tests

**Month 5: Advanced Features (January 2026)**
- [x] RBAC implementation
- [x] Advanced SQL validation (AST-based)
- [x] Caching layer (Redis)
- [x] Prometheus metrics
- [x] Structured logging
- [x] Integration tests

#### Semester 2 (February 2026 - June 2026)

**Month 6: Evaluation and Optimization (February 2026)**
- [ ] Evaluation dataset creation
- [ ] Benchmark implementation
- [ ] Performance profiling
- [ ] Query optimization
- [ ] Cost analysis

**Month 7: Deployment and Testing (March 2026)**
- [x] Docker containerization
- [x] Kubernetes manifests
- [ ] Cloud deployment testing
- [ ] Security hardening
- [ ] Load testing
- [ ] Production readiness checklist

**Month 8: Documentation and Presentation (April - May 2026)**
- [x] Technical documentation
- [x] API documentation
- [x] Deployment guides
- [ ] Research paper draft
- [ ] Presentation preparation
- [ ] Demo video

**Final Presentation (June 2026)**
- [ ] Project presentation to university committee
- [ ] TÜBİTAK final report submission
- [ ] Public demo
- [ ] Open source release

---

## Detailed Milestones

### M1: Literature Review & Requirements (Completed: October 2025)

**Objectives:**
- Understand state-of-the-art Text-to-SQL approaches
- Identify key technologies and frameworks
- Define system requirements
- Draft initial architecture

**Deliverables:**
- Research background document
- Technology stack decision (Python, FastAPI, LangChain, SQLAlchemy)
- Architecture diagram
- Requirements specification

**Academic Output:**
- Literature review on Text-to-SQL benchmarks (Spider, WikiSQL, BIRD-SQL)
- Analysis of LLM capabilities for SQL generation

---

### M2: Prototype Implementation (Completed: December 2025)

**Objectives:**
- Implement minimal viable product (MVP)
- Demonstrate end-to-end natural language query flow
- Establish development practices

**Deliverables:**
- Backend API structure
- Database layer (SQLite)
- Basic LLM integration (OpenAI mock)
- Simple safety validator
- Authentication (JWT)
- Unit tests
- Docker setup

**Technical Achievements:**
- RESTful API with FastAPI
- SQLAlchemy ORM models
- LangChain LLM abstraction
- Pydantic validation schemas

---

### M3: Advanced Features (Completed: January 2026)

**Objectives:**
- Implement production-grade security features
- Add observability and monitoring
- Improve code quality and testing

**Deliverables:**
- Role-Based Access Control (RBAC)
- AST-based SQL parser (using sqlparse)
- Policy engine (strict/moderate/permissive modes)
- Redis caching layer
- Prometheus metrics
- Structured logging (structlog)
- Integration tests
- Audit logging

**Security Features:**
- SQL injection prevention
- Destructive operation blocking
- Table-level access control
- Query approval workflows (optional)

---

### M4: Evaluation & Optimization (In Progress: February 2026)

**Objectives:**
- Systematically evaluate Text-to-SQL accuracy
- Benchmark different LLM providers
- Optimize performance and cost

**Planned Deliverables:**
- [ ] Evaluation dataset (50+ queries)
- [ ] Benchmark runner script
- [ ] Metrics: exact match, execution accuracy, latency
- [ ] LLM provider comparison (OpenAI vs Anthropic vs Local)
- [ ] Performance optimization report
- [ ] Cost analysis (API calls, tokens)

**Evaluation Metrics:**
- **Exact Match (EM)**: Generated SQL == Gold SQL
- **Execution Accuracy (EX)**: Query results match expected results
- **Valid Syntax**: Percentage of syntactically correct SQL
- **Safety Compliance**: Percentage passing safety checks
- **Average Latency**: Time from question to result
- **Token Usage**: Cost per query

**Benchmarking Plan:**
| Provider | Model | Expected Accuracy | Cost/1K Tokens |
|--------------|--------------------------|-------------------|----------------|
| OpenAI | GPT-4 Turbo | 90-95% | $0.01 |
| Anthropic | Claude 3 Sonnet | 88-92% | $0.003 |
| Local (mock) | Deterministic responses | 15-20% | $0.00 |

---

### M5: Deployment & Production Testing (Planned: March 2026)

**Objectives:**
- Deploy to production-like environment
- Perform security audit
- Conduct load and stress testing
- Ensure high availability

**Planned Deliverables:**
- [ ] Kubernetes deployment on test cluster
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Security audit report
- [ ] Load testing results (1000 concurrent users)
- [ ] Backup and recovery procedures
- [ ] Monitoring dashboard (Grafana)

**Testing Plan:**
- **Unit Tests**: >80% code coverage
- **Integration Tests**: All API endpoints
- **Load Tests**: 1000 requests/minute
- **Security Tests**: OWASP Top 10
- **Chaos Engineering**: Database failover, network partitions

---

### M6: Documentation & Presentation (Planned: April - May 2026)

**Objectives:**
- Complete comprehensive documentation
- Prepare academic presentation
- Write research paper (optional publication)

**Planned Deliverables:**
- [ ] Complete technical documentation
- [ ] Research paper draft (IEEE format)
- [ ] Project presentation slides
- [ ] Demo video (5-10 minutes)
- [ ] User manual
- [ ] Developer guide

**Documentation Structure:**
- README (project overview)
- Architecture documentation
- API reference (OpenAPI)
- Deployment guide
- Security policy
- Contributing guidelines

---

## Research Questions

### Primary Research Questions

1. **RQ1**: How accurately can state-of-the-art LLMs translate natural language to SQL for real-world business queries?

2. **RQ2**: What safety mechanisms are necessary to deploy an LLM-based DBMS in production environments?

3. **RQ3**: How do different LLM providers compare in terms of accuracy, latency, and cost for Text-to-SQL tasks?

4. **RQ4**: Can prompt engineering techniques improve Text-to-SQL accuracy without fine-tuning?

### Secondary Research Questions

5. **RQ5**: How effective is AST-based SQL parsing vs. regex-based approaches for safety validation?

6. **RQ6**: What is the impact of caching on reducing LLM API costs in production?

7. **RQ7**: How does RBAC affect the complexity and performance of the system?

---

## Success Criteria

### Technical Success Criteria

 **Functionality**
- System successfully translates 80%+ of test queries to correct SQL
- All safety checks prevent dangerous operations
- RBAC correctly enforces access control
- API achieves 99%+ uptime in test deployment

 **Performance**
- Average query latency < 2 seconds (including LLM call)
- System handles 100+ concurrent users
- Cache hit rate > 30% in typical usage

 **Security**
- Zero SQL injection vulnerabilities
- All destructive operations blocked
- Comprehensive audit logging
- Secure authentication

### Academic Success Criteria

 **Documentation**
- Complete technical documentation
- Reproducible evaluation methodology
- Published codebase (open source)

 **Research Output** (Planned)
- Research paper submission to conference (e.g., SIGMOD, VLDB)
- TÜBİTAK project report
- University thesis/project report

 **Presentation** (Planned)
- Successful defense to university committee
- Demo at university engineering expo
- Potential conference presentation

---

## Risk Management

### Technical Risks

| Risk | Probability | Impact | Mitigation Strategy |
|-------------------------------|-------------|--------|----------------------------------------------|
| LLM API reliability issues | Medium | High | Implement fallback providers, caching |
| SQL generation accuracy low | Low | High | Prompt engineering, few-shot examples |
| Performance bottlenecks | Medium | Medium | Database indexing, connection pooling |
| Security vulnerabilities | Low | Critical | Security audits, penetration testing |

### Academic Risks

| Risk | Probability | Impact | Mitigation Strategy |
|-------------------------------|-------------|--------|----------------------------------------------|
| Timeline delays | Medium | Medium | Agile development, regular check-ins |
| Scope creep | High | Medium | Strict scope management, prioritization |
| Unavailable team members | Low | Low | Documentation, knowledge sharing |

---

## Budget and Resources

### TÜBİTAK 2209-A Funding

**Allocated Budget**: Per TÜBİTAK 2209-A program guidelines

**Budget Allocation:**
- **Cloud Services**: AWS/GCP credits for testing (~$200)
- **LLM API Credits**: OpenAI/Anthropic API usage (~$300)
- **Conference/Publication**: Conference registration fees (~$500)
- **Hardware**: Potential server/GPU costs (if needed)

### Development Resources

**Computational Resources:**
- Local development: Personal laptops (Python 3.11+, 16GB RAM)
- Database: PostgreSQL (free tier or self-hosted)
- Cloud: AWS/GCP free tier credits

**Software & Tools:**
- IDE: VS Code, PyCharm (free/student licenses)
- LLM APIs: OpenAI, Anthropic (paid)
- Monitoring: Prometheus, Grafana (open source)
- CI/CD: GitHub Actions (free for public repos)

---

## Collaboration and Communication

### Weekly Meetings

**Time**: Every Monday, 14:00-15:00 
**Attendees**: All team members + advisor 
**Topics**:
- Progress updates
- Blocker discussions
- Next week planning

### Communication Channels

- **Primary**: University email
- **Development**: GitHub issues, pull requests
- **Quick questions**: WhatsApp/Telegram group
- **Documentation**: Shared Google Drive

### Code Review Process

1. Create feature branch
2. Implement changes with tests
3. Submit pull request
4. Peer review (at least 1 team member)
5. Advisor approval (for major changes)
6. Merge to main

---

## Deliverables Summary

### Technical Deliverables

- [x] Working prototype (MVP)
- [x] Production-ready API
- [x] Docker containerization
- [x] Kubernetes manifests
- [ ] Evaluation framework
- [ ] Benchmark results
- [x] Comprehensive documentation

### Academic Deliverables

- [x] TÜBİTAK project proposal
- [ ] Midterm progress report (February 2026)
- [ ] Final project report (June 2026)
- [ ] University thesis/project document
- [ ] Presentation slides
- [ ] Demo video

### Optional Deliverables

- [ ] Research paper submission
- [ ] Conference presentation
- [ ] Blog post series
- [ ] Tutorial videos

---

## Future Work Beyond 2026

### Potential Extensions

1. **Multi-Language Support**
 - Turkish language query understanding
 - Multilingual prompt templates

2. **Advanced LLM Features**
 - Fine-tuned models for domain-specific SQL
 - Local LLM deployment (Llama, Mistral)
 - Agent-based query refinement

3. **Extended Database Support**
 - MySQL, MariaDB, SQL Server
 - NoSQL databases (MongoDB, Cassandra)
 - Data warehouses (BigQuery, Snowflake)

4. **User Interface**
 - Web-based UI (React/Next.js)
 - Query builder with visual components
 - Result visualization (charts, graphs)

5. **Enterprise Features**
 - Multi-tenancy support
 - SSO integration (OAuth, SAML)
 - Advanced audit trails
 - Data masking for PII

6. **Research Directions**
 - Query optimization using RL
 - Semantic search over schema
 - Conversational query refinement
 - Automatic index recommendation

---

## Conclusion

This project represents a comprehensive effort to bridge natural language understanding and database querying, addressing a real-world need for accessible data analytics. Through rigorous engineering and research, we aim to contribute both a practical system and academic insights to the field of Natural Language Interfaces for Databases.

**Status (as of December 2025)**: Ahead of schedule, core implementation complete. 
**Next Phase**: Evaluation framework development and optimization.

---

**For more information, contact:**

Derya Umut Kulalı (Principal Investigator) 
Eskişehir Technical University 
Department of Electrical and Electronics Engineering 
Email: [university email]

**Project Repository**: https://github.com/Japyh/llm-based-dbms 
**TÜBİTAK Program**: 2209-A University Students Research Projects Support Programme
