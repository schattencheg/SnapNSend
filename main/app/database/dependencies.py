from contextlib import asynccontextmanager
from fastapi import HTTPException
import aioredis
import aio_pika
from .core.config import settings


# Global instances for external services
_redis_client = None
_rabbitmq_connection = None


async def get_redis_client():
    """Dependency to get Redis client"""
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.from_url(settings.redis_url)
    return _redis_client


async def get_rabbitmq_connection():
    """Dependency to get RabbitMQ connection"""
    global _rabbitmq_connection
    if _rabbitmq_connection is None:
        _rabbitmq_connection = await aio_pika.connect_robust(
            settings.rabbitmq_url
        )
    return _rabbitmq_connection


# Example of how to use these dependencies in endpoints
async def get_db_session():  # Placeholder for database session
    """Placeholder for database session dependency"""
    try:
        # In a real implementation, you would yield a database session
        yield None
    except Exception as e:
        # Handle database session errors
        raise HTTPException(
            status_code=500, detail=f"Database error: {str(e)}"
        )


# Context manager for managing external service lifecycle
@asynccontextmanager
async def lifespan_services(app):
    """Manage the lifecycle of external services"""
    redis_client = None
    rabbitmq_conn = None

    try:
        # Initialize services
        redis_client = await get_redis_client()
        rabbitmq_conn = await get_rabbitmq_connection()

        yield {"redis": redis_client, "rabbitmq": rabbitmq_conn}
    finally:
        # Cleanup services
        if redis_client:
            await redis_client.close()
        if rabbitmq_conn:
            await rabbitmq_conn.close()
