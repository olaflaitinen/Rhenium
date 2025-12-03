"""
LLM Response Caching Module.

Provides a caching mechanism for LLM responses to reduce latency and costs.
Supports Redis as the backend.
"""
import json
import hashlib
from typing import Optional, Any
import redis
from backend.config.settings import settings

class LLMCache:
    """
    Cache for LLM responses using Redis.
    """
    def __init__(self):
        self.enabled = settings.ENABLE_LLM_CACHE
        self.redis = None
        if self.enabled:
            try:
                self.redis = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=0,
                    decode_responses=True,
                    socket_connect_timeout=1
                )
                self.redis.ping()
            except Exception as e:
                print(f"Warning: Redis cache connection failed: {e}")
                self.enabled = False

    def get(self, prompt: str, model: str) -> Optional[str]:
        """Retrieve cached response for a prompt."""
        if not self.enabled or not self.redis:
            return None
            
        key = self._generate_key(prompt, model)
        try:
            return self.redis.get(key)
        except Exception:
            return None

    def set(self, prompt: str, model: str, response: str, ttl: int = 3600):
        """Cache a response."""
        if not self.enabled or not self.redis:
            return
            
        key = self._generate_key(prompt, model)
        try:
            self.redis.setex(key, ttl, response)
        except Exception:
            pass

    def _generate_key(self, prompt: str, model: str) -> str:
        """Generate a unique cache key."""
        content = f"{model}:{prompt}"
        return f"llm_cache:{hashlib.sha256(content.encode()).hexdigest()}"

# Global cache instance
llm_cache = LLMCache()
