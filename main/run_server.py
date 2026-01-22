#!/usr/bin/env python
"""
Simple script to run the SnapNSend API server.
This bypasses potential uvicorn command-line issues.
"""

import asyncio
import sys
from contextlib import redirect_stdout, redirect_stderr
import io

from app.main import app

def run_with_uvicorn_programmatically():
    """Run the application using uvicorn programmatically"""
    try:
        import uvicorn
        
        # Try to run on a higher port that might not be restricted
        config = uvicorn.Config(
            app,
            host="127.0.0.1",
            port=9000,  # Try a higher port
            log_level="info"
        )
        server = uvicorn.Server(config)
        
        print("Starting server on http://127.0.0.1:9000")
        print("Press Ctrl+C to stop the server")
        
        # Run the server
        import signal
        import threading
        
        def signal_handler(sig, frame):
            print("\nShutting down server...")
            server.should_exit = True
            
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        import uvicorn.platform
        uvicorn.platform.ACTIVE = True
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(server.serve())
        except KeyboardInterrupt:
            print("Server stopped by user")
            
    except ImportError:
        print("uvicorn not available, trying alternative method...")
        run_simple_server()

def run_simple_server():
    """Alternative method using FastAPI's built-in server (if available)"""
    print("FastAPI doesn't have a built-in server, please install uvicorn:")
    print("pip install uvicorn[standard]")
    
    # Just test that the app is working
    print("Testing app import...")
    print(f"App title: {app.title}")
    print(f"App version: {app.version}")
    print("App imported successfully!")

if __name__ == "__main__":
    print("Attempting to run SnapNSend API server...")
    run_with_uvicorn_programmatically()