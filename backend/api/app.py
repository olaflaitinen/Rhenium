from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config.settings import settings
from backend.api.routes import router as api_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="LLM-based DBMS",
        description="Natural Language Interface for Database Management",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins for development
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(api_router)

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.api.app:app", host=settings.API_HOST, port=settings.API_PORT, reload=settings.DEBUG)
