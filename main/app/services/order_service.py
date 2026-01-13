import asyncio
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from ..schemas import OrderCreate, OrderUpdate, OrderResponse


class OrderService:
    """
    Service class for handling order business logic.
    In a real implementation, this would interact with a database,
    message queues, and other external services.
    """
    
    def __init__(self):
        # In-memory storage for demonstration purposes
        # In production, this would be replaced with a database
        self._orders = {}
    
    async def create_order(self, order_data: OrderCreate) -> OrderResponse:
        """Create a new order"""
        order_id = uuid4()
        
        order = OrderResponse(
            id=order_id,
            customer_id=order_data.customer_id,
            items=order_data.items,
            total_amount=order_data.total_amount,
            status=order_data.status,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        self._orders[order_id] = order
        return order
    
    async def get_order(self, order_id: UUID) -> Optional[OrderResponse]:
        """Get an order by ID"""
        return self._orders.get(order_id)
    
    async def list_orders(self) -> List[OrderResponse]:
        """List all orders"""
        return list(self._orders.values())
    
    async def update_order(self, order_id: UUID, order_update: OrderUpdate) -> Optional[OrderResponse]:
        """Update an existing order"""
        if order_id not in self._orders:
            return None
        
        order = self._orders[order_id]
        update_data = order_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(order, field, value)
        
        order.updated_at = datetime.utcnow()
        self._orders[order_id] = order
        return order


# Global order service instance
order_service = OrderService()