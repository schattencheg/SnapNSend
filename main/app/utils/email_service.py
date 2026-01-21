import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Service class for handling email operations"""

    def __init__(self):
        # In a real implementation, you would load SMTP settings from config
        # For now, we'll simulate email sending
        pass

    async def send_registration_email(
        self, user_name: str, user_mail: str, user_uuid: str
    ) -> bool:
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

            Your account has been successfully created with the following
            details:
            - User Name: {user_name}
            - User Email: {user_mail}
            - User ID: {user_uuid}

            You can now start using our services. If you have any questions,
            feel free to contact us.

            Best regards,
            The SnapNSend Team
            """

            # Create and send the email
            msg = MIMEMultipart()
            msg['From'] = settings.smtp_username  # Use the email from
            # environment
            msg['To'] = user_mail
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL(
                settings.smtp_server, settings.smtp_port, context=context
            ) as server:
                server.login(settings.smtp_username, settings.smtp_password)
                server.send_message(msg)

            # Log the email for debugging purposes (in a real app, this would
            # be actual email sending)
            logger.info(
                f"Registration email sent to {user_mail} for user {user_name} "
                f"with UUID {user_uuid}"
            )
            return True
        except Exception as e:
            logger.error(
                f"Failed to send registration email to {user_mail}: {str(e)}"
            )
            return False

    async def send_images_email(
        self, user_name: str, user_mail: str, image_paths: List[str], prompt: str
    ) -> bool:
        """
        Send images to the user via email

        Args:
            user_name: Name of the user
            user_mail: Email address of the user
            image_paths: List of file paths to the images to be sent
            prompt: The original prompt used to generate the images

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            subject = f"Your Images - Generated from Prompt: '{prompt}'"
            body = f"""
            Hello {user_name},

            Here are the images generated based on your prompt: '{prompt}'

            We hope you enjoy these images!

            Best regards,
            The SnapNSend Team
            """

            # Create the email message
            msg = MIMEMultipart()
            msg['From'] = settings.smtp_username
            msg['To'] = user_mail
            msg['Subject'] = subject

            # Attach the body text
            msg.attach(MIMEText(body, 'plain'))

            # Attach each image file
            for image_path in image_paths:
                try:
                    with open(image_path, "rb") as attachment:
                        # Instance of MIMEBase and named as part
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())

                    # Encode file in ASCII characters to send by email
                    encoders.encode_base64(part)

                    # Add header as key/value pair to attachment part
                    import os
                    part.add_header(
                        'Content-Disposition',
                        f"attachment; filename= {os.path.basename(image_path)}"
                    )

                    # Attach the part to message
                    msg.attach(part)
                except FileNotFoundError:
                    logger.warning(f"Image file not found: {image_path}")
                    continue  # Skip missing files but continue with others

            # Create secure connection with server and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(
                settings.smtp_server, settings.smtp_port, context=context
            ) as server:
                server.login(settings.smtp_username, settings.smtp_password)
                server.send_message(msg)

            logger.info(
                f"Images email sent to {user_mail} for user {user_name} "
                f"with {len(image_paths)} images from prompt '{prompt}'"
            )
            return True
        except Exception as e:
            logger.error(
                f"Failed to send images email to {user_mail}: {str(e)}"
            )
            return False


# Global email service instance
email_service = EmailService()
