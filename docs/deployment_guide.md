# Deployment Guide

## Docker Compose (Recommended for simple deployments)

1. Ensure Docker and Docker Compose are installed.
2. Configure `.env` file.
3. Run:
   ```bash
   docker-compose up -d --build
   ```

## Kubernetes

1. Apply ConfigMap and Secrets:
   ```bash
   kubectl apply -f k8s/configmap.yaml
   # Create secret manually or via manifest
   kubectl create secret generic llm-dbms-secrets --from-literal=OPENAI_API_KEY=...
   ```
2. Apply Deployment and Service:
   ```bash
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   ```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Connection string | sqlite:///./sql_app.db |
| `LLM_PROVIDER` | openai, anthropic, mock | openai |
| `OPENAI_API_KEY` | API Key | - |
