"""
Enhanced LLM client with multi-provider support.
"""
from abc import ABC, abstractmethod
from typing import Optional

from backend.config.settings import settings


class LLMClient(ABC):
    """Abstract base class for LLM clients."""
    
    @abstractmethod
    def generate_sql(self, prompt: str) -> str:
        """Generate SQL from a natural language prompt."""
        pass

    @abstractmethod
    def explain_sql(self, sql: str, question: str) -> str:
        """Explain a generated SQL query."""
        pass


class MockLLMClient(LLMClient):
    """Mock LLM client for testing and development without API keys."""
    
    def generate_sql(self, prompt: str) -> str:
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
        from langchain_core.messages import SystemMessage, HumanMessage
        
        self.llm = ChatOpenAI(
            model=settings.MODEL_NAME,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            api_key=api_key
        )
        self._SystemMessage = SystemMessage
        self._HumanMessage = HumanMessage

    def generate_sql(self, prompt: str) -> str:
        messages = [
            self._SystemMessage(content="You are an expert SQL assistant. Return ONLY the SQL query, nothing else. Do not use markdown formatting."),
            self._HumanMessage(content=prompt)
        ]
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

    def generate_sql(self, prompt: str) -> str:
        from langchain_core.messages import SystemMessage, HumanMessage
        
        messages = [
            SystemMessage(content="You are an expert SQL assistant. Return ONLY the SQL query, nothing else."),
            HumanMessage(content=prompt)
        ]
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


def get_llm_client() -> LLMClient:
    """
    Factory function to get the configured LLM client.
    
    Returns:
        LLMClient instance based on settings.LLM_PROVIDER
    """
    provider = settings.LLM_PROVIDER.lower()
    
    if provider == "openai":
        return OpenAILLMClient()
    elif provider == "anthropic":
        return AnthropicLLMClient()
    elif provider == "mock":
        return MockLLMClient()
    else:
        # Default to mock for unknown providers
        return MockLLMClient()
