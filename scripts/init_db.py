"""
Production-grade database initialization script.

Initializes:
- Database schema (all tables)
- Default roles
- Default admin user
- Large-scale sample sales data (5000+ records)
"""
import sys
import random
from pathlib import Path
from datetime import datetime, timedelta
from sqlalchemy import text

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from backend.database.connection import init_db, SessionLocal, engine
from backend.auth.models import User, RoleEnum
from backend.auth.service import AuthService
from backend.auth.rbac import RBACService
from backend.config.settings import settings

# --- Data Generation Constants ---
NUM_ORDERS = 5000
NUM_CUSTOMERS = 500
NUM_PRODUCTS = 100

PRODUCT_LINES = [
    'Vintage Cars', 'Classic Cars', 'Motorcycles', 'Planes', 
    'Ships', 'Trains', 'Trucks and Buses'
]

STATUSES = ['Shipped', 'In Process', 'Resolved', 'On Hold', 'Cancelled', 'Disputed']

COUNTRIES_DATA = {
    'USA': {'territory': 'NA', 'cities': ['NYC', 'LA', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']},
    'UK': {'territory': 'EMEA', 'cities': ['London', 'Manchester', 'Birmingham', 'Leeds', 'Glasgow', 'Sheffield', 'Edinburgh', 'Liverpool', 'Bristol', 'Cardiff']},
    'France': {'territory': 'EMEA', 'cities': ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice', 'Nantes', 'Strasbourg', 'Montpellier', 'Bordeaux', 'Lille']},
    'Germany': {'territory': 'EMEA', 'cities': ['Berlin', 'Munich', 'Hamburg', 'Frankfurt', 'Cologne', 'Stuttgart', 'Dusseldorf', 'Dortmund', 'Essen', 'Leipzig']},
    'Spain': {'territory': 'EMEA', 'cities': ['Madrid', 'Barcelona', 'Valencia', 'Seville', 'Zaragoza', 'Malaga', 'Murcia', 'Palma', 'Las Palmas', 'Bilbao']},
    'Italy': {'territory': 'EMEA', 'cities': ['Rome', 'Milan', 'Naples', 'Turin', 'Palermo', 'Genoa', 'Bologna', 'Florence', 'Bari', 'Catania']},
    'Canada': {'territory': 'NA', 'cities': ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton', 'Ottawa', 'Winnipeg', 'Quebec City', 'Hamilton', 'Kitchener']},
    'Australia': {'territory': 'APAC', 'cities': ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Gold Coast', 'Canberra', 'Newcastle', 'Wollongong', 'Logan City']},
    'Japan': {'territory': 'APAC', 'cities': ['Tokyo', 'Yokohama', 'Osaka', 'Nagoya', 'Sapporo', 'Fukuoka', 'Kobe', 'Kyoto', 'Kawasaki', 'Saitama']},
    'China': {'territory': 'APAC', 'cities': ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Chengdu', 'Hangzhou', 'Wuhan', 'Xi\'an', 'Chongqing', 'Tianjin']},
    'Brazil': {'territory': 'LATAM', 'cities': ['São Paulo', 'Rio de Janeiro', 'Brasília', 'Salvador', 'Fortaleza', 'Belo Horizonte', 'Manaus', 'Curitiba', 'Recife', 'Porto Alegre']},
    'Mexico': {'territory': 'LATAM', 'cities': ['Mexico City', 'Guadalajara', 'Monterrey', 'Puebla', 'Tijuana', 'León', 'Juárez', 'Zapopan', 'Mérida', 'San Luis Potosí']},
    'India': {'territory': 'APAC', 'cities': ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Ahmedabad', 'Chennai', 'Kolkata', 'Surat', 'Pune', 'Jaipur']},
    'Singapore': {'territory': 'APAC', 'cities': ['Singapore', 'Jurong', 'Woodlands', 'Tampines', 'Bedok', 'Hougang', 'Choa Chu Kang', 'Yishun', 'Sengkang', 'Punggol']},
    'Sweden': {'territory': 'EMEA', 'cities': ['Stockholm', 'Gothenburg', 'Malmö', 'Uppsala', 'Västerås', 'Örebro', 'Linköping', 'Helsingborg', 'Jönköping', 'Norrköping']},
}

FIRST_NAMES = ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph', 'Thomas', 'Charles', 'Mary', 'Patricia', 'Jennifer', 'Linda', 'Barbara', 'Elizabeth', 'Susan', 'Jessica', 'Sarah', 'Karen']
LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Anderson', 'Taylor', 'Thomas', 'Hernandez', 'Moore', 'Martin']
COMPANY_TYPES = ['Inc.', 'Ltd.', 'Corp.', 'LLC', 'Co.', 'GmbH', 'S.A.', 'Pty Ltd', 'KK', 'AB']
COMPANY_NAMES = ['Tech', 'Global', 'International', 'Trading', 'Motors', 'Industries', 'Retail', 'Wholesale', 'Distribution', 'Imports', 'Exports', 'Solutions']


def generate_bulk_data():
    """Generate bulk data for insertion."""
    print("Generating synthetic data...")
    
    # Customers
    customers = []
    for _ in range(NUM_CUSTOMERS):
        country = random.choice(list(COUNTRIES_DATA.keys()))
        city = random.choice(COUNTRIES_DATA[country]['cities'])
        territory = COUNTRIES_DATA[country]['territory']
        
        customers.append({
            'name': f"{random.choice(COMPANY_NAMES)} {random.choice(COMPANY_TYPES)}",
            'phone': f"+{random.randint(1, 99)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
            'address1': f"{random.randint(1, 9999)} {random.choice(['Main', 'Oak', 'Maple', 'Park'])} St",
            'address2': random.choice([None, f"Suite {random.randint(100, 999)}"]),
            'city': city,
            'state': random.choice([None, 'CA', 'NY', 'TX']) if country == 'USA' else None,
            'postal': f"{random.randint(10000, 99999)}",
            'country': country,
            'territory': territory,
            'contact_first': random.choice(FIRST_NAMES),
            'contact_last': random.choice(LAST_NAMES)
        })

    # Products
    products = []
    for _ in range(NUM_PRODUCTS):
        base_price = random.uniform(20, 500)
        products.append({
            'code': f"S{random.randint(10, 99)}_{random.randint(1000, 9999)}",
            'line': random.choice(PRODUCT_LINES),
            'msrp': round(base_price * random.uniform(1.2, 2.0), 2),
            'base_price': round(base_price, 2)
        })

    # Orders
    orders = []
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range = (end_date - start_date).days

    for order_num in range(10100, 10100 + NUM_ORDERS):
        order_date = start_date + timedelta(days=random.randint(0, date_range))
        customer = random.choice(customers)
        product = random.choice(products)
        quantity = random.randint(1, 100)
        price_each = round(product['base_price'] * random.uniform(0.8, 1.2), 2)
        sales = round(quantity * price_each, 2)
        
        deal_size = 'Small' if sales < 1000 else 'Medium' if sales < 5000 else 'Large'
        status = random.choices(STATUSES, weights=[70, 10, 5, 5, 5, 5], k=1)[0]

        orders.append({
            'ORDERNUMBER': order_num,
            'QUANTITYORDERED': quantity,
            'PRICEEACH': price_each,
            'ORDERLINENUMBER': random.randint(1, 15),
            'SALES': sales,
            'ORDERDATE': order_date,
            'STATUS': status,
            'QTR_ID': (order_date.month - 1) // 3 + 1,
            'MONTH_ID': order_date.month,
            'YEAR_ID': order_date.year,
            'PRODUCTLINE': product['line'],
            'MSRP': product['msrp'],
            'PRODUCTCODE': product['code'],
            'CUSTOMERNAME': customer['name'],
            'PHONE': customer['phone'],
            'ADDRESSLINE1': customer['address1'],
            'ADDRESSLINE2': customer['address2'],
            'CITY': customer['city'],
            'STATE': customer['state'],
            'POSTALCODE': customer['postal'],
            'COUNTRY': customer['country'],
            'TERRITORY': customer['territory'],
            'CONTACTLASTNAME': customer['contact_last'],
            'CONTACTFIRSTNAME': customer['contact_first'],
            'DEALSIZE': deal_size
        })
    
    return orders

def insert_bulk_data(db):
    """Insert bulk data using SQLAlchemy Core for performance."""
    print(f"Inserting {NUM_ORDERS} records...")
    
    # Check if data exists
    result = db.execute(text("SELECT COUNT(*) FROM sales"))
    count = result.scalar()
    if count and count > 0:
        print(f"Database already contains {count} records. Skipping bulk insertion.")
        return

    orders = generate_bulk_data()
    
    # Use raw SQL for speed
    try:
        # Prepare data for bulk insert
        # Note: We use a simplified approach compatible with SQLite and Postgres
        # For very large datasets, specific bulk copy methods would be better
        
        # We'll use SQLAlchemy's insert
        from backend.database.models import SalesOrder
        
        # Batch insert
        batch_size = 1000
        for i in range(0, len(orders), batch_size):
            batch = orders[i:i + batch_size]
            db.execute(
                insert(SalesOrder),
                batch
            )
            print(f"  Inserted batch {i//batch_size + 1}/{(len(orders)-1)//batch_size + 1}")
            
        db.commit()
        print("✓ Bulk insertion complete.")
        
    except Exception as e:
        print(f"✗ Error inserting data: {e}")
        db.rollback()
        raise

def create_default_admin(db):
    """Create default admin user."""
    print("Creating default admin user...")
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            print("Admin user already exists.")
            return

        # Create admin with explicit error handling
        admin_user = AuthService.create_user(
            db=db,
            email="admin@llmdbms.local",
            username="admin",
            password="admin123",
            full_name="System Administrator",
            roles=[RoleEnum.ADMIN]
        )
        admin_user.is_superuser = True
        db.commit()
        
        print("✓ Created admin user (admin/admin123)")
        print("  ⚠️  CHANGE PASSWORD IN PRODUCTION!")
        
    except Exception as e:
        print(f"Warning: Could not create admin user: {e}")
        # Don't fail the whole script for this, might be a hashing issue
        db.rollback()

def main():
    print("=" * 60)
    print("LLM-based DBMS - Database Initialization")
    print("=" * 60)
    
    try:
        # 1. Initialize Schema
        print("\n1. Initializing Schema...")
        init_db()
        print("✓ Schema created.")
        
        db = SessionLocal()
        
        # 2. Initialize Roles
        print("\n2. Initializing Roles...")
        RBACService.initialize_default_roles(db)
        print("✓ Roles created.")
        
        # 3. Create Admin
        print("\n3. Creating Admin...")
        create_default_admin(db)
        
        # 4. Insert Data
        print("\n4. Inserting Sample Data...")
        insert_bulk_data(db)
        
        print("\n" + "=" * 60)
        print("✓ Initialization Complete!")
        print("=" * 60)
        return 0
        
    except Exception as e:
        print(f"\n✗ Fatal Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    sys.exit(main())
