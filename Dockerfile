FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml .
COPY .env.example .env

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Copy application code
COPY backend ./backend
COPY scripts ./scripts
COPY data ./data
COPY experiments ./experiments
COPY docs ./docs

# Initialize database
RUN python scripts/init_db.py

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "scripts/run_dev_server.py"]
