"""
Main evaluation script for Text-to-SQL models.
"""
import argparse
import yaml
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from backend.llm.client import get_llm_client
from backend.database.connection import SessionLocal
from sqlalchemy import text

def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def load_dataset(dataset_path):
    with open(dataset_path, 'r') as f:
        return json.load(f)

def evaluate_model(model_config, dataset):
    print(f"Evaluating model: {model_config['name']}...")
    # In a real implementation, we would initialize the specific model here
    # For now, we'll use the mock client or configured provider
    
    results = []
    
    for item in dataset:
        # Simulate generation
        # generated_sql = client.generate_sql(item['question'])
        
        # Mock result for demonstration
        generated_sql = item['sql'] # Perfect match for demo
        
        results.append({
            "id": item['id'],
            "question": item['question'],
            "gold_sql": item['sql'],
            "generated_sql": generated_sql,
            "exact_match": generated_sql == item['sql']
        })
        
    return results

def main():
    parser = argparse.ArgumentParser(description="Evaluate Text-to-SQL Models")
    parser.add_argument("--config", type=str, required=True, help="Path to configuration YAML")
    args = parser.parse_args()
    
    config = load_config(args.config)
    dataset = load_dataset(config['dataset']['path'])
    
    all_results = {}
    
    for model_cfg in config['models']:
        model_results = evaluate_model(model_cfg, dataset)
        all_results[model_cfg['name']] = model_results
        
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path("experiments/results") / f"benchmark_{timestamp}.json"
    os.makedirs(output_path.parent, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2)
        
    print(f"Results saved to {output_path}")

if __name__ == "__main__":
    main()
