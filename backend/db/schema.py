from sqlalchemy import MetaData, Table, Column, Integer, String, Float, Date

metadata = MetaData()

# Define the 'sales' table
# This schema mimics the classic sample sales data structure
sales_table = Table(
    "sales",
    metadata,
    Column("ORDERNUMBER", Integer, primary_key=True),
    Column("QUANTITYORDERED", Integer),
    Column("PRICEEACH", Float),
    Column("ORDERLINENUMBER", Integer),
    Column("SALES", Float),
    Column("ORDERDATE", Date),
    Column("STATUS", String),
    Column("QTR_ID", Integer),
    Column("MONTH_ID", Integer),
    Column("YEAR_ID", Integer),
    Column("PRODUCTLINE", String),
    Column("MSRP", Integer),
    Column("PRODUCTCODE", String),
    Column("CUSTOMERNAME", String),
    Column("PHONE", String),
    Column("ADDRESSLINE1", String),
    Column("ADDRESSLINE2", String),
    Column("CITY", String),
    Column("STATE", String),
    Column("POSTALCODE", String),
    Column("COUNTRY", String),
    Column("TERRITORY", String),
    Column("CONTACTLASTNAME", String),
    Column("CONTACTFIRSTNAME", String),
    Column("DEALSIZE", String),
)
