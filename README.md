# LLM-Based Database Management System

**A Research-Grade Natural Language Interface for Relational Databases**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/olaflaitinen/Rhenium/actions)
[![TÜBİTAK 2209-A](https://img.shields.io/badge/Supported%20by-T%C3%9CB%C4%B0TAK%202209--A-red.svg)](https://www.tubitak.gov.tr/)

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Academic Context & Background](#academic-context--background)
3. [Key Features](#key-features)
4. [System Architecture](#system-architecture)
5. [Repository Structure](#repository-structure)
6. [Getting Started](#getting-started)
7. [Configuration](#configuration)
8. [Database Setup](#database-setup)
9. [Running the API](#running-the-api)
10. [Usage Examples](#usage-examples)
11. [Evaluation & Experiments](#evaluation--experiments)
12. [Team & Supervision](#team--supervision)
13. [Funding & Acknowledgements](#funding--acknowledgements)
14. [Citation](#citation)
15. [License](#license)

---

## Project Overview

The **LLM-Based Database Management System (DBMS)** is a comprehensive software platform designed to bridge the gap between non-technical users and complex relational databases. By leveraging state-of-the-art **Large Language Models (LLMs)**, the system allows users to query data using natural language (e.g., *"What is the total revenue per product category for the last quarter?"*) instead of writing complex SQL queries.

Unlike simple Text-to-SQL prototypes, this project is engineered as a **robust, modular, and safe** system suitable for both academic research and potential enterprise deployment. It features a sophisticated orchestration layer that handles schema injection, prompt engineering, rule-based SQL validation, and role-based access control (RBAC), ensuring that the generated queries are not only syntactically correct but also secure and policy-compliant.

### Problem Motivation
As data volumes grow, the ability to extract insights quickly becomes a competitive advantage. However, the requirement to master SQL (Structured Query Language) creates a bottleneck for domain experts, managers, and researchers. This project aims to democratize data access by providing a reliable, explainable, and secure natural language interface to relational data.

---

## Academic Context & Background

This project is conducted within the **Department of Electrical and Electronics Engineering** at **Eskisehir Technical University**. It is developed as part of the **2025–2026 Electrical and Electronics Engineering Design Project** curriculum, representing a rigorous engineering effort spanning two semesters (8 months).

The initiative is formally supported and recognized under the **TÜBİTAK 2209-A University Students Research Projects Support Program** (2025 Fall Application Period).

- **Turkish Project Title**: *LLM Tabanlı Doğal Dil Arayüzlü Veritabanı Yönetim Sistemi (DBMS)*
- **English Project Title**: *LLM Based Database Management System*

The project serves a dual purpose:
1. **Academic Research**: To investigate the efficacy of different LLM architectures and prompting strategies for Text-to-SQL tasks, specifically within the context of Turkish and English query understanding.
2. **Engineering Design**: To implement a scalable, secure, and user-friendly software architecture that integrates modern AI capabilities with traditional database systems.

---

## Key Features

- **Natural Language to SQL**: Converts complex user questions into executable SQL queries using advanced LLMs (OpenAI GPT-4, Anthropic Claude, or local models).
- **Enterprise-Grade Security**:
  - **Role-Based Access Control (RBAC)**: Granular permissions (Admin, Data Scientist, Analyst, Viewer) enforcing table and column-level access.
  - **SQL Safety Engine**: AST-based parsing and validation to prevent SQL injection and destructive operations (DROP, DELETE).
- **Multi-LLM Support**: Abstracted client layer allowing seamless switching between different LLM providers for benchmarking and cost optimization.
- **Explainability**: Optional natural language explanations of the generated SQL to build user trust.
- **Production Infrastructure**:
  - **FastAPI Backend**: High-performance, asynchronous REST API.
  - **Structured Logging**: Comprehensive JSON logging for observability.
  - **Dockerized Deployment**: Full containerization with Docker Compose (API + PostgreSQL + Redis).
- **Research Evaluation Framework**: Built-in scripts to evaluate Text-to-SQL performance using exact matching and result set equivalence metrics.

---

## System Architecture

The system follows a layered microservices-ready architecture:

```text
User Request (Natural Language)
       │
       ▼
┌───────────────────┐
│   API Gateway     │  (FastAPI, Auth, Rate Limiting)
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Orchestrator     │  (LangChain, Prompt Management)
└────────┬──────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌───────┐
│  LLM  │ │Vector │  (Optional Semantic Search)
│Service│ │ Store │
└───┬───┘ └───┬───┘
    │         │
    ▼         ▼
┌───────────────────┐
│ Generated SQL     │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Safety Engine    │  (sqlparse, Policy Validation)
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Query Executor   │  (SQLAlchemy, PostgreSQL/SQLite)
└───────────────────┘
```

---

## Repository Structure

```text
llm-based-dbms/
├── backend/
│   ├── api/              # REST API endpoints (Routers, Schemas, Middleware)
│   ├── auth/             # Authentication, JWT, and RBAC services
│   ├── database/         # Database models, connection pooling, and executors
│   ├── llm/              # LLM client implementations and prompt templates
│   ├── safety/           # SQL validation and policy enforcement engine
│   ├── observability/    # Structured logging and metrics configuration
│   └── config/           # Environment-based configuration management
├── scripts/              # Utility scripts (Database init, Server startup)
├── experiments/          # Evaluation datasets and benchmarking scripts
├── docs/                 # Detailed architectural and research documentation
├── tests/                # Unit and integration tests
├── docker-compose.yml    # Production deployment configuration
├── Dockerfile            # Multi-stage Docker build definition
└── requirements.txt      # Python dependencies
```

---

## Getting Started

### Prerequisites
- **Python 3.11+**
- **Git**
- **Docker & Docker Compose** (Optional, for containerized run)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/olaflaitinen/Rhenium.git
   cd Rhenium
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements-minimal.txt
   pip install email-validator
   ```

---

## Configuration

The system uses environment variables for configuration. Copy the example file to create your local configuration:

```bash
cp .env.example .env
```

**Key Settings (`.env`):**

```ini
# Core
ENVIRONMENT=development
DATABASE_TYPE=sqlite  # or postgresql

# Authentication (CHANGE IN PRODUCTION)
JWT_SECRET_KEY=your-secure-secret-key-min-32-chars

# LLM Provider
LLM_PROVIDER=openai   # options: openai, anthropic, mock
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4-turbo

# Safety
SAFETY_MODE=strict
```

---

## Database Setup

The project includes a sample **Sales & Orders** database (based on the classic sample dataset) to facilitate immediate testing and research.

**Initialize the database:**
```bash
python scripts/init_db.py
```
*This script creates the schema, initializes default roles (ADMIN, DATA_SCIENTIST, ANALYST, VIEWER), creates a default admin user, and populates sample data.*

---

## Running the API

Start the development server using the provided script:

```bash
python scripts/run_dev_server.py
```

The API will be available at: `http://localhost:8000`  
Interactive API Documentation (Swagger UI): `http://localhost:8000/docs`

---

## Usage Examples

### 1. Authentication
First, obtain an access token using the default admin credentials (`admin` / `admin123`):

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin123"
```

### 2. Natural Language Query
Send a natural language question to the API:

```bash
curl -X POST "http://localhost:8000/api/v1/query/" \
     -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{
           "question": "What are the top 3 products by sales revenue in 2003?",
           "explain": true
         }'
```

**Response:**
```json
{
  "sql": "SELECT PRODUCTCODE, SUM(SALES) as total_sales FROM sales_orders WHERE YEAR_ID = 2003 GROUP BY PRODUCTCODE ORDER BY total_sales DESC LIMIT 3;",
  "result": [
    {"PRODUCTCODE": "S18_3232", "total_sales": 150200.50},
    {"PRODUCTCODE": "S10_1949", "total_sales": 145000.00},
    {"PRODUCTCODE": "S12_1108", "total_sales": 138500.25}
  ],
  "explanation": "This query calculates the total sales for each product in the year 2003, sorts them in descending order, and returns the top 3."
}
```

---

## Evaluation & Experiments

The repository includes a dedicated `experiments/` directory for academic evaluation. This framework allows for the systematic benchmarking of different LLMs against a ground-truth dataset of Question-SQL pairs.

**Running the evaluation:**
```bash
python -m experiments.evaluate_text_to_sql --config experiments/configs/benchmark_v1.yaml
```

**Metrics:**
- **Exact Match Accuracy**: Percentage of generated SQL queries that identically match the reference SQL.
- **Execution Accuracy**: Percentage of queries that return the correct result set (handling valid SQL variations).
- **Latency**: Average time taken for generation and execution.

---

## Team & Supervision

This project is executed by a multidisciplinary team of engineering students at Eskisehir Technical University, combining expertise in software development, embedded systems, and signal processing to address the complex challenges of AI-database integration.

### Student Team Members

- **Derya Umut Kulalı**  
  *Principal Investigator / Project Lead*  
  Department of Electrical and Electronics Engineering

- **Anıl Aydın**  
  *Research Team Member*  
  Department of Electrical and Electronics Engineering

- **Sıla Alhan**  
  *Research Team Member*  
  Department of Electrical and Electronics Engineering

### Academic Supervision

- **Mehmet Fidan**  
  *Academic Advisor*  
  Department of Electrical and Electronics Engineering

The team structure is intentionally designed to cover the full spectrum of the system's requirements, from high-level software architecture and API design to efficient data processing and system optimization.

---

## Funding & Acknowledgements

We gratefully acknowledge the support of the **TÜBİTAK (Scientific and Technological Research Council of Türkiye)** under the **2209-A University Students Research Projects Support Program**. This support validates the scientific merit and technical potential of the "LLM Based Database Management System" project.

We also thank **Eskisehir Technical University** and the **Department of Electrical and Electronics Engineering** for providing the academic environment, laboratory infrastructure, and curriculum framework (Design Project 2025-2026) that made this work possible.

---

## Citation

If you use this project or its methodology in your research, please cite it as follows:

```bibtex
@misc{kulali2025llmdbms,
  author = {Kulalı, Derya Umut and Aydın, Anıl and Alhan, Sıla and Fidan, Mehmet},
  title = {LLM Based Database Management System: A Natural Language Interface for Relational Databases},
  year = {2025},
  publisher = {GitHub},
  journal = {TÜBİTAK 2209-A Research Project},
  howpublished = {\url{https://github.com/olaflaitinen/Rhenium}}
}
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
