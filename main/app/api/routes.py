from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from ..schemas import RegisterRequest, RegisterResponse, SearchRequest, SearchResponse, HealthCheck
from ..services.request_service import request_service
from datetime import datetime


router = APIRouter()


@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint to verify the service is running"""
    return HealthCheck(timestamp=datetime.utcnow())


@router.post("/requests", response_model=SearchResponse, status_code=status.HTTP_201_CREATED)
async def create_request(request: SearchRequest):
    """Create a new request"""
    return await request_service.create_request(request)


@router.get("/requests/{request_id}", response_model=SearchResponse)
async def get_request(request_id: UUID):
    """Get a request by ID"""
    request = await request_service.get_request(request_id)
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found"
        )
    return request


@router.get("/requests", response_model=List[SearchResponse])
async def list_requests():
    """List all requests"""
    return await request_service.list_requests()


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest):
    """Register new user"""
    return await request_service.register_user(request)


@router.post("/request_by_email", response_model=SearchResponse, status_code=status.HTTP_201_CREATED)
async def create_request_by_email(request: SearchRequest):
    """Create a new request by email"""
    return await request_service.create_request(request)
