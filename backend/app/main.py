from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.db.session import engine, Base
from app.models import all_models  # Ensures all models are registered
from app.api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Agentic AI assistant platform that plans multi-step tasks, uses connected tools, enforces human approvals, and delivers verified results.",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Secure logging without leaking sensitive stack traces
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected server error occurred. Please try again or inspect system logs."}
    )


@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "HEALTHY",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "llm_provider": settings.LLM_PROVIDER,
        "database": "sqlite_fallback" if "sqlite" in settings.DATABASE_URL else "postgresql",
        "demo_mode": settings.DEMO_MODE,
        "simulated_alexa_mode": settings.SIMULATED_ALEXA_MODE
    }


@app.get("/", tags=["System"])
def root():
    return {
        "message": "Welcome to ContextPilot AI API. Navigate to /docs for the interactive Swagger OpenAPI documentation.",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }


app.include_router(api_router, prefix=settings.API_V1_STR)
