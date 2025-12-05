"""
Configuration Package

Application configuration management using Pydantic settings.

Features:
- Environment variable loading
- Type validation
- Default values
- Production/development modes
"""

from backend.config.settings import settings

__all__ = ['settings']
