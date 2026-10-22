"""
Gmail API Email Service using OAuth 2.0

Provides secure, HTTPS-based transactional email delivery via the official
Google Gmail API. Uses refresh-token authentication to operate seamlessly
in non-interactive, headless production environments (such as Render).

Security:
- Never logs OTP codes, refresh tokens, client secrets, or full authorization headers.
- Masks recipient email addresses in operational logs.
- Does not rely on local file-based credentials at runtime.
"""

import os
import base64
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, Dict, Any, Tuple

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger("quantum_banking.gmail_service")

# Required scope for sending email via Gmail API
GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"


class GmailServiceError(Exception):
    """Custom exception for Gmail API service errors with sanitized messages."""
    pass


def _mask_email(email: str) -> str:
    """Mask email for secure logging (e.g., user@example.com -> u***@example.com)."""
    if not email or "@" not in email:
        return "[redacted-email]"
    local_part, domain = email.split("@", 1)
    if len(local_part) <= 2:
        masked_local = local_part[0] + "***"
    else:
        masked_local = local_part[0] + "***" + local_part[-1]
    return f"{masked_local}@{domain}"


class GmailService:
    """Singleton-style or reusable service for sending emails via Gmail REST API."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        refresh_token: Optional[str] = None,
        sender_email: Optional[str] = None,
    ):
        self._client_id = client_id
        self._client_secret = client_secret
        self._refresh_token = refresh_token
        self._sender_email = sender_email
        self._credentials: Optional[Credentials] = None
        self._service = None

    def _load_env_config(self) -> Tuple[str, str, str, str]:
        """Load and validate credentials from environment variables."""
        client_id = (
            self._client_id
            or os.getenv("GMAIL_CLIENT_ID")
            or os.getenv("GOOGLE_CLIENT_ID")
        )
        client_secret = (
            self._client_secret
            or os.getenv("GMAIL_CLIENT_SECRET")
            or os.getenv("GOOGLE_CLIENT_SECRET")
        )
        refresh_token = (
            self._refresh_token
            or os.getenv("GMAIL_REFRESH_TOKEN")
            or os.getenv("GOOGLE_REFRESH_TOKEN")
        )
        sender_email = (
            self._sender_email
            or os.getenv("GMAIL_SENDER_EMAIL")
            or os.getenv("FROM_EMAIL")
            or os.getenv("SMTP_EMAIL")
        )

        missing = []
        if not client_id:
            missing.append("GMAIL_CLIENT_ID")
        if not client_secret:
            missing.append("GMAIL_CLIENT_SECRET")
        if not refresh_token:
            missing.append("GMAIL_REFRESH_TOKEN")
        if not sender_email:
            missing.append("GMAIL_SENDER_EMAIL")

        if missing:
            raise GmailServiceError(
                f"Missing required Gmail OAuth configuration in environment: {', '.join(missing)}"
            )

        return client_id, client_secret, refresh_token, sender_email

    def get_credentials(self) -> Credentials:
        """Construct or refresh OAuth 2.0 Credentials object in-memory."""
        client_id, client_secret, refresh_token, _ = self._load_env_config()

        if self._credentials is None:
            self._credentials = Credentials(
                token=None,
                refresh_token=refresh_token,
                token_uri=GOOGLE_TOKEN_URI,
                client_id=client_id,
                client_secret=client_secret,
                scopes=GMAIL_SCOPES,
            )

        # Refresh token if expired or not yet fetched
        if not self._credentials.valid:
            request = Request()
            try:
                self._credentials.refresh(request)
            except RefreshError as e:
                logger.error("Gmail OAuth token refresh failed: invalid refresh token or client secret.")
                raise GmailServiceError(
                    "Gmail OAuth token refresh failed. Verify GMAIL_REFRESH_TOKEN, GMAIL_CLIENT_ID, and GMAIL_CLIENT_SECRET."
                ) from e
            except Exception as e:
                logger.error("Unexpected error during OAuth token refresh.")
                raise GmailServiceError(f"OAuth token refresh error: {str(e)}") from e

        return self._credentials

    def get_service(self):
        """Build and cache the authorized Gmail API service resource."""
        creds = self.get_credentials()
        # Always build with fresh credentials
        if self._service is None or not creds.valid:
            try:
                self._service = build("gmail", "v1", credentials=creds, cache_discovery=False)
            except Exception as e:
                logger.error("Failed to build Gmail API client service.")
                raise GmailServiceError(f"Failed to initialize Gmail API client: {str(e)}") from e
        return self._service

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        plain_body: Optional[str] = None,
        from_email: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send an email message via Gmail API.

        Args:
            to_email: Recipient email address
            subject: Email subject line
            html_body: HTML content of the email
            plain_body: Optional plain-text fallback content
            from_email: Optional override for sender email

        Returns:
            Dict containing message status, message_id, and thread_id on success.

        Raises:
            GmailServiceError: If validation or sending fails.
        """
        _, _, _, configured_sender = self._load_env_config()
        sender = from_email or configured_sender

        if not to_email or "@" not in to_email:
            raise GmailServiceError(f"Invalid recipient email address format: {_mask_email(to_email)}")

        masked_to = _mask_email(to_email)
        masked_from = _mask_email(sender)

        # Create MIME multipart message
        message = MIMEMultipart("alternative")
        message["to"] = to_email
        message["from"] = sender
        message["subject"] = subject

        # Attach text and html parts
        if plain_body:
            part1 = MIMEText(plain_body, "plain", "utf-8")
            message.attach(part1)

        part2 = MIMEText(html_body, "html", "utf-8")
        message.attach(part2)

        # Base64 URL-safe encode
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")

        try:
            service = self.get_service()
            send_request = service.users().messages().send(
                userId="me",
                body={"raw": raw_message}
            )
            result = send_request.execute()

            message_id = result.get("id")
            thread_id = result.get("threadId")

            logger.info("Email dispatched successfully via Gmail API to %s (Message ID: %s)", masked_to, message_id)

            return {
                "status": "success",
                "message_id": message_id,
                "thread_id": thread_id,
            }

        except HttpError as http_err:
            status_code = http_err.resp.status if hasattr(http_err, "resp") else "Unknown"
            error_details = http_err.content.decode("utf-8", errors="replace") if hasattr(http_err, "content") else str(http_err)
            
            logger.error(
                "Gmail API HTTP error [%s] when sending email to %s.",
                status_code, masked_to
            )

            if status_code == 401 or status_code == 403:
                raise GmailServiceError(
                    f"Gmail API authorization error (HTTP {status_code}): Check API enablement, scopes, and OAuth permissions."
                ) from http_err
            elif status_code == 429:
                raise GmailServiceError("Gmail API rate limit or quota exceeded.") from http_err
            else:
                raise GmailServiceError(f"Gmail API request failed with HTTP {status_code}") from http_err

        except GmailServiceError:
            raise
        except Exception as err:
            logger.error("Failed to send email via Gmail API to %s: %s", masked_to, str(err))
            raise GmailServiceError(f"Failed to dispatch email via Gmail API: {str(err)}") from err


# Global default instance
_default_gmail_service: Optional[GmailService] = None

def get_gmail_service() -> GmailService:
    """Retrieve or initialize the global GmailService instance."""
    global _default_gmail_service
    if _default_gmail_service is None:
        _default_gmail_service = GmailService()
    return _default_gmail_service


def send_email_via_gmail(
    to_email: str,
    subject: str,
    html_body: str,
    plain_body: Optional[str] = None,
    from_email: Optional[str] = None,
) -> Dict[str, Any]:
    """Helper function to send email using the shared Gmail service instance."""
    service = get_gmail_service()
    return service.send_email(
        to_email=to_email,
        subject=subject,
        html_body=html_body,
        plain_body=plain_body,
        from_email=from_email,
    )
