import argparse
import sys
from pathlib import Path
import time

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from backend.llm.client import get_llm_client
from backend.llm.prompts import get_text_to_sql_prompt
from backend.safety.validator import SQLValidator

# Sample dataset for evaluation
# In a real scenario, this would be loaded from a file
DATASET = [
    {
        "question": "What is the total revenue?",
        "gold_sql": "SELECT SUM(SALES) FROM sales;"
    },
    {
        "question": "How many orders were placed in 2003?",
        "gold_sql": "SELECT COUNT(DISTINCT ORDERNUMBER) FROM sales WHERE YEAR_ID = 2003;"
    },
    {
        "question": "List all customers in USA.",
        "gold_sql": "SELECT CUSTOMERNAME FROM sales WHERE COUNTRY = 'USA';"
    }
]

def evaluate():
    print("Starting evaluation...")
    llm_client = get_llm_client()
    
    correct_count = 0
    total_count = len(DATASET)
    total_latency = 0
    
    for item in DATASET:
        question = item["question"]
        gold_sql = item["gold_sql"]
        
        print(f"\nQuestion: {question}")
        
        start_time = time.time()
        prompt = get_text_to_sql_prompt(question)
        generated_sql = llm_client.generate_sql(prompt)
        latency = time.time() - start_time
        total_latency += latency
        
        # Clean SQL
        generated_sql = generated_sql.replace("```sql", "").replace("```", "").strip()
        
        print(f"Generated SQL: {generated_sql}")
        
        # Validate
        is_valid, error = SQLValidator.validate(generated_sql)
        if not is_valid:
            print(f"Validation Error: {error}")
            continue
            
        # Compare (Simple string comparison for now)
        # In production, we should execute both and compare results
        if generated_sql.lower().strip().rstrip(';') == gold_sql.lower().strip().rstrip(';'):
            print("Result: MATCH")
            correct_count += 1
        else:
            print(f"Result: MISMATCH (Expected: {gold_sql})")
            
    accuracy = (correct_count / total_count) * 100
    avg_latency = total_latency / total_count
    
    print("\n--- Evaluation Results ---")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Avg Latency: {avg_latency:.4f}s")

if __name__ == "__main__":
    evaluate()
