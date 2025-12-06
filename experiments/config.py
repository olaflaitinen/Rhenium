"""
Experiment Configuration Models.

Defines the schema for running Text-to-SQL experiments.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class LLMConfig(BaseModel):
    provider: str
    model: str
    temperature: float = 0.0
    max_tokens: int = 1000

class DatasetConfig(BaseModel):
    name: str
    path: str
    format: str = "json" # json, csv, spider

class EvaluationConfig(BaseModel):
    metrics: List[str] = ["exact_match", "execution_accuracy", "latency"]
    max_samples: Optional[int] = None

class ExperimentConfig(BaseModel):
    name: str
    description: Optional[str] = None
    llm: LLMConfig
    dataset: DatasetConfig
    evaluation: EvaluationConfig
    output_dir: str = "experiments/results"

def load_config(path: str) -> ExperimentConfig:
    import yaml
    with open(path, 'r', encoding='utf-8-sig') as f:
        data = yaml.safe_load(f)
    return ExperimentConfig(**data)
