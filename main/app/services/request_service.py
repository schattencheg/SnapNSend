import asyncio
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from ..schemas import (
    SearchRequest, SearchResponse, RegisterRequest, RegisterResponse
)
from ..models.user import User
from ..utils.email_service import email_service
from ..db.database import DatabaseManager
from ..ai.image_downloader import PerplexityImageDownloader


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
        # Initialize database manager for persistent user storage
        self.db_manager = DatabaseManager()

    async def register_user(
        self, register_request: RegisterRequest
    ) -> RegisterResponse:
        """
        Register a new user and store in local DB

        Args:
            register_request: Contains user_name and user_mail

        Returns:
            RegisterResponse: Contains the user UUID and status
        """
        # Check if user with email already exists
        if self.db_manager.user_exists_with_email(register_request.user_mail):
            return RegisterResponse(
                user_id=UUID(int=0),  # Return a zero UUID to indicate error
                status="error",
                error=(
                    f"User with email {register_request.user_mail} "
                    f"already exists"
                )
            )

        # Check if user with username already exists
        if self.db_manager.user_exists_with_username(
            register_request.user_name
        ):
            return RegisterResponse(
                user_id=UUID(int=0),  # Return a zero UUID to indicate error
                status="error",
                error=(
                    f"User with username {register_request.user_name} "
                    f"already exists"
                )
            )

        user_id = uuid4()

        # Create user object
        user = User(
            id=user_id,
            user_name=register_request.user_name,
            user_mail=register_request.user_mail,
            created_at=datetime.utcnow()
        )

        # Store user in local DB
        success = self.db_manager.create_user(user)
        if not success:
            # This shouldn't happen if the checks above passed, but just in
            # case
            return RegisterResponse(
                user_id=UUID(int=0),  # Return a zero UUID to indicate error
                status="error",
                error="Failed to create user in database"
            )

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

    async def create_request(
        self, request_data: SearchRequest
    ) -> SearchResponse:
        """Create a new request and process image download and email sending"""
        request_id = uuid4()

        # Validate that the user exists in the database
        if request_data.user is None:
            # If no user ID provided, return unauthorized
            return SearchResponse(
                request_id=request_id,
                status="error",
                images=[],
                error="Unauthorized: No user ID provided"
            )

        # Check if the user exists in the database
        user = self.db_manager.get_user_by_id(str(request_data.user))
        if not user:
            # Return unauthorized response if user doesn't exist
            return SearchResponse(
                request_id=request_id,
                status="error",
                images=[],
                error=f"Unauthorized: User with ID {request_data.user} does not exist in the database"
            )

        # Create initial request with pending status
        request = SearchResponse(
            request_id=request_id,
            status="processing",  # Changed to processing while images are being downloaded
            images=[],
            error=None
        )
        self._requests[request_id] = request

        try:
            # Use the image downloader to get images based on the prompt
            async with PerplexityImageDownloader() as image_downloader:
                image_paths = await image_downloader.search_and_download_images(
                    query=request_data.prompt,
                    num_images=10,  # Request 10 images as specified
                    user_name=user.user_name,
                    request_id=str(request_id)
                )

            # Update the request with the downloaded images
            request.images = image_paths
            request.status = "done"

            # Send the images to the user's email
            email_sent = await self._send_images_to_user_email(user, image_paths, request_data.prompt)

            if not email_sent:
                request.status = "done_with_errors"
                if request.error:
                    request.error += "; Failed to send email"
                else:
                    request.error = "Failed to send email"

        except Exception as e:
            # Handle any errors during image download
            request.status = "error"
            request.error = f"Error processing images: {str(e)}"
            print(f"Error in create_request: {str(e)}")

        # Update the stored request with final status
        self._requests[request_id] = request
        return request

    async def _send_images_to_user_email(self, user: User, image_paths: List[str], prompt: str):
        """
        Send the downloaded images to the user's email address.

        Args:
            user: The user object containing email information
            image_paths: List of file paths to the downloaded images
            prompt: The original prompt used to generate the images

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            # Send email with images attached
            email_sent = await email_service.send_images_email(
                user_name=user.user_name,
                user_mail=user.user_mail,
                image_paths=image_paths,
                prompt=prompt
            )
            return email_sent
        except Exception as e:
            print(f"Error sending email to {user.user_mail}: {str(e)}")
            return False

    async def get_request(self, request_id: UUID) -> Optional[SearchResponse]:
        """Get a request by ID"""
        return self._requests.get(request_id)

    async def list_requests(self) -> List[SearchResponse]:
        """List all requests"""
        return list(self._requests.values())


# Global request service instance
request_service = RequestService()
