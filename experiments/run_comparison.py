"""
Script to run model comparison and generate reports.
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from experiments.comparison_data import COMPARISON_TEST_CASES

OUTPUT_DIR = project_root / "experiments" / "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_markdown_report(results):
    """Generate a readable markdown report."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    md = f"# Model Comparison Report\n\n"
    md += f"**Date**: {timestamp}\n"
    md += f"**Total Test Cases**: {len(results)}\n\n"
    
    md += "## Summary Metrics\n\n"
    
    # Calculate metrics
    base_correct = sum(1 for r in results if r['models']['base_model']['is_correct'])
    ft_correct = sum(1 for r in results if r['models']['finetuned_model']['is_correct'])
    
    md += f"- **Base Model Accuracy**: {base_correct/len(results)*100:.1f}%\n"
    md += f"- **Fine-Tuned Model Accuracy**: {ft_correct/len(results)*100:.1f}%\n\n"
    
    md += "## Detailed Comparison\n\n"
    
    for case in results:
        md += f"### Test Case: {case['id']} - {case['category']}\n\n"
        md += f"**Question**: {case['question']}\n\n"
        md += f"**Gold Standard SQL**:\n```sql\n{case['gold_sql']}\n```\n\n"
        
        base = case['models']['base_model']
        ft = case['models']['finetuned_model']
        
        md += "| Feature | Base Model | Fine-Tuned Model |\n"
        md += "| :--- | :--- | :--- |\n"
        md += f"| **SQL Output** | `{base['sql']}` | `{ft['sql']}` |\n"
        md += f"| **Correct?** | {'[OK]' if base['is_correct'] else '[FAIL]'} | {'[OK]' if ft['is_correct'] else '[FAIL]'} |\n"
        md += f"| **Error Type** | {base['error_type']} | {ft['error_type']} |\n"
        md += f"| **Latency** | {base['latency_ms']}ms | {ft['latency_ms']}ms |\n"
        md += "\n---\n\n"
        
    return md

def main():
    print("Running model comparison...")
    
    # In a real scenario, we would run the models here.
    # For now, we use the pre-defined mock data in COMPARISON_TEST_CASES
    results = COMPARISON_TEST_CASES
    
    # Save JSON
    json_path = OUTPUT_DIR / "comparison_results.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Saved JSON results to {json_path}")
    
    # Generate Markdown
    md_content = generate_markdown_report(results)
    md_path = OUTPUT_DIR / "comparison_report.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"Saved Markdown report to {md_path}")
    
    print("\nComparison complete!")

if __name__ == "__main__":
    main()
