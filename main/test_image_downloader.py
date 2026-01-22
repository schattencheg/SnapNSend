#!/usr/bin/env python3
"""
Test script to verify the image downloader functionality without running the full server.
This helps validate that our code changes work correctly.
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import pytest
from app.ai.image_downloader import PerplexityImageDownloader
from app.services.request_service import request_service
from app.schemas import SearchRequest
from uuid import UUID


@pytest.mark.asyncio
async def test_image_downloader():
    """Test the image downloader functionality"""
    print("Testing image downloader...")
    
    try:
        async with PerplexityImageDownloader() as downloader:
            # Test with a simple query - this will use mock URLs if no API keys are set
            images = await downloader.search_and_download_images("test query", 3, "test_user", "test_request")
            print(f"Downloaded {len(images)} images: {images}")
            return True
    except Exception as e:
        print(f"Error in image downloader test: {e}")
        return False


@pytest.mark.asyncio
async def test_request_service():
    """Test the request service functionality"""
    print("\nTesting request service...")
    
    # Create a mock UUID for testing
    try:
        # This will fail if the user doesn't exist in the database, which is expected
        request_data = SearchRequest(
            user=UUID("12345678-1234-5678-1234-567812345678"),  # Non-existent user
            n=1,
            prompt="test prompt"
        )
        
        response = await request_service.create_request(request_data)
        print(f"Request response: {response}")
        print(f"Status: {response.status}")
        print(f"Error: {response.error}")
        
        # This should return an unauthorized error since the user doesn't exist
        if "Unauthorized" in (response.error or ""):
            print("OK: Correctly returned unauthorized for non-existent user")
            return True
        else:
            print("? Unexpected response for non-existent user")
            return False
            
    except Exception as e:
        print(f"Error in request service test: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    print("Running tests for image downloader and request service...\n")
    
    # Test image downloader
    dl_success = await test_image_downloader()
    
    # Test request service
    rs_success = await test_request_service()
    
    print(f"\nResults:")
    print(f"Image Downloader Test: {'PASS' if dl_success else 'FAIL'}")
    print(f"Request Service Test: {'PASS' if rs_success else 'FAIL'}")

    if dl_success and rs_success:
        print("\nOK: All tests passed!")
        return 0
    else:
        print("\nFAILED: Some tests failed!")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)