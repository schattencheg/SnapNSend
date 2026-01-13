import asyncio
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from ..schemas import RequestCreate, RequestUpdate, RequestResponse


class RequestService:
    """
    Service class for handling request business logic.
    In a real implementation, this would interact with a database,
    message queues, and other external services.
    """

    def __init__(self):
        # In-memory storage for demonstration purposes
        # In production, this would be replaced with a database
        self._requests = {}

    async def create_request(self, request_data: RequestCreate) -> RequestResponse:
        """Create a new request"""
        request_id = uuid4()

        request = RequestResponse(
            id=request_id,
            customer_id=request_data.customer_id,
            items=request_data.items,
            total_amount=request_data.total_amount,
            status=request_data.status,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self._requests[request_id] = request
        return request

    async def get_request(self, request_id: UUID) -> Optional[RequestResponse]:
        """Get a request by ID"""
        return self._requests.get(request_id)

    async def list_requests(self) -> List[RequestResponse]:
        """List all requests"""
        return list(self._requests.values())

    async def update_request(self, request_id: UUID, request_update: RequestUpdate) -> Optional[RequestResponse]:
        """Update an existing request"""
        if request_id not in self._requests:
            return None

        request = self._requests[request_id]
        update_data = request_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(request, field, value)

        request.updated_at = datetime.utcnow()
        self._requests[request_id] = request
        return request


# Global request service instance
request_service = RequestService()