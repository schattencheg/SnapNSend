# SnapNSend API

A FastAPI-based microservice for request processing with Redis and RabbitMQ integration.

## Project Structure

```
app/
├── main.py                 # Main FastAPI application
├── api/
│   └── routes.py           # API route definitions
├── schemas.py              # Pydantic models for request/response validation
├── core/
│   └── config.py           # Configuration and settings
├── services/
│   └── request_service.py    # Business logic layer
├── database/
│   └── dependencies.py     # Dependency injection for external services
└── utils/                  # Utility functions
```

## Features

- Health check endpoint
- Request management (CRUD operations)
- Configuration via environment variables
- Dependency injection for external services
- Proper separation of concerns (API, business logic, data models)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy the `.env.example` to `.env` and adjust settings:
```bash
cp .env.example .env
```

3. Run the application:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Environment Variables

- `APP_NAME`: Name of the application
- `APP_VERSION`: Version of the application
- `DEBUG`: Enable/disable debug mode
- `API_V1_PREFIX`: API version prefix (default: /v1)
- `REDIS_URL`: Redis connection URL
- `RABBITMQ_URL`: RabbitMQ connection URL
- `ALLOWED_ORIGINS`: List of allowed origins for CORS

## Endpoints

- `GET /` - Root endpoint with service info
- `GET /v1/health` - Health check
- `POST /v1/requests` - Create a new request
- `GET /v1/requests/{id}` - Get a request by ID
- `GET /v1/requests` - List all requests
- `PUT /v1/requests/{id}` - Update a request

## Development

To run in development mode with auto-reload:
```bash
uvicorn app.main:app --reload
```

## Production

For production deployment, use:
```bash
uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000
```

Or use a process manager like gunicorn:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```