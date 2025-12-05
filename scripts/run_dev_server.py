"""
Development server startup script.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import uvicorn
from backend.config.settings import settings

if __name__ == "__main__":
    print("=" * 70)
    print("LLM-based DBMS v1.0 - Development Server")
    print("=" * 70)
    print()
    print(f"🚀 Starting server...")
    print(f"   Environment: {settings.ENVIRONMENT}")
    print(f"   API URL: http://{settings.API_HOST}:{settings.API_PORT}")
    print(f"   API Docs: http://{settings.API_HOST}:{settings.API_PORT}/docs")
    print(f"   Database: {settings.DATABASE_TYPE}")
    print(f"   LLM Provider: {settings.LLM_PROVIDER}")
    print()
    print("Press CTRL+C to stop")
    print("=" * 70)
    print()
    
    uvicorn.run(
        "backend.api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
