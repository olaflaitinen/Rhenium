# Deployment Guide

## LLM-Based DBMS - Production Deployment Documentation

**Institution**: Eskişehir Technical University, Department of Electrical and Electronics Engineering 
**Project**: 2025-2026 Design Project | TÜBİTAK 2209-A 
**Team**: Derya Umut Kulalı, Anıl Aydın, Sıla Alhan | **Advisor**: Mehmet Fidan

---

## Table of Contents

1. [Deployment Overview](#deployment-overview)
2. [Prerequisites](#prerequisites)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Cloud Deployments](#cloud-deployments)
6. [Configuration](#configuration)
7. [Security Hardening](#security-hardening)
8. [Monitoring and Observability](#monitoring-and-observability)
9. [Backup and Recovery](#backup-and-recovery)
10. [Troubleshooting](#troubleshooting)

---

## Deployment Overview

### Architecture Components

```
┌─────────────┐
│ Clients │
└──────┬──────┘
 │
┌──────▼──────────┐
│ Load Balancer │ (Nginx/Traefik)
└──────┬──────────┘
 │
┌──────▼──────────┐
│ API Service │ (FastAPI - Multiple replicas)
└──────┬──────────┘
 │
 ┌───┴───┐
 │ │
┌──▼──┐ ┌──▼──┐
│Redis│ │ DB │ (PostgreSQL)
└─────┘ └─────┘
```

### Deployment Options

1. **Docker Compose** - Simple, single-host deployment
2. **Kubernetes** - Scalable, production-grade orchestration
3. **Cloud Platforms** - AWS, GCP, Azure
4. **Bare Metal** - Direct server deployment

---

## Prerequisites

### System Requirements

**Minimum (Development):**
- 2 CPU cores
- 4 GB RAM
- 20 GB disk space
- Network connectivity

**Recommended (Production):**
- 4+ CPU cores
- 8+ GB RAM
- 50+ GB SSD
- Load balancer
- Monitoring stack

### Software Requirements

- **Docker**: 24.0+ and Docker Compose 2.0+
- **Python**: 3.11+ (for bare metal deployments)
- **PostgreSQL**: 15+ (production database)
- **Redis**: 7+ (caching layer)
- **Nginx/Tr aefik**: Latest (reverse proxy)

### Network Requirements

- Ports 8000 (API), 5432 (PostgreSQL), 6379 (Redis)
- HTTPS/TLS certificates
- Domain name (for production)

---

## Docker Deployment

### Using Docker Compose (Recommended)

#### 1. Prepare Environment

```bash
# Clone repository
git clone https://github.com/Japyh/llm-based-dbms.git
cd llm-based-dbms

# Create environment file
cp .env.example .env
```

#### 2. Configure `.env`

```ini
# Core Settings
ENVIRONMENT=production
API_HOST=0.0.0.0
API_PORT=8000

# Database (PostgreSQL for production)
DATABASE_TYPE=postgresql
POSTGRES_USER=llmdbms
POSTGRES_PASSWORD=YOUR_SECURE_PASSWORD_HERE # CHANGE THIS!
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=llmdbms

# JWT Secret (CRITICAL - Use strong secret)
JWT_SECRET_KEY=YOUR_RANDOM_32_CHAR_SECRET_KEY_HERE # Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

# LLM Provider
LLM_PROVIDER=openai # or anthropic
OPENAI_API_KEY=sk-your-actual-key-here
MODEL_NAME=gpt-4-turbo

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=YOUR_REDIS_PASSWORD # Set a password!
ENABLE_LLM_CACHE=True

# Safety
SAFETY_MODE=strict
ALLOW_DANGEROUS_QUERIES=False

# Logging
LOG_LEVEL=INFO
ENABLE_METRICS=True
```

#### 3. Start Services

```bash
# Build and start all services
docker-compose up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f api
```

#### 4. Initialize Database

```bash
# Run initialization script
docker-compose exec api python scripts/init_db.py
```

#### 5. Verify Deployment

```bash
# Health check
curl http://localhost:8000/health/liveness

# API documentation
open http://localhost:8000/docs
```

### Custom Docker Compose Configuration

**docker-compose.prod.yml:**

```yaml
version: '3.8'

services:
 postgres:
 image: postgres:16-alpine
 container_name: llmdbms-postgres
 environment:
 POSTGRES_USER: ${POSTGRES_USER}
 POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
 POSTGRES_DB: ${POSTGRES_DB}
 volumes:
 - postgres_data:/var/lib/postgresql/data
 - ./backups:/backups
 healthcheck:
 test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
 interval: 10s
 timeout: 5s
 retries: 5
 deploy:
 resources:
 limits:
 cpus: '2'
 memory: 2G
 restart: unless-stopped
 networks:
 - backend

 redis:
 image: redis:7-alpine
 container_name: llmdbms-redis
 command: redis-server --requirepass ${REDIS_PASSWORD}
 volumes:
 - redis_data:/data
 healthcheck:
 test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
 interval: 10s
 timeout: 3s
 retries: 5
 deploy:
 resources:
 limits:
 cpus: '1'
 memory: 512M
 restart: unless-stopped
 networks:
 - backend

 api:
 build: .
 container_name: llmdbms-api
 env_file: .env
 depends_on:
 postgres:
 condition: service_healthy
 redis:
 condition: service_healthy
 healthcheck:
 test: ["CMD", "curl", "-f", "http://localhost:8000/health/liveness"]
 interval: 30s
 timeout: 10s
 retries: 3
 start_period: 40s
 deploy:
 replicas: 2
 resources:
 limits:
 cpus: '2'
 memory: 2G
 reservations:
 cpus: '1'
 memory: 1G
 restart: unless-stopped
 networks:
 - backend
 - frontend

 nginx:
 image: nginx:alpine
 container_name: llmdbms-nginx
 ports:
 - "80:80"
 - "443:443"
 volumes:
 - ./nginx.conf:/etc/nginx/nginx.conf:ro
 - ./ssl:/etc/nginx/ssl:ro
 depends_on:
 - api
 restart: unless-stopped
 networks:
 - frontend

volumes:
 postgres_data:
 redis_data:

networks:
 backend:
 driver: bridge
 frontend:
 driver: bridge
```

**nginx.conf:**

```nginx
upstream api_backend {
 least_conn;
 server api:8000 max_fails=3 fail_timeout=30s;
}

server {
 listen 80;
 server_name yourdomain.com;
 return 301 https://$server_name$request_uri;
}

server {
 listen 443 ssl http2;
 server_name yourdomain.com;

 ssl_certificate /etc/nginx/ssl/cert.pem;
 ssl_certificate_key /etc/nginx/ssl/key.pem;
 ssl_protocols TLSv1.2 TLSv1.3;
 ssl_ciphers HIGH:!aNULL:!MD5;

 client_max_body_size 10M;

 location / {
 proxy_pass http://api_backend;
 proxy_set_header Host $host;
 proxy_set_header X-Real-IP $remote_addr;
 proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
 proxy_set_header X-Forwarded-Proto $scheme;
 
 proxy_connect_timeout 60s;
 proxy_send_timeout 60s;
 proxy_read_timeout 60s;
 }

 location /metrics {
 deny all;
 return 403;
 }
}
```

---

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (1.25+)
- kubectl configured
- Helm (optional)

### 1. Create Namespace

```bash
kubectl create namespace llmdbms
```

### 2. Create Secrets

```bash
# Database credentials
kubectl create secret generic llmdbms-db-secret \
 --from-literal=postgres-user=llmdbms \
 --from-literal=postgres-password=YOUR_SECURE_PASSWORD \
 --from-literal=postgres-db=llmdbms \
 -n llmdbms

# JWT secret
kubectl create secret generic llmdbms-jwt-secret \
 --from-literal=jwt-secret-key=$(python -c "import secrets; print(secrets.token_urlsafe(32))") \
 -n llmdbms

# LLM API keys
kubectl create secret generic llmdbms-llm-secret \
 --from-literal=openai-api-key=sk-your-key \
 -n llmdbms

# Redis password
kubectl create secret generic llmdbms-redis-secret \
 --from-literal=redis-password=YOUR_REDIS_PASSWORD \
 -n llmdbms
```

### 3. Apply ConfigMap

```bash
kubectl apply -f k8s/configmap.yaml -n llmdbms
```

**k8s/configmap.yaml:**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
 name: llmdbms-config
 namespace: llmdbms
data:
 ENVIRONMENT: "production"
 API_HOST: "0.0.0.0"
 API_PORT: "8000"
 DATABASE_TYPE: "postgresql"
 POSTGRES_HOST: "postgres-service"
 POSTGRES_PORT: "5432"
 REDIS_HOST: "redis-service"
 REDIS_PORT: "6379"
 LLM_PROVIDER: "openai"
 MODEL_NAME: "gpt-4-turbo"
 SAFETY_MODE: "strict"
 LOG_LEVEL: "INFO"
```

### 4. Deploy PostgreSQL

```yaml
# k8s/postgres-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
 name: postgres
 namespace: llmdbms
spec:
 replicas: 1
 selector:
 matchLabels:
 app: postgres
 template:
 metadata:
 labels:
 app: postgres
 spec:
 containers:
 - name: postgres
 image: postgres:16-alpine
 envFrom:
 - secretRef:
 name: llmdbms-db-secret
 ports:
 - containerPort: 5432
 volumeMounts:
 - name: postgres-storage
 mountPath: /var/lib/postgresql/data
 resources:
 requests:
 memory: "1Gi"
 cpu: "500m"
 limits:
 memory: "2Gi"
 cpu: "1000m"
 volumes:
 - name: postgres-storage
 persistentVolumeClaim:
 claimName: postgres-pvc
---
apiVersion: v1
kind: Service
metadata:
 name: postgres-service
 namespace: llmdbms
spec:
 selector:
 app: postgres
 ports:
 - port: 5432
 targetPort: 5432
```

### 5. Deploy API

```bash
kubectl apply -f k8s/deployment.yaml -n llmdbms
kubectl apply -f k8s/service.yaml -n llmdbms
```

### 6. Create Ingress

```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
 name: llmdbms-ingress
 namespace: llmdbms
 annotations:
 cert-manager.io/cluster-issuer: letsencrypt-prod
 nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
 ingressClassName: nginx
 tls:
 - hosts:
 - api.yourdomain.com
 secretName: llmdbms-tls
 rules:
 - host: api.yourdomain.com
 http:
 paths:
 - path: /
 pathType: Prefix
 backend:
 service:
 name: llmdbms-api-service
 port:
 number: 8000
```

### 7. Apply Ingress

```bash
kubectl apply -f k8s/ingress.yaml -n llmdbms
```

### 8. Verify Deployment

```bash
# Check pods
kubectl get pods -n llmdbms

# Check services
kubectl get svc -n llmdbms

# View logs
kubectl logs -f deployment/llmdbms-api -n llmdbms

# Port forward for testing
kubectl port-forward svc/llmdbms-api-service 8000:8000 -n llmdbms
```

---

## Cloud Deployments

### AWS (ECS/Fargate)

#### Using AWS Copilot

```bash
# Install Copilot
brew install aws/tap/copilot-cli

# Initialize application
copilot app init llmdbms

# Create service
copilot svc init \
 --name api \
 --svc-type "Load Balanced Web Service" \
 --dockerfile ./Dockerfile

# Deploy
copilot svc deploy --name api --env production
```

### Google Cloud Platform (Cloud Run)

```bash
# Build and push image
gcloud builds submit --tag gcr.io/PROJECT_ID/llmdbms

# Deploy
gcloud run deploy llmdbms \
 --image gcr.io/PROJECT_ID/llmdbms \
 --platform managed \
 --region us-central1 \
 --allow-unauthenticated \
 --set-env-vars="ENVIRONMENT=production" \
 --set-secrets="JWT_SECRET_KEY=jwt-secret:latest"
```

### Azure (Container Instances)

```bash
# Create resource group
az group create --name llmdbms-rg --location eastus

# Create container
az container create \
 --resource-group llmdbms-rg \
 --name llmdbms \
 --image your-registry/llmdbms:latest \
 --dns-name-label llmdbms-api \
 --ports 8000 \
 --environment-variables \
 ENVIRONMENT=production \
 --secure-environment-variables \
 JWT_SECRET_KEY=$JWT_SECRET
```

---

## Security Hardening

### 1. Change Default Credentials

```bash
# Generate strong JWT secret
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Update admin password
docker-compose exec api python -c "
from backend.database.connection import SessionLocal
from backend.auth.models import User
from backend.auth.service import AuthService

db = SessionLocal()
admin = db.query(User).filter(User.username == 'admin').first()
admin.hashed_password = AuthService.hash_password('NEW_STRONG_PASSWORD')
db.commit()
"
```

### 2. Enable HTTPS

```bash
# Using Let's Encrypt with Certbot
certbot certonly --standalone -d yourdomain.com
```

### 3. Firewall Rules

```bash
# Allow only necessary ports
ufw allow 22/tcp # SSH
ufw allow 80/tcp # HTTP
ufw allow 443/tcp # HTTPS
ufw enable
```

### 4. Regular Updates

```bash
# Update Docker images
docker-compose pull
docker-compose up -d

# Update dependencies
pip install --upgrade -r requirements.txt
```

---

## Monitoring and Observability

### Prometheus Metrics

Access metrics at: `http://localhost:9090/metrics`

**Key Metrics:**
- `http_requests_total`
- `http_request_duration_seconds`
- `llm_requests_total`
- `sql_queries_total`

### Grafana Dashboard

```yaml
# docker-compose.monitoring.yml
services:
 prometheus:
 image: prom/prometheus
 volumes:
 - ./prometheus.yml:/etc/prometheus/prometheus.yml
 ports:
 - "9090:9090"

 grafana:
 image: grafana/grafana
 ports:
 - "3000:3000"
 environment:
 - GF_SECURITY_ADMIN_PASSWORD=admin
```

### Log Aggregation

**Using ELK Stack:**
```yaml
 elasticsearch:
 image: elasticsearch:8.11.0
 
 logstash:
 image: logstash:8.11.0
 
 kibana:
 image: kibana:8.11.0
```

---

## Backup and Recovery

### Database Backup

**Automated backup script:**

```bash
#!/bin/bash
# backup.sh

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# PostgreSQL backup
docker-compose exec -T postgres pg_dump \
 -U llmdbms llmdbms > $BACKUP_DIR/db_$TIMESTAMP.sql

# Compress
gzip $BACKUP_DIR/db_$TIMESTAMP.sql

# Keep last 7 days
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +7 -delete
```

**Cron job:**
```bash
0 2 * * * /path/to/backup.sh
```

### Restore

```bash
# Restore from backup
gunzip -c /backups/db_20250101_020000.sql.gz | \
 docker-compose exec -T postgres psql -U llmdbms -d llmdbms
```

---

## Troubleshooting

### Common Issues

**API not responding:**
```bash
# Check logs
docker-compose logs api

# Restart service
docker-compose restart api
```

**Database connection errors:**
```bash
# Check PostgreSQL
docker-compose exec postgres psql -U llmdbms -c "\l"

# Verify credentials in .env
```

**High memory usage:**
```bash
# Check resource usage
docker stats

# Increase limits in docker-compose.yml
```

---

## Production Checklist

- [ ] Change default admin password
- [ ] Generate strong JWT secret (32+ chars)
- [ ] Configure CORS for specific origins only
- [ ] Enable HTTPS/TLS
- [ ] Use PostgreSQL (not SQLite)
- [ ] Set Redis password
- [ ] Configure rate limiting
- [ ] Set SAFETY_MODE=strict
- [ ] Enable audit logging
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Configure firewall
- [ ] Use environment variables for secrets
- [ ] Enable health checks
- [ ] Configure log rotation
- [ ] Set up automated backups
- [ ] Test disaster recovery
- [ ] Document runbooks
- [ ] Set up alerting

---

**For production support, contact**: 
Eskişehir Technical University 
Department of Electrical and Electronics Engineering

**Team**: Derya Umut Kulalı, Anıl Aydın, Sıla Alhan 
**Advisor**: Mehmet Fidan
