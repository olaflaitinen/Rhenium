# Scripts Directory

Utility scripts for database initialization, development server, and maintenance tasks.

## Available Scripts

### 1. init_db.py

**Purpose**: Initialize the database with schema, default users, and sample data.

**Usage**:
```bash
python scripts/init_db.py
```

**What it does**:
1. Creates all database tables (users, roles, sales_orders, audit_logs)
2. Initializes default roles (ADMIN, DATA_SCIENTIST, ANALYST, VIEWER)
3. Creates default admin user:
   - Username: `admin`
   - Password: `admin123` ⚠️ **CHANGE IN PRODUCTION!**
4. Populates sample sales data (3 sample orders)

**Configuration**:
- Uses settings from `.env` or environment variables
- Database location: `data/processed/sales.db` (SQLite) or PostgreSQL connection

**Output**:
```
==========================================================
LLM-based DBMS - Database Initialization
==========================================================

Environment: development
Database Type: sqlite
Database URL: sqlite:///./data/processed/sales.db

Initializing database schema...
✓ Database schema created.

Initializing default roles...
✓ Default roles created (ADMIN, DATA_SCIENTIST, ANALYST, VIEWER).

Creating default admin user...
✓ Created admin user:
  Username: admin
  Password: admin123
  ⚠️  PLEASE CHANGE THIS PASSWORD IN PRODUCTION!

Inserting sample sales data...
✓ Inserted 3 sample sales records.

==========================================================
✓ Database initialization complete!
==========================================================
```

---

### 2. run_dev_server.py

**Purpose**: Start the development server with auto-reload.

**Usage**:
```bash
python scripts/run_dev_server.py
```

**Features**:
- Auto-reload on code changes
- Debug mode enabled
- Runs on configured host and port (default: `0.0.0.0:8000`)
- Access API docs at `http://localhost:8000/docs`

**Configuration**:
```bash
# .env file
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

---

## Creating Additional Scripts

### Example: Update Admin Password

Create `scripts/update_admin_password.py`:

```python
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from backend.database.connection import SessionLocal
from backend.auth.models import User
from backend.auth.service import AuthService

def update_password():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            print("Admin user not found!")
            return
        
        new_password = input("Enter new password: ")
        confirm = input("Confirm password: ")
        
        if new_password != confirm:
            print("Passwords don't match!")
            return
        
        # Hash and update password
        admin.hashed_password = AuthService.hash_password(new_password)
        db.commit()
        
        print("✓ Admin password updated successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    update_password()
```

### Example: Export Data to CSV

Create `scripts/export_data.py`:

```python
import pandas as pd
from backend.database.connection import SessionLocal
from backend.database.models import SalesOrder

def export_to_csv():
    db = SessionLocal()
    try:
        orders = db.query(SalesOrder).all()
        
        # Convert to DataFrame
        data = [
            {
                'order_number': o.ORDERNUMBER,
                'customer': o.CUSTOMERNAME,
                'sales': o.SALES,
                'date': o.ORDERDATE
            }
            for o in orders
        ]
        
        df = pd.DataFrame(data)
        df.to_csv('data/exports/sales_export.csv', index=False)
        
        print(f"✓ Exported {len(orders)} orders to CSV")
    finally:
        db.close()

if __name__ == "__main__":
    export_to_csv()
```

### Example: Database Backup

Create `scripts/backup_db.sh`:

```bash
#!/bin/bash

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups"

mkdir -p $BACKUP_DIR

# SQLite backup
if [ -f "data/processed/sales.db" ]; then
    cp data/processed/sales.db $BACKUP_DIR/sales_${TIMESTAMP}.db
    echo "✓ SQLite backup created: $BACKUP_DIR/sales_${TIMESTAMP}.db"
fi

# PostgreSQL backup (if configured)
if [ "$DATABASE_TYPE" = "postgresql" ]; then
    pg_dump -U $POSTGRES_USER -h $POSTGRES_HOST $POSTGRES_DB > $BACKUP_DIR/postgres_${TIMESTAMP}.sql
    echo "✓ PostgreSQL backup created: $BACKUP_DIR/postgres_${TIMESTAMP}.sql"
fi
```

## Script Guidelines

When creating new scripts:

1. **Add shebang** for shell scripts:
   ```bash
   #!/bin/bash
   ```
   or for Python:
   ```python
   #!/usr/bin/env python3
   ```

2. **Add project root to path**:
   ```python
   import sys
   from pathlib import Path
   project_root = Path(__file__).resolve().parent.parent
   sys.path.append(str(project_root))
   ```

3. **Use proper imports**:
   ```python
   from backend.database.connection import SessionLocal
   from backend.config.settings import settings
   ```

4. **Add docstrings**:
   ```python
   """
   Script description.
   
   Usage:
       python scripts/script_name.py [args]
   """
   ```

5. **Handle errors gracefully**:
   ```python
   try:
       # Main logic
   except Exception as e:
       print(f"Error: {e}")
       sys.exit(1)
   ```

6. **Close database connections**:
   ```python
   db = SessionLocal()
   try:
       # Database operations
   finally:
       db.close()
   ```

## Running Scripts

### From Project Root

```bash
# Python scripts
python scripts/script_name.py

# Shell scripts (make executable first)
chmod +x scripts/script_name.sh
./scripts/script_name.sh
```

### With Docker

```bash
# Run script in container
docker-compose exec api python scripts/script_name.py
```

### With Environment Variables

```bash
# Override config
DATABASE_TYPE=postgresql python scripts/init_db.py
```

## Troubleshooting

### Import Errors

If you get `ModuleNotFoundError`:
```python
# Add this at the top of your script
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

### Database Connection Errors

Check your `.env` file:
```bash
# Verify database configuration
cat .env | grep DATABASE
```

### Permission Errors

Make scripts executable:
```bash
chmod +x scripts/*.sh
```

## Best Practices

1. ✅ Always use `SessionLocal()` for database operations
2. ✅ Close database connections in `finally` blocks
3. ✅ Add helpful output messages
4. ✅ Include error handling
5. ✅ Document usage in docstrings
6. ✅ Test scripts before committing
7. ✅ Use environment variables for configuration
8. ✅ Add scripts to `.gitignore` if they contain sensitive data

## Security Notes

- Never hardcode secrets in scripts
- Use environment variables or `.env` files
- Don't commit database files or backups
- Change default passwords immediately
- Review scripts before running in production
