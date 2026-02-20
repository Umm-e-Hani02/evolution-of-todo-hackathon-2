"""FastAPI application entry point for Phase-3 AI Chatbot."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.database import init_db
from .api import auth, todos
from .api.chat import router as chat_router


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


# Create FastAPI application - matches Phase-2 structure
print("Creating FastAPI application for Phase-3...")
app = FastAPI(
    title="Todo AI Chatbot API - Phase III",
    description="AI-powered chatbot API for multi-user todo application with conversation history",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)
print("FastAPI application created successfully")


# Configure CORS - matches Phase-2 pattern
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
print("Including auth router...")
app.include_router(auth.router)
print("Including todos router...")
app.include_router(todos.router)
print("Including chat router...")
app.include_router(chat_router)
print("Routers included successfully")


@app.get("/health", tags=["Health"])
def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "version": "3.0.0", "service": "Phase-3 AI Chatbot"}


@app.get("/", tags=["Root"])
def root() -> dict:
    """Root endpoint with API information."""
    return {
        "name": "Todo AI Chatbot API - Phase III",
        "version": "3.0.0",
        "description": "AI-powered chatbot for todo management",
        "docs": "/docs",
        "chat_endpoint": "/api/chat"
    }