import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .api.routes import router as api_router
from .core.config import settings


# Configure logging based on environment
logging.basicConfig(level=getattr(logging, settings.log_level.upper()))
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for startup and shutdown events.
    This is where you would initialize connections to databases,
    message brokers, etc.
    """
    logger.info(f"Starting up {settings.app_name} (Environment: {os.getenv('ENVIRONMENT', 'development')})...")

    # Startup logic here
    # - Initialize Redis connection
    # - Initialize RabbitMQ connection
    # - Initialize database connections
    logger.info(f"Connecting to Redis at {settings.redis_url}")
    logger.info(f"Connecting to RabbitMQ at {settings.rabbitmq_url}")

    yield  # Application runs here

    # Shutdown logic here
    # - Close Redis connection
    # - Close RabbitMQ connection
    # - Close database connections
    logger.info("Shutting down SnapNSend API...")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(
        api_router,
        prefix=settings.api_v1_prefix,
        tags=["requests"]
    )

    return app


# Create the main application instance
app = create_app()


@app.get("/")
async def root():
    """Root endpoint for basic service info"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "environment": os.getenv("ENVIRONMENT", "development"),
        "status": "running",
        "debug": settings.debug
    }

