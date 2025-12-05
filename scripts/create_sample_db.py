"""
Simple database initialization script without bcrypt issues.
Creates SQLite database with sample sales data.
"""

import sqlite3
import os
from pathlib import Path

# Create data directory if it doesn't exist
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

print(f"\n{'='*60}")
print(f"Creating database: {db_path}")
print(f"{'='*60}\n")

# Create sales table
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

print("✓ Created sales table")

# Insert sample data
sample_data = [
    (
        10100, 30, 100.0, 1, 3000.0, '2003-01-06', 'Shipped',
        1, 1, 2003, 'Vintage Cars', 95.0, 'S18_1749',
        'Land of Toys Inc.', '2125557818', '897 Long Airport Avenue', None,
        'NYC', 'NY', '10022', 'USA', 'NA', 'Yu', 'Kwai', 'Medium'
    ),
    (
        10101, 50, 120.0, 1, 6000.0, '2003-01-09', 'Shipped',
        1, 1, 2003, 'Classic Cars', 110.0, 'S24_2022',
        'Euro+ Shopping Channel', '(91) 555 94 44', 'C/ Moralzarzal, 86', None,
        'Madrid', None, '28034', 'Spain', 'EMEA', 'Freyre', 'Diego', 'Large'
    ),
    (
        10102, 20, 30.0, 1, 600.0, '2003-01-10', 'Shipped',
        1, 1, 2003, 'Vintage Cars', 28.0, 'S18_3232',
        'Volvo Model Replicas, Co', '0921-12 3555', 'Berguvsvägen  8', None,
        'Luleå', None, 'S-958 22', 'Sweden', 'EMEA', 'Berglund', 'Christina', 'Small'
    ),
    (
        10103, 45, 80.0, 1, 3600.0, '2003-01-29', 'Shipped',
        1, 1, 2003, 'Motorcycles', 77.0, 'S10_1949',
        'Baane Mini Imports', '07-98 9555', 'Erling Skakkes gate 78', None,
        'Stavern', None, '4110', 'Norway', 'EMEA', 'Bergulfsen', 'Jonas', 'Medium'
    ),
    (
        10104, 35, 90.0, 1, 3150.0, '2003-01-31', 'Shipped',
        1, 1, 2003, 'Classic Cars', 86.0, 'S18_2325',
        'Mini Gifts Distributors Ltd.', '4155551450', '5677 Strong St.', None,
        'San Rafael', 'CA', '97562', 'USA', 'NA', 'Nelson', 'Susan', 'Medium'
    ),
    (
        10105, 60, 110.0, 1, 6600.0, '2003-02-11', 'Shipped',
        1, 2, 2003, 'Vintage Cars', 105.0, 'S18_1342',
        'Danish Wholesale Imports', '31 12 3555', 'Vinbæltet 34', None,
        'Kobenhavn', None, '1734', 'Denmark', 'EMEA', 'Petersen', 'Jytte', 'Large'
    ),
    (
        10106, 25, 150.0, 1, 3750.0, '2003-02-17', 'Shipped',
        1, 2, 2003, 'Classic Cars', 145.0, 'S24_3969',
        'Land of Toys Inc.', '2125557818', '897 Long Airport Avenue', None,
        'NYC', 'NY', '10022', 'USA', 'NA', 'Yu', 'Kwai', 'Medium'
    ),
    (
        10107, 40, 95.0, 1, 3800.0, '2003-02-24', 'Shipped',
        1, 2, 2003, 'Ships', 92.0, 'S72_3212',
        'Royale Belge', '(071) 23 67 2555', 'Boulevard Tirou, 255', None,
        'Charleroi', None, 'B-6000', 'Belgium', 'EMEA', 'Cartrain', 'Pascale', 'Medium'
    ),
    (
        10108, 55, 75.0, 1, 4125.0, '2003-03-03', 'Shipped',
        1, 3, 2003, 'Trucks and Buses', 72.0, 'S50_1392',
        'Cruz & Sons Co.', '+63 2 555 3587', '15 McCallum Street', 'NatWest Center #13-03',
        'Makati City', None, '1227 MM', 'Philippines', 'Japan', 'Cruz', 'Arnold', 'Medium'
    ),
    (
        10109, 70, 100.0, 1, 7000.0, '2003-03-10', 'Shipped',
        1, 3, 2003, 'Planes', 97.0, 'S700_2047',
        'Boards & Toys Co.', '3105552373', '4097 Douglas Av.', None,
        'Glendale', 'CA', '92561', 'USA', 'NA', 'Young', 'Julie', 'Large'
    )
]

cursor.executemany("""
INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", sample_data)

conn.commit()

print(f"✓ Inserted {len(sample_data)} sample sales records")

# Verify data
cursor.execute("SELECT COUNT(*) FROM sales")
count = cursor.fetchone()[0]
print(f"\n✓ Database verification: {count} total records")

# Show sample queries
print(f"\n{'='*60}")
print("Sample Queries:")
print(f"{'='*60}")

cursor.execute("SELECT SUM(SALES) as total_revenue FROM sales")
total_revenue = cursor.fetchone()[0]
print(f"Total Revenue: ${total_revenue:,.2f}")

cursor.execute("SELECT COUNT(DISTINCT COUNTRY) as countries FROM sales")
countries = cursor.fetchone()[0]
print(f"Countries: {countries}")

cursor.execute("SELECT PRODUCTLINE, COUNT(*) as count FROM sales GROUP BY PRODUCTLINE ORDER BY count DESC LIMIT 3")
print("\nTop Product Lines:")
for row in cursor.fetchall():
    print(f"  - {row[0]}: {row[1]} orders")

conn.close()

print(f"\n{'='*60}")
print("✓ Database initialization complete!")
print(f"Database location: {db_path.absolute()}")
print(f"{'='*60}\n")
