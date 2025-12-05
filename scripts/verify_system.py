"""
System Verification Script

Checks the environment, dependencies, and configuration to ensure the system is ready to run.
"""
import sys
import os
import importlib.util
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

def check_python_version():
    print("Checking Python version...", end=" ")
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ is required.")
        return False
    print(f"✅ {sys.version.split()[0]}")
    return True

def check_dependencies():
    print("\nChecking core dependencies...")
    dependencies = [
        "fastapi", "uvicorn", "pydantic", "sqlalchemy", 
        "alembic", "jose", "passlib", "langchain", "structlog"
    ]
    
    all_ok = True
    for dep in dependencies:
        print(f"  - {dep:<15}", end=" ")
        if importlib.util.find_spec(dep) is not None:
            print("✅ Found")
        else:
            # Handle package name differences
            if dep == "jose" and importlib.util.find_spec("jose"):
                print("✅ Found")
            elif dep == "passlib" and importlib.util.find_spec("passlib"):
                print("✅ Found")
            else:
                print("❌ Missing")
                all_ok = False
    return all_ok

def check_configuration():
    print("\nChecking configuration...")
    
    # Check .env
    env_path = project_root / ".env"
    if env_path.exists():
        print("  - .env file:      ✅ Found")
    else:
        print("  - .env file:      ⚠️  Not found (using defaults)")
        
    # Load settings
    try:
        from backend.config.settings import settings
        print(f"  - Environment:    ✅ {settings.ENVIRONMENT}")
        print(f"  - Database Type:  ✅ {settings.DATABASE_TYPE}")
        print(f"  - LLM Provider:   ✅ {settings.LLM_PROVIDER}")
        return True
    except Exception as e:
        print(f"  - Settings load:  ❌ Failed ({e})")
        return False

def check_database():
    print("\nChecking database...")
    from backend.config.settings import settings
    
    if settings.DATABASE_TYPE == "sqlite":
        db_path = project_root / settings.SQLITE_DB_PATH
        if db_path.exists():
            print(f"  - SQLite file:    ✅ Found ({db_path.name})")
            size_mb = db_path.stat().st_size / (1024 * 1024)
            print(f"  - Size:           ℹ️  {size_mb:.2f} MB")
        else:
            print(f"  - SQLite file:    ❌ Not found at {settings.SQLITE_DB_PATH}")
            print("    Run 'python scripts/init_db.py' to create it.")
            return False
            
    # Try connection
    try:
        from backend.database.connection import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("  - Connection:     ✅ Successful")
            
            # Check tables
            if settings.DATABASE_TYPE == "sqlite":
                tables = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'")).fetchall()
                table_names = [t[0] for t in tables]
                required = ['users', 'sales']
                missing = [t for t in required if t not in table_names]
                
                if not missing:
                    print(f"  - Tables:         ✅ Found {len(table_names)} tables")
                else:
                    print(f"  - Tables:         ❌ Missing {missing}")
                    return False
                    
        return True
    except Exception as e:
        print(f"  - Connection:     ❌ Failed ({e})")
        return False

def main():
    print("=" * 60)
    print("LLM-Based DBMS - System Verification")
    print("=" * 60)
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_configuration(),
        check_database()
    ]
    
    print("\n" + "=" * 60)
    if all(checks):
        print("✅ System is ready to run!")
        print("   Start server with: python scripts/run_dev_server.py")
        return 0
    else:
        print("❌ System verification failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
