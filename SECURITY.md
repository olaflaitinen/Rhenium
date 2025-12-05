# Security Policy

## Reporting a Vulnerability

The LLM-Based DBMS project takes security seriously. If you discover a security vulnerability, please follow these steps:

### How to Report

1. **Do NOT** open a public GitHub issue for security vulnerabilities
2. Contact the project team directly through Eskişehir Technical University's Department of Electrical and Electronics Engineering
3. Provide detailed information about the vulnerability:
 - Type of vulnerability
 - Steps to reproduce
 - Potential impact
 - Suggested fix (if available)

### What to Expect

- **Initial Response**: Within 48 hours
- **Status Updates**: Every 72 hours until resolved
- **Resolution Timeline**: Depends on severity
 - Critical: 7 days
 - High: 14 days
 - Medium: 30 days
 - Low: 60 days

## Supported Versions

| Version | Supported |
| ------- | ------------------ |
| 1.0.x | :white_check_mark: |
| < 1.0 | :x: |

## Security Features

### Current Implementations

#### 1. SQL Injection Prevention
- **AST-based SQL parsing** using `sqlparse`
- **Parameterized queries** where applicable
- **Multiple statement detection** and blocking
- **Whitelist-based validation**

#### 2. Access Control
- **JWT-based authentication** with secure token handling
- **Role-Based Access Control (RBAC)** with 4 permission levels
- **Table-level access restrictions**
- **Session management** with configurable expiration

#### 3. Query Safety
- **Destructive operation prevention** (DROP, DELETE, UPDATE blocked by default)
- **Policy-based validation** (strict/moderate/permissive modes)
- **Audit logging** of all query attempts
- **Dry-run mode** for safe testing

#### 4. API Security
- **Rate limiting** (configurable)
- **CORS configuration** (restrictive in production)
- **Input validation** using Pydantic
- **Error message sanitization** (no sensitive info in responses)

#### 5. Infrastructure Security
- **Environment-based configuration** (no hardcoded secrets)
- **Docker security best practices** (non-root user, minimal image)
- **TLS/SSL support** for production deployments
- **Health check endpoints** (liveness/readiness)

### Security Best Practices

#### For Deployment

1. **Always change default credentials**
 ```bash
 # Default admin password is admin123 - CHANGE THIS!
 python scripts/update_admin_password.py
 ```

2. **Use strong JWT secrets**
 ```bash
 # Generate secure secret
 python -c "import secrets; print(secrets.token_urlsafe(32))"
 ```

3. **Enable HTTPS in production**
 - Use reverse proxy (nginx, Traefik)
 - Configure SSL/TLS certificates
 - Enforce HTTPS redirects

4. **Restrict CORS origins**
 ```python
 # In production, specify exact origins
 allow_origins=["https://yourdomain.com"]
 ```

5. **Use PostgreSQL in production**
 - SQLite is for development only
 - Configure proper PostgreSQL authentication
 - Use connection pooling

6. **Enable Redis authentication**
 ```bash
 # Set Redis password in .env
 REDIS_PASSWORD=your_secure_password
 ```

7. **Set safety mode to strict**
 ```bash
 SAFETY_MODE=strict
 ALLOW_DANGEROUS_QUERIES=False
 ```

#### For Development

1. **Never commit secrets**
 - Use `.env` files (gitignored)
 - Use environment variables
 - Rotate API keys regularly

2. **Keep dependencies updated**
 ```bash
 pip list --outdated
 pip install --upgrade <package>
 ```

3. **Run security scans**
 ```bash
 # Check for known vulnerabilities
 pip install safety
 safety check
 ```

4. **Use mock LLM provider**
 ```bash
 # Avoid exposing real API keys in development
 LLM_PROVIDER=mock
 ```

## Known Security Considerations

### LLM-Specific Risks

1. **Prompt Injection**
 - Users may attempt to manipulate LLM prompts
 - **Mitigation**: Structured prompts, output validation

2. **Data Exposure**
 - LLM responses may include sensitive schema information
 - **Mitigation**: RBAC enforcement, response sanitization

3. **Cost Attacks**
 - Excessive queries can incur high LLM API costs
 - **Mitigation**: Rate limiting, caching, usage quotas

### Database Risks

1. **Schema Inference**
 - Attackers may infer schema through error messages
 - **Mitigation**: Generic error messages, audit logging

2. **Data Exfiltration**
 - Large SELECT queries may expose data
 - **Mitigation**: Result size limits, RBAC

3. **Resource Exhaustion**
 - Complex queries may overwhelm database
 - **Mitigation**: Query timeout, connection pooling

## Security Checklist for Production

- [ ] Change default admin password
- [ ] Generate and set strong JWT secret (32+ characters)
- [ ] Configure allowed CORS origins
- [ ] Enable HTTPS/TLS
- [ ] Use PostgreSQL (not SQLite)
- [ ] Set Redis password
- [ ] Configure rate limiting
- [ ] Set SAFETY_MODE=strict
- [ ] Enable audit logging
- [ ] Set up monitoring and alerts
- [ ] Configure firewall rules
- [ ] Use environment variables for all secrets
- [ ] Enable health check endpoints
- [ ] Set up log rotation
- [ ] Configure backup strategy
- [ ] Test disaster recovery procedures

## Vulnerability Disclosure Policy

We follow responsible disclosure practices:

1. **Report received**: Acknowledge within 48 hours
2. **Initial assessment**: 7 days
3. **Fix development**: Based on severity
4. **Testing**: 3-5 days
5. **Disclosure**: After fix is deployed
6. **Public announcement**: CVE assigned (if applicable)

## Security Updates

Security updates will be announced through:
- GitHub Security Advisories
- Release notes
- Academic communications (for research collaborators)

## Compliance

This project is intended for:
- Academic research
- Educational purposes
- Prototype/proof-of-concept deployments

For production use with sensitive data:
- Conduct security audit
- Implement additional controls
- Ensure regulatory compliance (GDPR, etc.)

## Contact

For security-related questions:
- **Academic**: Contact through Eskişehir Technical University
- **Technical**: security@[project-domain]
- **Emergency**: Create encrypted message via GitHub

## Acknowledgments

We appreciate responsible disclosure and will credit security researchers (with permission) in:
- Security advisories
- Release notes
- Academic publications

Thank you for helping keep the LLM-Based DBMS project secure!
