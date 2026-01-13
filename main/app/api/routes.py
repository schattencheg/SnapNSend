from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from ..schemas import OrderCreate, OrderUpdate, OrderResponse, HealthCheck
from ..services.order_service import order_service
from datetime import datetime


router = APIRouter()


@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint to verify the service is running"""
    return HealthCheck(timestamp=datetime.utcnow())


@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    """Create a new order"""
    return await order_service.create_order(order)


@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: UUID):
    """Get an order by ID"""
    order = await order_service.get_order(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order


@router.get("/orders", response_model=List[OrderResponse])
async def list_orders():
    """List all orders"""
    return await order_service.list_orders()


@router.put("/orders/{order_id}", response_model=OrderResponse)
async def update_order(order_id: UUID, order_update: OrderUpdate):
    """Update an existing order"""
    updated_order = await order_service.update_order(order_id, order_update)
    if not updated_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return updated_order