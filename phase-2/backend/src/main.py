"""FastAPI application entry point with fixed CORS for Vercel and localhost."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from src.core.config import settings
from src.core.database import init_db, get_db
from src.api import auth, todos
from src.models import User, TodoTask

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    try:
        init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise
    yield

# Create FastAPI application
print("Creating FastAPI application...")
app = FastAPI(
    title="Todo API - Phase II",
    description="REST API for multi-user todo application with JWT authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)
print("FastAPI application created successfully")

# Configure CORS with validation
cors_origins_input = settings.cors_origins
print(f"Raw CORS origins from settings: {cors_origins_input}")

if not cors_origins_input or len(cors_origins_input.strip()) == 0:
    print("WARNING: CORS_ORIGINS is empty, using safe default")
    cors_origins = ["http://localhost:3000"]
else:
    # Split and clean origins
    cors_origins = [origin.strip() for origin in cors_origins_input.split(",")]

print(f"Final CORS origins: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,        # exact match domains
    allow_credentials=True,
    allow_methods=["*"],               # allow all methods including OPTIONS
    allow_headers=["*"],               # allow all headers
)

# Include routers
print("Including auth router...")
app.include_router(auth.router)
print("Including todos router...")
app.include_router(todos.router)
print("Routers included successfully")

# Health check endpoints
@app.get("/health", tags=["Health"])
def health_check() -> dict:
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/ready", tags=["Health"])
def readiness_check(db: Session = Depends(get_db)) -> dict:
    try:
        db.execute("SELECT 1")
        return {"status": "ready", "database": "connected", "version": "1.0.0"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database not ready: {str(e)}")

# Root endpoint
@app.get("/", tags=["Root"])
def root() -> dict:
    return {
        "name": "Todo API - Phase II",
        "version": "1.0.0",
        "docs": "/docs",
    }
