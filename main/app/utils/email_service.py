import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Service class for handling email operations"""
    
    def __init__(self):
        # In a real implementation, you would load SMTP settings from config
        # For now, we'll simulate email sending
        pass
    
    async def send_registration_email(self, user_name: str, user_mail: str, user_uuid: str) -> bool:
        """
        Send registration confirmation email to the user
        
        Args:
            user_name: Name of the user
            user_mail: Email address of the user
            user_uuid: UUID assigned to the user
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            # In a real implementation, you would connect to an SMTP server
            # and send the actual email. For now, we'll simulate it.
            
            subject = "Welcome to SnapNSend - Registration Confirmation"
            body = f"""
            Hello {user_name},
            
            Thank you for registering with SnapNSend!
            
            Your account has been successfully created with the following details:
            - User Name: {user_name}
            - User Email: {user_mail}
            - User ID: {user_uuid}
            
            You can now start using our services. If you have any questions, feel free to contact us.
            
            Best regards,
            The SnapNSend Team
            """
            

            # Create and send the email
            msg = MIMEMultipart()
            msg['From'] = settings.smtp_username  # Use the email from environment
            msg['To'] = user_mail
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL(settings.smtp_server, settings.smtp_port, context=context) as server:
                server.login(settings.smtp_username, settings.smtp_password)
                server.send_message(msg)
            
            # Log the email for debugging purposes (in a real app, this would be actual email sending)
            logger.info(f"Registration email sent to {user_mail} for user {user_name} with UUID {user_uuid}")
            return True
        except Exception as e:
            logger.error(f"Failed to send registration email to {user_mail}: {str(e)}")
            return False


# Global email service instance
email_service = EmailService()