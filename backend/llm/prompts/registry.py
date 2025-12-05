"""
Prompt Versioning System.

Manages different versions of prompts to allow for A/B testing and rollback.
"""
from typing import Dict, Optional
from pydantic import BaseModel
import yaml
import os

class PromptVersion(BaseModel):
    id: str
    version: str
    template: str
    description: str
    input_variables: list[str]

class PromptRegistry:
    def __init__(self, prompts_dir: str = "backend/llm/prompts/templates"):
        self.prompts_dir = prompts_dir
        self._prompts: Dict[str, Dict[str, PromptVersion]] = {}
        # Ensure directory exists
        os.makedirs(prompts_dir, exist_ok=True)

    def load_prompt(self, name: str, version: str = "latest") -> Optional[PromptVersion]:
        """Load a specific version of a prompt."""
        # In a real system, this might load from a DB or file system
        # For now, we simulate with a default template if file not found
        
        # Try to load from file
        file_path = os.path.join(self.prompts_dir, f"{name}_{version}.yaml")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
                return PromptVersion(**data)
        
        # Fallback for "text_to_sql" default
        if name == "text_to_sql":
            return PromptVersion(
                id="text_to_sql",
                version="v1.0",
                template="Given the following schema:\n{schema}\n\nWrite a SQL query to answer: {question}",
                description="Standard text-to-sql prompt",
                input_variables=["schema", "question"]
            )
        return None

    def save_prompt(self, prompt: PromptVersion):
        """Save a prompt version to disk."""
        file_path = os.path.join(self.prompts_dir, f"{prompt.id}_{prompt.version}.yaml")
        with open(file_path, 'w') as f:
            yaml.dump(prompt.dict(), f)

# Global registry
prompt_registry = PromptRegistry()
