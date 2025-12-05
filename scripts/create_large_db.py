"""
Large-scale database generator for LLM-based DBMS.
Generates thousands of realistic sales records with detailed information.
"""

import sqlite3
import os
from pathlib import Path
from datetime import datetime, timedelta
import random

# Configuration
NUM_ORDERS = 5000  # Total number of orders to generate
NUM_CUSTOMERS = 500  # Number of unique customers
NUM_PRODUCTS = 100  # Number of unique products

# Create data directory
data_dir = Path("data/processed")
data_dir.mkdir(parents=True, exist_ok=True)

db_path = data_dir / "sales.db"

# Remove existing database
if db_path.exists():
    os.remove(db_path)
    print(f"Removed existing database: {db_path}")

# Create connection
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print(f"\n{'='*70}")
print(f"Large-Scale Database Generator")
print(f"Target: {NUM_ORDERS:,} orders, {NUM_CUSTOMERS} customers, {NUM_PRODUCTS} products")
print(f"{'='*70}\n")

# Create tables
print("Creating database schema...")

# Main sales table
cursor.execute("""
CREATE TABLE sales (
    ORDERNUMBER INTEGER PRIMARY KEY,
    QUANTITYORDERED INTEGER,
    PRICEEACH REAL,
    ORDERLINENUMBER INTEGER,
    SALES REAL,
    ORDERDATE TEXT,
    STATUS TEXT,
    QTR_ID INTEGER,
    MONTH_ID INTEGER,
    YEAR_ID INTEGER,
    PRODUCTLINE TEXT,
    MSRP REAL,
    PRODUCTCODE TEXT,
    CUSTOMERNAME TEXT,
    PHONE TEXT,
    ADDRESSLINE1 TEXT,
    ADDRESSLINE2 TEXT,
    CITY TEXT,
    STATE TEXT,
    POSTALCODE TEXT,
    COUNTRY TEXT,
    TERRITORY TEXT,
    CONTACTLASTNAME TEXT,
    CONTACTFIRSTNAME TEXT,
    DEALSIZE TEXT
)
""")

# Create indexes for performance
cursor.execute("CREATE INDEX idx_orderdate ON sales(ORDERDATE)")
cursor.execute("CREATE INDEX idx_productcode ON sales(PRODUCTCODE)")
cursor.execute("CREATE INDEX idx_customername ON sales(CUSTOMERNAME)")
cursor.execute("CREATE INDEX idx_country ON sales(COUNTRY)")
cursor.execute("CREATE INDEX idx_year_month ON sales(YEAR_ID, MONTH_ID)")

print("✓ Created sales table with indexes")

# Data pools for realistic generation
product_lines = [
    'Vintage Cars', 'Classic Cars', 'Motorcycles', 'Planes', 
    'Ships', 'Trains', 'Trucks and Buses'
]

statuses = ['Shipped', 'In Process', 'Resolved', 'On Hold', 'Cancelled', 'Disputed']
deal_sizes = ['Small', 'Medium', 'Large']

countries_data = {
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

first_names = ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph', 'Thomas', 'Charles',
               'Mary', 'Patricia', 'Jennifer', 'Linda', 'Barbara', 'Elizabeth', 'Susan', 'Jessica', 'Sarah', 'Karen',
               'Anna', 'Maria', 'Emma', 'Olivia', 'Sophia', 'Isabella', 'Mia', 'Charlotte', 'Amelia', 'Harper']

last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
              'Anderson', 'Taylor', 'Thomas', 'Hernandez', 'Moore', 'Martin', 'Jackson', 'Thompson', 'White', 'Lopez',
              'Lee', 'Gonzalez', 'Harris', 'Clark', 'Lewis', 'Robinson', 'Walker', 'Perez', 'Hall', 'Young']

company_types = ['Inc.', 'Ltd.', 'Corp.', 'LLC', 'Co.', 'GmbH', 'S.A.', 'Pty Ltd', 'KK', 'AB']
company_names = ['Tech', 'Global', 'International', 'Trading', 'Motors', 'Industries', 'Retail', 'Wholesale', 
                 'Distribution', 'Imports', 'Exports', 'Solutions', 'Systems', 'Enterprises', 'Holdings']

# Generate unique customers
print("Generating customer database...")
customers = []
for i in range(NUM_CUSTOMERS):
    country = random.choice(list(countries_data.keys()))
    city = random.choice(countries_data[country]['cities'])
    territory = countries_data[country]['territory']
    
    company_name = f"{random.choice(company_names)} {random.choice(company_types)}"
    contact_first = random.choice(first_names)
    contact_last = random.choice(last_names)
    
    customers.append({
        'name': company_name,
        'phone': f"+{random.randint(1, 99)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
        'address1': f"{random.randint(1, 9999)} {random.choice(['Main', 'Oak', 'Maple', 'Park', 'King', 'Queen'])} St",
        'address2': random.choice([None, None, None, f"Suite {random.randint(100, 999)}", f"Floor {random.randint(1, 50)}"]),
        'city': city,
        'state': random.choice([None, 'CA', 'NY', 'TX', 'FL', 'IL']) if country == 'USA' else None,
        'postal': f"{random.randint(10000, 99999)}",
        'country': country,
        'territory': territory,
        'contact_first': contact_first,
        'contact_last': contact_last
    })

print(f"✓ Generated {len(customers)} unique customers")

# Generate unique products
print("Generating product catalog...")
products = []
for i in range(NUM_PRODUCTS):
    product_line = random.choice(product_lines)
    product_code = f"S{random.randint(10, 99)}_{random.randint(1000, 9999)}"
    base_price = random.uniform(20, 500)
    msrp = base_price * random.uniform(1.2, 2.0)
    
    products.append({
        'code': product_code,
        'line': product_line,
        'msrp': round(msrp, 2),
        'base_price': round(base_price, 2)
    })

print(f"✓ Generated {len(products)} unique products")

# Generate orders
print(f"\nGenerating {NUM_ORDERS:,} sales orders...")
print("This may take a minute...")

start_date = datetime(2021, 1, 1)
end_date = datetime(2024, 12, 31)
date_range = (end_date - start_date).days

orders = []
for order_num in range(10100, 10100 + NUM_ORDERS):
    # Random date
    random_days = random.randint(0, date_range)
    order_date = start_date + timedelta(days=random_days)
    
    # Extract date components
    year = order_date.year
    month = order_date.month
    quarter = (month - 1) // 3 + 1
    
    # Random customer and product
    customer = random.choice(customers)
    product = random.choice(products)
    
    # Random quantity and pricing
    quantity = random.randint(1, 100)
    price_variance = random.uniform(0.8, 1.2)
    price_each = round(product['base_price'] * price_variance, 2)
    sales = round(quantity * price_each, 2)
    
    # Deal size based on sales value
    if sales < 1000:
        deal_size = 'Small'
    elif sales < 5000:
        deal_size = 'Medium'
    else:
        deal_size = 'Large'
    
    # Status (weighted towards shipped)
    status = random.choices(
        statuses, 
        weights=[70, 10, 5, 5, 5, 5],
        k=1
    )[0]
    
    orders.append((
        order_num,
        quantity,
        price_each,
        random.randint(1, 5),  # order line number
        sales,
        order_date.strftime('%Y-%m-%d'),
        status,
        quarter,
        month,
        year,
        product['line'],
        product['msrp'],
        product['code'],
        customer['name'],
        customer['phone'],
        customer['address1'],
        customer['address2'],
        customer['city'],
        customer['state'],
        customer['postal'],
        customer['country'],
        customer['territory'],
        customer['contact_last'],
        customer['contact_first'],
        deal_size
    ))
    
    # Progress indicator
    if (order_num - 10100 + 1) % 500 == 0:
        progress = ((order_num - 10100 + 1) / NUM_ORDERS) * 100
        print(f"  Progress: {progress:.1f}% ({order_num - 10100 + 1:,}/{NUM_ORDERS:,} orders)")

# Batch insert for performance
print("\nInserting records into database...")
cursor.executemany("""
    INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", orders)

conn.commit()
print(f"✓ Inserted {len(orders):,} orders")

# Generate statistics
print(f"\n{'='*70}")
print("Database Statistics:")
print(f"{'='*70}")

cursor.execute("SELECT COUNT(*) FROM sales")
total_orders = cursor.fetchone()[0]
print(f"Total Orders: {total_orders:,}")

cursor.execute("SELECT SUM(SALES) FROM sales")
total_revenue = cursor.fetchone()[0]
print(f"Total Revenue: ${total_revenue:,.2f}")

cursor.execute("SELECT AVG(SALES) FROM sales")
avg_order = cursor.fetchone()[0]
print(f"Average Order Value: ${avg_order:,.2f}")

cursor.execute("SELECT COUNT(DISTINCT CUSTOMERNAME) FROM sales")
unique_customers = cursor.fetchone()[0]
print(f"Unique Customers: {unique_customers}")

cursor.execute("SELECT COUNT(DISTINCT PRODUCTCODE) FROM sales")
unique_products = cursor.fetchone()[0]
print(f"Unique Products: {unique_products}")

cursor.execute("SELECT COUNT(DISTINCT COUNTRY) FROM sales")
countries = cursor.fetchone()[0]
print(f"Countries: {countries}")

cursor.execute("SELECT MIN(YEAR_ID), MAX(YEAR_ID) FROM sales")
min_year, max_year = cursor.fetchone()
print(f"Date Range: {min_year} - {max_year}")

print(f"\n{'='*70}")
print("Top 5 Countries by Revenue:")
print(f"{'='*70}")
cursor.execute("""
    SELECT COUNTRY, SUM(SALES) as revenue, COUNT(*) as orders
    FROM sales 
    GROUP BY COUNTRY 
    ORDER BY revenue DESC 
    LIMIT 5
""")
for country, revenue, orders in cursor.fetchall():
    print(f"  {country:15} ${revenue:>12,.2f}  ({orders:,} orders)")

print(f"\n{'='*70}")
print("Top 5 Products by Sales:")
print(f"{'='*70}")
cursor.execute("""
    SELECT PRODUCTLINE, SUM(SALES) as revenue, COUNT(*) as orders
    FROM sales 
    GROUP BY PRODUCTLINE 
    ORDER BY revenue DESC 
    LIMIT 5
""")
for product, revenue, orders in cursor.fetchall():
    print(f"  {product:20} ${revenue:>12,.2f}  ({orders:,} orders)")

print(f"\n{'='*70}")
print("Revenue by Year:")
print(f"{'='*70}")
cursor.execute("""
    SELECT YEAR_ID, SUM(SALES) as revenue, COUNT(*) as orders
    FROM sales 
    GROUP BY YEAR_ID 
    ORDER BY YEAR_ID
""")
for year, revenue, orders in cursor.fetchall():
    print(f"  {year}: ${revenue:>12,.2f}  ({orders:,} orders)")

print(f"\n{'='*70}")
print("Order Status Distribution:")
print(f"{'='*70}")
cursor.execute("""
    SELECT STATUS, COUNT(*) as count, 
           ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM sales), 1) as percentage
    FROM sales 
    GROUP BY STATUS 
    ORDER BY count DESC
""")
for status, count, pct in cursor.fetchall():
    print(f"  {status:15} {count:>6,} ({pct:>5.1f}%)")

# File size
db_size = db_path.stat().st_size
print(f"\n{'='*70}")
print(f"Database created successfully!")
print(f"Location: {db_path.absolute()}")
print(f"Size: {db_size / 1024 / 1024:.2f} MB")
print(f"{'='*70}\n")

conn.close()
