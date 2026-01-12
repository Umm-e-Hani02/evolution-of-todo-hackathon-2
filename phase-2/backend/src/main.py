"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from src.core.config import settings
from src.core.database import init_db, get_db
from src.api import auth, todos

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
    cors_origins = [origin.strip() for origin in cors_origins_input.split(",") if origin.strip()]

print(f"Final CORS origins: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],  # Explicitly include OPTIONS
    allow_headers=["*"],
    # Expose headers that browsers can access
    expose_headers=["Access-Control-Allow-Origin", "Access-Control-Allow-Credentials"]
)

# Include routers
print("Including auth router...")
app.include_router(auth.router)
print("Including todos router...")
app.include_router(todos.router)
print("Routers included successfully")


@app.get("/health", tags=["Health"])
def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/ready", tags=["Health"])
def readiness_check(db: Session = Depends(get_db)) -> dict:
    """Readiness check endpoint that verifies database connectivity."""
    try:
        # Test database connectivity
        db.execute("SELECT 1")
        return {"status": "ready", "database": "connected", "version": "1.0.0"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database not ready: {str(e)}")


@app.get("/", tags=["Root"])
def root() -> dict:
    """Root endpoint with API information."""
    return {
        "name": "Todo API - Phase II",
        "version": "1.0.0",
        "docs": "/docs",
    }
