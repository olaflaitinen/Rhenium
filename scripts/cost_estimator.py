"""
Cost Estimator for LLM-based DBMS.

Calculates estimated monthly costs based on query volume and model choice.
"""
import argparse

# Pricing (approximate as of late 2024)
PRICING = {
    "gpt-4o": {"input": 5.00, "output": 15.00}, # per 1M tokens
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "claude-3-sonnet": {"input": 3.00, "output": 15.00},
    "llama-3-70b": {"input": 0.90, "output": 0.90}, # via Groq/Together
    "local": {"input": 0.00, "output": 0.00} # Hardware cost excluded
}

def estimate_cost(model: str, daily_queries: int, avg_input_tokens: int = 500, avg_output_tokens: int = 100):
    if model not in PRICING:
        print(f"Model {model} not found in pricing table.")
        return

    rates = PRICING[model]
    
    daily_input_tokens = daily_queries * avg_input_tokens
    daily_output_tokens = daily_queries * avg_output_tokens
    
    daily_cost = (daily_input_tokens / 1_000_000 * rates["input"]) + \
                 (daily_output_tokens / 1_000_000 * rates["output"])
                 
    monthly_cost = daily_cost * 30
    
    print(f"--- Cost Estimate for {model} ---")
    print(f"Daily Queries: {daily_queries}")
    print(f"Avg Input Tokens: {avg_input_tokens}")
    print(f"Avg Output Tokens: {avg_output_tokens}")
    print(f"Daily Cost: ${daily_cost:.2f}")
    print(f"Monthly Cost: ${monthly_cost:.2f}")
    print("--------------------------------")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Estimate LLM costs")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", choices=PRICING.keys())
    parser.add_argument("--queries", type=int, default=1000, help="Daily query volume")
    
    args = parser.parse_args()
    
    estimate_cost(args.model, args.queries)
