# Data Directory

This directory contains data files used by the LLM-Based DBMS system.

## Directory Structure

```
data/
├── processed/          # Processed database files
│   └── sales.db       # SQLite database (created by init_db.py)
├── raw/               # Raw data files (if any)
└── vector_store/      # Vector embeddings (if semantic search enabled)
```

## Database Files

### sales.db
- **Type**: SQLite database
- **Created by**: `scripts/init_db.py`
- **Schema**: Sales orders with customer, product, and transaction data
- **Purpose**: Sample database for development and testing

**To create/reset the database:**
```bash
python scripts/init_db.py
```

## Data Privacy

⚠️ **Important Notes:**

1. **Never commit database files with real data** to version control
2. The `.gitignore` file excludes:
   - `*.db` - Database files
   - `*.sqlite` - SQLite databases
   - `data/processed/*` - Processed data
   - `data/raw/*` - Raw data files

3. **For development**: Use sample/synthetic data only
4. **For production**: Use PostgreSQL, not SQLite files

## Sample Data

The initial database includes sample sales data with:
- **3 sample orders** from different regions
- **Product information**: Vintage Cars, Classic Cars
- **Customer data**: Names, addresses, contact information
- **Order details**: Quantities, prices, dates, statuses

### Sample Tables

#### sales_orders
Columns:
- `ORDERNUMBER` (Primary Key)
- `QUANTITYORDERED`
- `PRICEEACH`
- `SALES`
- `ORDERDATE`
- `STATUS`
- `PRODUCTCODE`, `PRODUCTLINE`
- `CUSTOMERNAME`, `COUNTRY`, `CITY`
- And more...

## Adding Your Own Data

### Option 1: Modify init_db.py

Edit `scripts/init_db.py` to add more sample data:

```python
sample_data = [
    {
        "ORDERNUMBER": 10103,
        "QUANTITYORDERED": 25,
        # ... add more fields
    },
    # Add more records
]
```

### Option 2: Import CSV

Create a script to import CSV files:

```python
import pandas as pd
from backend.database.connection import SessionLocal
from backend.database.models import SalesOrder

df = pd.read_csv('data/raw/your_data.csv')
db = SessionLocal()

for _, row in df.iterrows():
    order = SalesOrder(**row.to_dict())
    db.add(order)

db.commit()
db.close()
```

### Option 3: Use SQL Directly

```bash
sqlite3 data/processed/sales.db
```

```sql
INSERT INTO sales_orders (ORDERNUMBER, QUANTITYORDERED, ...) 
VALUES (10104, 30, ...);
```

## Database Migrations

For schema changes, use Alembic:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Data Security

For production deployments:

1. **Use PostgreSQL** instead of SQLite
2. **Enable database encryption** if handling sensitive data
3. **Set up regular backups**
4. **Implement row-level security** (RLS) if needed
5. **Audit database access** via application logs

## Vector Store Data

If semantic search is enabled (`ENABLE_SEMANTIC_SEARCH=True`):

- Vector embeddings are stored in `data/vector_store/`
- Uses ChromaDB by default
- Contains embeddings of:
  - Table descriptions
  - Column metadata
  - Example queries

**To initialize vector store:**
```bash
python scripts/init_vector_store.py
```

## Data Backup

Recommended backup strategy:

```bash
# SQLite backup
cp data/processed/sales.db data/processed/sales_backup_$(date +%Y%m%d).db

# PostgreSQL backup
pg_dump -U llmdbms llmdbms > backup_$(date +%Y%m%d).sql
```

## Cleanup

To remove all data and start fresh:

```bash
# Remove SQLite database
rm data/processed/sales.db

# Re-initialize
python scripts/init_db.py
```

## Notes

- This directory is automatically created by `scripts/init_db.py`
- Database files are gitignored by default
- Use environment variables to configure database paths
- See `backend/config/settings.py` for configuration options
