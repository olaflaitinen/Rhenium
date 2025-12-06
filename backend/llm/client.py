"""
Enhanced LLM client with multi-provider support.
"""
from abc import ABC, abstractmethod
from typing import Optional

from backend.config.settings import settings


class LLMClient(ABC):
    """Abstract base class for LLM clients."""
    
    @abstractmethod
    def generate_sql(self, prompt: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        """Generate SQL from a natural language prompt."""
        pass

    @abstractmethod
    def explain_sql(self, sql: str, question: str) -> str:
        """Explain a generated SQL query."""
        pass


class MockLLMClient(LLMClient):
    """Mock LLM client for testing and development without API keys."""
    
    def generate_sql(self, prompt: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        # Return a safe, valid SQL query regardless of input
        return "SELECT * FROM sales LIMIT 5;"

    def explain_sql(self, sql: str, question: str) -> str:
        return f"This query addresses '{question}' by executing: {sql}"


class OpenAILLMClient(LLMClient):
    """LLM client using OpenAI's API via LangChain."""
    
    def __init__(self):
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in configuration.")
        
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
        
        self.llm = ChatOpenAI(
            model=settings.MODEL_NAME,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            api_key=api_key
        )
        self._SystemMessage = SystemMessage
        self._HumanMessage = HumanMessage
        self._AIMessage = AIMessage

    def generate_sql(self, prompt: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        messages = [
            self._SystemMessage(content="You are an expert SQL assistant. Return ONLY the SQL query, nothing else. Do not use markdown formatting.")
        ]
        
        if history:
            for msg in history:
                if msg['role'] == 'user':
                    messages.append(self._HumanMessage(content=msg['content']))
                elif msg['role'] == 'assistant':
                    messages.append(self._AIMessage(content=msg['content']))
        
        messages.append(self._HumanMessage(content=prompt))
        
        response = self.llm.invoke(messages)
        return response.content.strip()

    def explain_sql(self, sql: str, question: str) -> str:
        messages = [
            self._SystemMessage(content="You are a helpful data analyst. Explain the SQL query in simple terms."),
            self._HumanMessage(content=f"Question: {question}\nSQL: {sql}\n\nExplain this query:")
        ]
        response = self.llm.invoke(messages)
        return response.content.strip()


class AnthropicLLMClient(LLMClient):
    """LLM client using Anthropic's Claude API."""
    
    def __init__(self):
        api_key = settings.ANTHROPIC_API_KEY
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY is not set in configuration.")
        
        from langchain_anthropic import ChatAnthropic
        
        self.llm = ChatAnthropic(
            model="claude-3-sonnet-20240229",
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            api_key=api_key
        )

    def generate_sql(self, prompt: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
        
        messages = [
            SystemMessage(content="You are an expert SQL assistant. Return ONLY the SQL query, nothing else."),
        ]
        
        if history:
            for msg in history:
                if msg['role'] == 'user':
                    messages.append(HumanMessage(content=msg['content']))
                elif msg['role'] == 'assistant':
                    messages.append(AIMessage(content=msg['content']))
                    
        messages.append(HumanMessage(content=prompt))
        
        response = self.llm.invoke(messages)
        return response.content.strip()

    def explain_sql(self, sql: str, question: str) -> str:
        from langchain_core.messages import SystemMessage, HumanMessage
        
        messages = [
            SystemMessage(content="You are a helpful data analyst. Explain the SQL query in simple terms."),
            HumanMessage(content=f"Question: {question}\nSQL: {sql}\n\nExplain:")
        ]
        response = self.llm.invoke(messages)
        return response.content.strip()


class LocalLLMClient(LLMClient):
    """Client for locally hosted models (Llama-3, Gemma)."""
    
    def __init__(self, model_path: str = None):
        # In a real implementation, this would load the model using transformers/unsloth
        # For now, we mock the local execution or connect to a local inference server
        self.model_path = model_path

    def generate_sql(self, prompt: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        # Mocking local generation for now
        return "SELECT * FROM sales LIMIT 10; -- Local Model Generation"

    def explain_sql(self, sql: str, question: str) -> str:
        return "Explanation generated by local model."


class OllamaLLMClient(LLMClient):
    """Client for Ollama (local LLM)."""
    
    def __init__(self, model: str = "llama3"):
        self.model = model
        self.base_url = "http://localhost:11434/api/generate"

    def generate_sql(self, prompt: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        import requests
        import json
        
        system_prompt = "You are an expert SQL assistant. Return ONLY the SQL query, nothing else. Do not use markdown formatting."
        
        context_str = ""
        if history:
            for msg in history:
                context_str += f"{msg['role']}: {msg['content']}\n"
        
        full_prompt = f"{system_prompt}\n\n{context_str}\nuser: {prompt}"
        
        try:
            response = requests.post(
                self.base_url,
                json={"model": self.model, "prompt": full_prompt, "stream": False},
                timeout=30
            )
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except Exception as e:
            return f"-- Error generating SQL with Ollama: {str(e)}"

    def explain_sql(self, sql: str, question: str) -> str:
        import requests
        
        prompt = f"Explain this SQL query for the question '{question}': {sql}"
        
        try:
            response = requests.post(
                self.base_url,
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=30
            )
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except Exception as e:
            return f"Error explaining SQL with Ollama: {str(e)}"


class VLLMClient(LLMClient):
    """Client for vLLM (high-performance local LLM serving)."""
    
    def __init__(self):
        # vLLM is OpenAI-compatible
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
        
        self.llm = ChatOpenAI(
            model=settings.MODEL_NAME or "meta-llama/Meta-Llama-3-8B-Instruct",
            openai_api_key="EMPTY",
            openai_api_base="http://localhost:8000/v1",
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
        )
        self._SystemMessage = SystemMessage
        self._HumanMessage = HumanMessage
        self._AIMessage = AIMessage

    def generate_sql(self, prompt: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        messages = [
            self._SystemMessage(content="You are an expert SQL assistant. Return ONLY the SQL query, nothing else. Do not use markdown formatting.")
        ]
        
        if history:
            for msg in history:
                if msg['role'] == 'user':
                    messages.append(self._HumanMessage(content=msg['content']))
                elif msg['role'] == 'assistant':
                    messages.append(self._AIMessage(content=msg['content']))
        
        messages.append(self._HumanMessage(content=prompt))
        
        response = self.llm.invoke(messages)
        return response.content.strip()

    def explain_sql(self, sql: str, question: str) -> str:
        messages = [
            self._SystemMessage(content="You are a helpful data analyst. Explain the SQL query in simple terms."),
            self._HumanMessage(content=f"Question: {question}\nSQL: {sql}\n\nExplain this query:")
        ]
        response = self.llm.invoke(messages)
        return response.content.strip()


class LLMClientFactory:
    """Factory for creating LLM clients."""
    
    @staticmethod
    def create(provider: str, api_key: Optional[str] = None, model_path: Optional[str] = None) -> LLMClient:
        provider = provider.lower()
        
        if provider == "openai":
            return OpenAILLMClient()
        elif provider == "anthropic":
            return AnthropicLLMClient()
        elif provider == "ollama":
            return OllamaLLMClient(model=model_path or "llama3")
        elif provider == "vllm":
            return VLLMClient()
        elif provider == "local":
            return LocalLLMClient(model_path)
        elif provider == "mock":
            return MockLLMClient()
        else:
            return MockLLMClient()

def get_llm_client() -> LLMClient:
    """Legacy factory function wrapper."""
    return LLMClientFactory.create(settings.LLM_PROVIDER)
