"""
Benchmark Runner.

CLI tool to run experiments based on a configuration file.
"""
import argparse
import json
import os
import time
from datetime import datetime
from typing import List, Dict

from experiments.config import load_config, ExperimentConfig
from backend.llm.client import LLMClientFactory
from backend.safety.validator import SQLValidator
# Mocking database execution for benchmark isolation or importing real executor
from backend.database.executor import execute_sql_query

class BenchmarkRunner:
    def __init__(self, config: ExperimentConfig):
        self.config = config
        self.llm_client = LLMClientFactory.create(
            provider=config.llm.provider,
            api_key=os.getenv("OPENAI_API_KEY") # Ensure env var is set
        )
        self.results = []

    def run(self):
        print(f"Starting experiment: {self.config.name}")
        dataset = self._load_dataset()
        
        for i, sample in enumerate(dataset):
            if self.config.evaluation.max_samples and i >= self.config.evaluation.max_samples:
                break
                
            question = sample['question']
            gold_sql = sample['sql']
            
            start_time = time.time()
            try:
                # Generate
                # Note: In a real benchmark, we'd use the prompt template from config
                generated_sql = self.llm_client.generate_sql(f"Question: {question}") 
                
                latency = time.time() - start_time
                
                # Evaluate
                exact_match = (generated_sql.strip().lower() == gold_sql.strip().lower())
                
                # Execution match (Placeholder logic)
                # real implementation would execute both and compare results
                execution_match = False 
                
                self.results.append({
                    "question": question,
                    "gold_sql": gold_sql,
                    "generated_sql": generated_sql,
                    "exact_match": exact_match,
                    "latency": latency
                })
                
                print(f"Sample {i+1}: {'PASS' if exact_match else 'FAIL'} ({latency:.2f}s)")
                
            except Exception as e:
                print(f"Sample {i+1}: ERROR - {str(e)}")

        self._save_results()

    def _load_dataset(self) -> List[Dict]:
        path = self.config.dataset.path
        if not os.path.exists(path):
            raise FileNotFoundError(f"Dataset not found at {path}")
        with open(path, 'r') as f:
            return json.load(f)

    def _save_results(self):
        os.makedirs(self.config.output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.config.name}_{timestamp}.json"
        path = os.path.join(self.config.output_dir, filename)
        
        with open(path, 'w') as f:
            json.dump({
                "config": self.config.dict(),
                "results": self.results,
                "summary": {
                    "total": len(self.results),
                    "accuracy": sum(r['exact_match'] for r in self.results) / len(self.results) if self.results else 0
                }
            }, f, indent=2)
        print(f"Results saved to {path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run LLM Benchmark")
    parser.add_argument("--config", type=str, required=True, help="Path to experiment config yaml")
    args = parser.parse_args()
    
    config = load_config(args.config)
    runner = BenchmarkRunner(config)
    runner.run()
