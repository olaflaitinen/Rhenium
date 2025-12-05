# Experiments Directory

Research evaluation framework for Text-to-SQL performance benchmarking.

## Purpose

This directory contains tools and datasets for evaluating the LLM-Based DBMS system's natural language to SQL translation accuracy and performance.

## Directory Structure

```
experiments/
├── datasets/ # Evaluation datasets (gitignored)
│ ├── sales_queries.json # Sales domain queries
│ ├── spider_sample.json # Spider dataset samples (if used)
│ └── .gitkeep
├── configs/ # Evaluation configurations
│ └── benchmark_v1.yaml
├── results/ # Benchmark results (gitignored)
├── evaluate_text_to_sql.py # Main evaluation script
├── benchmark.py # Benchmarking utilities
├── config.py # Configuration loader
└── README.md # This file
```

## Available Scripts

### 1. evaluate_text_to_sql.py

**Purpose**: Evaluate Text-to-SQL generation accuracy.

**Usage**:
```bash
python -m experiments.evaluate_text_to_sql
```

**What it evaluates**:
- SQL generation accuracy (exact match)
- Query execution correctness
- Average latency
- Error rate
- Validation pass rate

**Sample output**:
```
Starting evaluation...

Question: What is the total revenue?
Generated SQL: SELECT SUM(SALES) FROM sales;
Result: MATCH
Latency: 1.2s

Question: How many orders were placed in 2003?
Generated SQL: SELECT COUNT(DISTINCT ORDERNUMBER) FROM sales WHERE YEAR_ID = 2003;
Result: MATCH
Latency: 1.1s

--- Evaluation Results ---
Accuracy: 90.00%
Avg Latency: 1.15s
```

---

### 2. benchmark.py

**Purpose**: Comprehensive benchmarking utilities.

**Usage**:
```python
from experiments.benchmark import run_benchmark

results = run_benchmark(
 dataset_path='experiments/datasets/sales_queries.json',
 llm_provider='openai',
 num_iterations=3
)
```

**Features**:
- Multiple LLM provider comparison
- Performance profiling
- Results export (JSON, CSV)
- Statistical analysis

---

## Creating Evaluation Datasets

### Format

Datasets should be JSON files with the following structure:

```json
[
 {
 "question": "Natural language question",
 "gold_sql": "Expected SQL query",
 "description": "Optional description",
 "difficulty": "easy|medium|hard",
 "category": "aggregation|filter|join|etc"
 }
]
```

### Example: sales_queries.json

Create `experiments/datasets/sales_queries.json`:

```json
[
 {
 "question": "What is the total revenue from all sales?",
 "gold_sql": "SELECT SUM(SALES) as total_revenue FROM sales;",
 "difficulty": "easy",
 "category": "aggregation"
 },
 {
 "question": "Show the top 5 customers by total spending.",
 "gold_sql": "SELECT CUSTOMERNAME, SUM(SALES) as total FROM sales GROUP BY CUSTOMERNAME ORDER BY total DESC LIMIT 5;",
 "difficulty": "medium",
 "category": "aggregation-groupby"
 },
 {
 "question": "How many distinct products were sold in each quarter of 2003?",
 "gold_sql": "SELECT QTR_ID, COUNT(DISTINCT PRODUCTCODE) as products FROM sales WHERE YEAR_ID = 2003 GROUP BY QTR_ID;",
 "difficulty": "medium",
 "category": "aggregation-filter"
 }
]
```

### Using Public Datasets

#### Spider Dataset

```bash
# Download Spider dataset
wget https://drive.google.com/uc?export=download&id=1TqleXec_OykOYFREKKtschzY29dUcVAQ

# Extract to experiments/datasets/
unzip spider.zip -d experiments/datasets/
```

#### WikiSQL

```bash
# Install huggingface datasets
pip install datasets

# Load in Python
from datasets import load_dataset
dataset = load_dataset("wikisql")
```

---

## Evaluation Metrics

### 1. Exact Match (EM)

Percentage of generated SQL queries that exactly match the gold standard:

```python
def exact_match(generated, gold):
 # Normalize whitespace and case
 gen_norm = ' '.join(generated.lower().split())
 gold_norm = ' '.join(gold.lower().split())
 return gen_norm == gold_norm
```

### 2. Execution Accuracy (EX)

Percentage of queries that return the correct result set:

```python
def execution_accuracy(generated, gold, db):
 gen_result = execute_query(generated, db)
 gold_result = execute_query(gold, db)
 return gen_result == gold_result
```

### 3. Valid Syntax

Percentage of generated queries that are syntactically valid:

```python
def valid_syntax(sql):
 try:
 sqlparse.parse(sql)
 return True
 except:
 return False
```

### 4. Safety Compliance

Percentage of queries that pass safety validation:

```python
from backend.safety.validator import SQLValidator

def safety_compliance(sql, user):
 validator = SQLValidator(user)
 is_valid, _ = validator.validate(sql)
 return is_valid
```

---

## Running Benchmarks

### Basic Evaluation

```bash
# Use mock LLM (no API key needed)
LLM_PROVIDER=mock python -m experiments.evaluate_text_to_sql

# Use OpenAI
LLM_PROVIDER=openai OPENAI_API_KEY=sk-... python -m experiments.evaluate_text_to_sql
```

### Comparing Providers

```python
from experiments.benchmark import compare_providers

results = compare_providers(
 dataset='experiments/datasets/sales_queries.json',
 providers=['openai', 'anthropic', 'mock']
)

# Results structure:
# {
# 'openai': {'accuracy': 0.95, 'avg_latency': 1.2},
# 'anthropic': {'accuracy': 0.93, 'avg_latency': 1.5},
# 'mock': {'accuracy': 0.15, 'avg_latency': 0.01}
# }
```

### With Configuration File

Create `experiments/configs/benchmark_v1.yaml`:

```yaml
dataset:
 path: "experiments/datasets/sales_queries.json"
 split: "test" # train/val/test

llm:
 provider: "openai"
 model: "gpt-4-turbo"
 temperature: 0.0
 max_tokens: 500

evaluation:
 metrics:
 - exact_match
 - execution_accuracy
 - valid_syntax
 - safety_compliance
 num_iterations: 3

output:
 results_dir: "experiments/results"
 export_format: ["json", "csv"]
 save_errors: true
```

Run with config:

```bash
python -m experiments.evaluate_text_to_sql --config experiments/configs/benchmark_v1.yaml
```

---

## Analyzing Results

### Generate Report

```python
from experiments.benchmark import generate_report

report = generate_report('experiments/results/benchmark_20250101.json')

# Prints:
# ===== Benchmark Report =====
# Dataset: sales_queries.json
# Total Queries: 50
# 
# Metrics:
# - Exact Match: 45/50 (90.0%)
# - Execution Accuracy: 48/50 (96.0%)
# - Valid Syntax: 49/50 (98.0%)
# - Avg Latency: 1.25s
# 
# By Difficulty:
# - Easy: 100% (20/20)
# - Medium: 90% (18/20)
# - Hard: 70% (7/10)
```

### Export Results

```python
from experiments.benchmark import export_results

# Export to CSV
export_results(
 'experiments/results/benchmark.json',
 format='csv',
 output_path='experiments/results/benchmark.csv'
)

# Export to LaTeX table
export_results(
 'experiments/results/benchmark.json',
 format='latex',
 output_path='paper/tables/results.tex'
)
```

---

## Advanced Evaluation

### Error Analysis

```python
from experiments.benchmark import analyze_errors

errors = analyze_errors('experiments/results/benchmark.json')

# Categorize errors:
# - Syntax errors
# - Semantic errors
# - Safety violations
# - Timeout errors
```

### Cross-Database Testing

Test queries across different database backends:

```python
from experiments.benchmark import cross_db_test

results = cross_db_test(
 query="SELECT * FROM sales WHERE country = 'USA'",
 databases=['sqlite', 'postgresql', 'mysql']
)
```

### Prompt Engineering Experiments

Test different prompt strategies:

```python
prompts = [
 'zero_shot',
 'few_shot_3',
 'few_shot_5',
 'chain_of_thought'
]

for prompt_type in prompts:
 results = run_evaluation(
 dataset='sales_queries.json',
 prompt_strategy=prompt_type
 )
 save_results(f'results_{prompt_type}.json', results)
```

---

## Best Practices

1. **Version Your Datasets**: Use git to track dataset changes
2. **Document Changes**: Update CHANGELOG when modifying evaluation metrics
3. **Reproducibility**: Fix random seeds, save full configuration
4. **Error Logging**: Save failed queries for analysis
5. **Statistical Significance**: Run multiple iterations (3-5)
6. **Cross-Validation**: Test on unseen data
7. **Baseline Comparison**: Always compare against a baseline (e.g., mock provider)

---

## Contributing Datasets

When adding new evaluation datasets:

1. **Format**: Use the standard JSON format
2. **Quality**: Manually verify SQL correctness
3. **Diversity**: Cover different query types
4. **Documentation**: Add description and metadata
5. **Licensing**: Ensure dataset can be shared

Example contribution:

```json
{
 "dataset_name": "sales_advanced_v1",
 "version": "1.0",
 "created": "2025-12-03",
 "author": "Your Name",
 "license": "MIT",
 "queries": [
 // ... query objects
 ]
}
```

---

## Academic Use

For research papers and publications:

1. **Cite the Dataset**: Include dataset details in methodology
2. **Report All Metrics**: Exact match, execution accuracy, latency
3. **Statistical Tests**: Use significance tests when comparing methods
4. **Reproducibility**: Share configuration files and seeds

### Example Citation

```bibtex
@dataset{sales_queries_v1,
 title={Sales Domain Text-to-SQL Evaluation Dataset},
 author={Kulalı, Derya Umut and Aydın, Anıl and Alhan, Sıla},
 year={2025},
 institution={Eskişehir Technical University}
}
```

---

## Troubleshooting

### Common Issues

**1. Module Import Errors**

```bash
# Run as module from project root
python -m experiments.evaluate_text_to_sql
```

**2. Dataset Not Found**

```bash
# Check path is correct
ls experiments/datasets/

# Datasets are gitignored - create your own or download
```

**3. API Rate Limits**

```python
# Add delays between requests
import time
time.sleep(1) # 1 second delay
```

**4. Memory Issues with Large Datasets**

```python
# Process in batches
batch_size = 10
for i in range(0, len(dataset), batch_size):
 batch = dataset[i:i+batch_size]
 evaluate(batch)
```

---

## Future Work

- [ ] Integration with Spider benchmark server
- [ ] Automated dataset augmentation
- [ ] Multi-language support (Turkish)
- [ ] Query difficulty classifier
- [ ] Semantic equivalence checker
- [ ] Interactive evaluation UI

---

For questions about experiments and evaluation, contact the research team through Eskişehir Technical University.
