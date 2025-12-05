"""
Production-grade database initialization script.

Initializes:
- Database schema (all tables)
- Default roles
- Default admin user
- Sample sales data
"""
import sys
from pathlib import Path
from datetime import date, datetime

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from sqlalchemy import insert
from backend.database.connection import init_db, SessionLocal
from backend.database.models import SalesOrder
from backend.auth.models import User
from backend.auth.service import AuthService
from backend.auth.rbac import RBACService
from backend.config.settings import settings


def create_sample_sales_data(db):
    """Create sample sales data."""
    print("Inserting sample sales data...")
    
    sample_data = [
        {
            "ORDERNUMBER": 10100,
            "QUANTITYORDERED": 30,
            "PRICEEACH": 100.0,
            "ORDERLINENUMBER": 1,
            "SALES": 3000.0,
            "ORDERDATE": date(2003, 1, 6),
            "STATUS": "Shipped",
            "QTR_ID": 1,
            "MONTH_ID": 1,
            "YEAR_ID": 2003,
            "PRODUCTLINE": "Vintage Cars",
            "MSRP": 95,
            "PRODUCTCODE": "S18_1749",
            "CUSTOMERNAME": "Online Diecast Creations Co.",
            "PHONE": "2125557818",
            "ADDRESSLINE1": "897 Long Airport Avenue",
            "CITY": "Nashua",
            "STATE": "NH",
            "POSTALCODE": "62005",
            "COUNTRY": "USA",
            "TERRITORY": "NA",
            "CONTACTLASTNAME": "Young",
            "CONTACTFIRSTNAME": "Valarie",
            "DEALSIZE": "Medium"
        },
        {
            "ORDERNUMBER": 10101,
            "QUANTITYORDERED": 45,
            "PRICEEACH": 80.0,
            "ORDERLINENUMBER": 2,
            "SALES": 3600.0,
            "ORDERDATE": date(2003, 1, 9),
            "STATUS": "Shipped",
            "QTR_ID": 1,
            "MONTH_ID": 1,
            "YEAR_ID": 2003,
            "PRODUCTLINE": "Classic Cars",
            "MSRP": 80,
            "PRODUCTCODE": "S24_2022",
            "CUSTOMERNAME": "Blauer See Auto, Co.",
            "PHONE": "+49 69 66 90 2555",
            "ADDRESSLINE1": "Lyonerstr. 34",
            "CITY": "Frankfurt",
            "STATE": None,
            "POSTALCODE": "60528",
            "COUNTRY": "Germany",
            "TERRITORY": "EMEA",
            "CONTACTLASTNAME": "Keitel",
            "CONTACTFIRSTNAME": "Roland",
            "DEALSIZE": "Medium"
        },
        {
            "ORDERNUMBER": 10102,
            "QUANTITYORDERED": 20,
            "PRICEEACH": 150.0,
            "ORDERLINENUMBER": 3,
            "SALES": 3000.0,
            "ORDERDATE": date(2003, 1, 10),
            "STATUS": "Shipped",
            "QTR_ID": 1,
            "MONTH_ID": 1,
            "YEAR_ID": 2003,
            "PRODUCTLINE": "Vintage Cars",
            "MSRP": 140,
            "PRODUCTCODE": "S18_2248",
            "CUSTOMERNAME": "Vitachrome Inc.",
            "PHONE": "2125551500",
            "ADDRESSLINE1": "2678 Kingston Rd.",
            "CITY": "NYC",
            "STATE": "NY",
            "POSTALCODE": "10022",
            "COUNTRY": "USA",
            "TERRITORY": "NA",
            "CONTACTLASTNAME": "Frick",
            "CONTACTFIRSTNAME": "Michael",
            "DEALSIZE": "Medium"
        }
    ]
    
    # Check if data exists
    existing = db.query(SalesOrder).first()
    if existing:
        print("Sample data already exists. Skipping insertion.")
        return
    
    # Insert data
    for data in sample_data:
        order = SalesOrder(**data)
        db.add(order)
    
    db.commit()
    print(f"Inserted {len(sample_data)} sample sales records.")


def create_default_admin(db):
    """Create default admin user if none exists."""
    print("Creating default admin user...")
    
    # Check if admin exists
    admin = db.query(User).filter(User.is_superuser == True).first()
    if admin:
        print("Admin user already exists.")
        return
    
    # Create admin
    from backend.auth.models import RoleEnum
    
    admin_user = AuthService.create_user(
        db=db,
        email="admin@llmdbms.local",
        username="admin",
        password="admin123",  # CHANGE THIS IN PRODUCTION!
        full_name="System Administrator",
        roles=[RoleEnum.ADMIN]
    )
    admin_user.is_superuser = True
    db.commit()
    
    print(f"✓ Created admin user:")
    print(f"  Username: admin")
    print(f"  Password: admin123")
    print(f"  ⚠️  PLEASE CHANGE THIS PASSWORD IN PRODUCTION!")


def main():
    """Main initialization function."""
    print("=" * 60)
    print("LLM-based DBMS - Database Initialization")
    print("=" * 60)
    print()
    
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Database Type: {settings.DATABASE_TYPE}")
    print(f"Database URL: {settings.database_url}")
    print()
    
    # Initialize database schema
    print("Initializing database schema...")
    try:
        init_db()
        print("✓ Database schema created.")
    except Exception as e:
        print(f"✗ Error creating schema: {e}")
        return 1
    
    # Create session
    db = SessionLocal()
    
    try:
        # Initialize roles
        print("\nInitializing default roles...")
        RBACService.initialize_default_roles(db)
        print("✓ Default roles created (ADMIN, DATA_SCIENTIST, ANALYST, VIEWER).")
        
        # Create default admin
        print()
        create_default_admin(db)
        
        # Create sample data
        print()
        create_sample_sales_data(db)
        
        print()
        print("=" * 60)
        print("✓ Database initialization complete!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Review and change the default admin password")
        print("2. Start the API server: python -m backend.api.main")
        print("3. Access API docs: http://localhost:8000/docs")
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error during initialization: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
