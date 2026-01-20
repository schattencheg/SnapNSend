from pydantic_settings import BaseSettings
from typing import Optional, List
import os
from pydantic import ConfigDict


class BaseSettings(BaseSettings):
    """Base settings shared across all environments"""

    # Application settings
    app_name: str = "SnapNSend API"
    app_version: str = "1.0.0"

    # API settings
    api_v1_prefix: str = "/v1"
    debug: bool = False

    # Database settings
    redis_url: str = "redis://localhost:6379"

    # Message broker settings
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"

    # Email/SMTP settings
    smtp_server: str = "localhost"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""

    # CORS settings
    allowed_origins: List[str] = ["*"]

    # Logging
    log_level: str = "INFO"

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"  # This allows extra fields in .env files
    )


class DevelopmentSettings(BaseSettings):
    """Development environment settings"""

    # Application settings
    debug: bool = True

    # Logging
    log_level: str = "DEBUG"

    model_config = ConfigDict(
        env_file=".env.dev",
        case_sensitive=False,
        extra="ignore"
    )


class ProductionSettings(BaseSettings):
    """Production environment settings"""

    # Application settings
    debug: bool = False

    # Database settings
    redis_url: str = "redis://redis:6379"

    # Message broker settings
    rabbitmq_url: str = "amqp://rabbitmq:5672"

    # Logging
    log_level: str = "INFO"

    model_config = ConfigDict(
        env_file=".env.prod",
        case_sensitive=False,
        extra="ignore"
    )


class TestingSettings(BaseSettings):
    """Testing environment settings"""

    # Application settings
    debug: bool = True
    testing: bool = True

    # Logging
    log_level: str = "WARNING"

    model_config = ConfigDict(
        env_file=".env.test",
        case_sensitive=False,
        extra="ignore"
    )


def get_settings():
    """Factory function to get settings based on environment"""
    env = os.getenv("ENVIRONMENT", "development").lower()

    if env == "production":
        return ProductionSettings()
    elif env == "testing":
        return TestingSettings()
    else:  # default to development
        return DevelopmentSettings()


# Global settings instance
settings = get_settings()