# SnapNSend API

SnapNSend is an API service that allows users to search for images and have them sent via email.

## Project Structure

```
main/
├── app/
│   ├── api/
│   │   └── routes.py          # API route definitions
│   ├── core/
│   │   └── config.py          # Configuration settings
│   ├── models/
│   ├── schemas/
│   ├── services/
│   │   └── request_service.py # Business logic
│   ├── utils/
│   │   └── email_service.py   # Email functionality
│   ├── ai/
│   │   └── image_downloader.py # Image downloading functionality
│   ├── db/
│   │   └── database.py        # Database management
│   ├── main.py               # Main FastAPI application
│   └── __init__.py
├── requirements.txt          # Dependencies
├── test_api.py              # API tests
├── simple_test.py           # Simple integration tests
└── start.bat                # Windows startup script
```

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
   - On Windows: Double-click `start.bat` or run from command line
   - Alternative: `uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload`

## Available Scripts

- `start.bat` - Starts the application server on port 8080 using the virtual environment
- `stop.bat` - Stops the running server process
- `kill.bat` - Lists and optionally kills Python processes
- `send_register.bat` - Sends a registration request to the server
- `send_health.bat` - Checks the health endpoint of the server
- `send_post.bat` - Sends a POST request to the server
- `send.bat` - Generic script to send POST requests to the server

## Known Issues and Solutions

### Windows Port Binding Error
If you encounter the error `[WinError 10013] An attempt was made to access a socket in a way forbidden by its access permissions`, this is due to Windows security restrictions on port binding. 

**Solutions:**
1. Run the command prompt or PowerShell as Administrator
2. Use a port number higher than 1024 (e.g., 8080, 9000)
3. Check Windows Firewall or antivirus settings for port restrictions
4. The updated start.bat file now defaults to port 8080 to avoid this issue

### Package Compatibility
The project requires specific versions of FastAPI and related packages. If you encounter TestClient errors, reinstall the packages:
```bash
pip install fastapi uvicorn[standard] --force-reinstall
```

## API Endpoints

- `GET /` - Root endpoint with service info
- `GET /v1/health` - Health check
- `POST /v1/register` - User registration
- `POST /v1/requests` - Create a new search request
- `GET /v1/requests/{request_id}` - Get a specific request
- `GET /v1/requests` - List all requests

## Testing

Run the simple tests:
```bash
python simple_test.py
```

Or run with pytest:
```bash
pytest test_api.py -v
```

Note: Tests may fail if email services are not properly configured.