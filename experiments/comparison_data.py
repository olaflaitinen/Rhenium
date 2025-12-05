"""
Comparison data for model evaluation.
Contains test prompts, gold standard SQL, and mock responses for different models.
"""

COMPARISON_TEST_CASES = [
    {
        "id": "TC001",
        "category": "Simple Aggregation",
        "question": "What is the total sales amount for the year 2004?",
        "gold_sql": "SELECT SUM(SALES) FROM sales WHERE YEAR_ID = 2004",
        "complexity": "Simple",
        "models": {
            "base_model": {
                "sql": "SELECT SUM(amount) FROM orders WHERE year = '2004'",
                "error_type": "Schema Hallucination",
                "is_correct": False,
                "latency_ms": 350
            },
            "finetuned_model": {
                "sql": "SELECT SUM(SALES) FROM sales WHERE YEAR_ID = 2004",
                "error_type": "None",
                "is_correct": True,
                "latency_ms": 410
            }
        }
    },
    {
        "id": "TC002",
        "category": "Filtering",
        "question": "List all customers in France who have a credit limit over 50000.",
        "gold_sql": "SELECT CUSTOMERNAME FROM customers WHERE COUNTRY = 'France' AND CREDITLIMIT > 50000",
        "complexity": "Medium",
        "models": {
            "base_model": {
                "sql": "SELECT name FROM client_table WHERE country_name = 'France' AND credit > 50000",
                "error_type": "Schema Hallucination",
                "is_correct": False,
                "latency_ms": 380
            },
            "finetuned_model": {
                "sql": "SELECT CUSTOMERNAME FROM customers WHERE COUNTRY = 'France' AND CREDITLIMIT > 50000",
                "error_type": "None",
                "is_correct": True,
                "latency_ms": 420
            }
        }
    },
    {
        "id": "TC003",
        "category": "Complex Join",
        "question": "Show the top 5 products by quantity sold in 2003.",
        "gold_sql": "SELECT PRODUCTCODE, SUM(QUANTITYORDERED) as total_qty FROM sales WHERE YEAR_ID = 2003 GROUP BY PRODUCTCODE ORDER BY total_qty DESC LIMIT 5",
        "complexity": "Complex",
        "models": {
            "base_model": {
                "sql": "SELECT product, count(*) FROM sales_data WHERE date LIKE '2003%' GROUP BY product ORDER BY count(*) DESC LIMIT 5",
                "error_type": "Logic Error",
                "is_correct": False,
                "latency_ms": 450
            },
            "finetuned_model": {
                "sql": "SELECT PRODUCTCODE, SUM(QUANTITYORDERED) FROM sales WHERE YEAR_ID = 2003 GROUP BY PRODUCTCODE ORDER BY 2 DESC LIMIT 5",
                "error_type": "None",
                "is_correct": True,
                "latency_ms": 480
            }
        }
    },
    {
        "id": "TC004",
        "category": "Ambiguous",
        "question": "Show me the big deals.",
        "gold_sql": "SELECT * FROM sales WHERE DEALSIZE = 'Large'",
        "complexity": "Simple",
        "models": {
            "base_model": {
                "sql": "SELECT * FROM deals WHERE size = 'big'",
                "error_type": "Schema Hallucination",
                "is_correct": False,
                "latency_ms": 320
            },
            "finetuned_model": {
                "sql": "SELECT * FROM sales WHERE DEALSIZE = 'Large'",
                "error_type": "None",
                "is_correct": True,
                "latency_ms": 390
            }
        }
    },
    {
        "id": "TC005",
        "category": "Date Handling",
        "question": "How many orders were shipped in Q4 2004?",
        "gold_sql": "SELECT COUNT(*) FROM sales WHERE QTR_ID = 4 AND YEAR_ID = 2004 AND STATUS = 'Shipped'",
        "complexity": "Medium",
        "models": {
            "base_model": {
                "sql": "SELECT count(*) FROM orders WHERE quarter = 4 AND year = 2004",
                "error_type": "Logic Error",
                "is_correct": False,
                "latency_ms": 360
            },
            "finetuned_model": {
                "sql": "SELECT COUNT(*) FROM sales WHERE QTR_ID = 4 AND YEAR_ID = 2004 AND STATUS = 'Shipped'",
                "error_type": "None",
                "is_correct": True,
                "latency_ms": 430
            }
        }
    }
]
