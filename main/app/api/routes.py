from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from ..schemas import RequestCreate, RequestUpdate, RequestResponse, HealthCheck
from ..services.request_service import request_service
from datetime import datetime


router = APIRouter()


@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint to verify the service is running"""
    return HealthCheck(timestamp=datetime.utcnow())


@router.post("/requests", response_model=RequestResponse, status_code=status.HTTP_201_CREATED)
async def create_request(request: RequestCreate):
    """Create a new request"""
    return await request_service.create_request(request)


@router.get("/requests/{request_id}", response_model=RequestResponse)
async def get_request(request_id: UUID):
    """Get a request by ID"""
    request = await request_service.get_request(request_id)
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found"
        )
    return request


@router.get("/requests", response_model=List[RequestResponse])
async def list_requests():
    """List all requests"""
    return await request_service.list_requests()


@router.put("/requests/{request_id}", response_model=RequestResponse)
async def update_request(request_id: UUID, request_update: RequestUpdate):
    """Update an existing request"""
    updated_request = await request_service.update_request(request_id, request_update)
    if not updated_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found"
        )
    return updated_request