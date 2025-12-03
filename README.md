# LLM-based DBMS with Natural Language Interface

## Overview
This project implements a **next-generation Database Management System (DBMS)** that allows users to query and manage data using **natural language**. It bridges the gap between non-technical users and structured data by leveraging Large Language Models (LLMs) to translate natural language into SQL queries.

## Architecture
The system follows a modular, layered architecture:
1.  **API Layer (FastAPI)**: Handles HTTP requests, validation, and response formatting.
2.  **LLM Orchestration (LangChain)**: Manages interactions with LLMs (e.g., OpenAI, Local Models) to generate SQL.
3.  **Safety Layer**: Validates generated SQL to prevent dangerous operations and ensure compliance with safety rules.
4.  **Database Layer (SQLite)**: Executes validated queries against the relational database.
5.  **Evaluation**: Tools to measure the accuracy and performance of the Text-to-SQL pipeline.

## Setup Instructions

### Prerequisites
- Python 3.11+

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/olaflaitinen/llm-based-dbms.git
    cd llm-based-dbms
    ```

2.  **Create a virtual environment**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -e .[dev]
    ```

4.  **Configuration**
    Copy `.env.example` to `.env` and adjust settings:
    ```bash
    cp .env.example .env
    ```
    *Note: By default, `LLM_PROVIDER` is set to `mock` so you can run the system without an API key.*

5.  **Initialize the Database**
    Populate the SQLite database with sample data:
    ```bash
    python scripts/init_db.py
    ```

### Running the Application

Start the development server:
```bash
python scripts/run_dev_server.py
# OR directly
uvicorn backend.api.main:app --reload
```

Access the API documentation at `http://localhost:8000/docs`.

### Running Evaluation

Run the evaluation pipeline:
```bash
python -m experiments.evaluate_text_to_sql
```

## Current Limitations
- **Mock LLM**: The default configuration uses a deterministic mock response for testing purposes. Set `LLM_PROVIDER=openai` and provide an API key to use a real model.
- **SQLite Only**: Currently supports SQLite. Future versions will support PostgreSQL.
- **Basic Safety**: Rule-based validation is minimal.

## License
[License Name]
