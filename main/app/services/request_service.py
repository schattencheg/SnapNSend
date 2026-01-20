import asyncio
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from ..schemas import SearchRequest, SearchResponse, RegisterRequest, RegisterResponse
from ..models.user import User
from ..utils.email_service import email_service


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
        # Storage for user data
        self._users: dict[UUID, User] = {}

    async def register_user(self, register_request: RegisterRequest) -> RegisterResponse:
        """
        Register a new user and store in local DB

        Args:
            register_request: Contains user_name and user_mail

        Returns:
            RegisterResponse: Contains the user UUID and status
        """
        # Check if user with email already exists
        if register_request.user_mail in [x.user_mail for x in self._users.values()]:
            raise ValueError(f"User with email {register_request.user_mail} already exists")

        # Check if user with username already exists
        if register_request.user_name in [x.user_name for x in self._users.values()]:
            raise ValueError(f"User with username {register_request.user_name} already exists")

        user_id = uuid4()

        # Create user object
        user = User(
            id=user_id,
            user_name=register_request.user_name,
            user_mail=register_request.user_mail,
            created_at=datetime.utcnow()
        )

        # Store user in local DB (simulated with in-memory storage)
        self._users[user_id] = user

        # Send registration email to the user
        email_sent = await email_service.send_registration_email(
            user_name=register_request.user_name,
            user_mail=register_request.user_mail,
            user_uuid=str(user_id)
        )

        # Determine status based on email sending success
        status = "done" if email_sent else "error"

        # Return the user UUID as requested
        return RegisterResponse(
            user_id=user_id,  # Using request_id field to return user UUID
            status=status
        )

    async def create_request(self, request_data: SearchRequest) -> SearchResponse:
        """Create a new request"""
        request_id = uuid4()

        # Validate that the user exists if a user ID is provided
        if request_data.user != -1:  # Assuming -1 means no user specified
            if request_data.user not in self._users:
                raise ValueError(f"User with ID {request_data.user} does not exist")

        request = SearchResponse(
            request_id=request_id,
            status="pending",  # Default status for new requests
            images=[],  # Empty initially
            error=None
        )

        self._requests[request_id] = request
        return request

    async def get_request(self, request_id: UUID) -> Optional[SearchResponse]:
        """Get a request by ID"""
        return self._requests.get(request_id)

    async def list_requests(self) -> List[SearchResponse]:
        """List all requests"""
        return list(self._requests.values())


# Global request service instance
request_service = RequestService()