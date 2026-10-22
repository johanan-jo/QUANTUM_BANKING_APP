"""
Unit and Integration Tests for Gmail API Service & Mailer
"""

import unittest
from unittest.mock import MagicMock, patch
import os
import sys
import base64
from email.message import Message

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.gmail_service import (
    GmailService,
    GmailServiceError,
    _mask_email,
    send_email_via_gmail
)
from utils.mailer import send_otp_email, send_welcome_email


class TestGmailService(unittest.TestCase):

    def test_mask_email(self):
        self.assertEqual(_mask_email("john@example.com"), "j***n@example.com")
        self.assertEqual(_mask_email("ab@bank.com"), "a***@bank.com")
        self.assertEqual(_mask_email("invalid_email"), "[redacted-email]")

    def test_missing_env_vars_raises_error(self):
        service = GmailService(
            client_id=None,
            client_secret=None,
            refresh_token=None,
            sender_email=None
        )
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(GmailServiceError) as ctx:
                service._load_env_config()
            self.assertIn("Missing required Gmail OAuth configuration", str(ctx.exception))

    def test_invalid_recipient_format(self):
        service = GmailService(
            client_id="dummy_id",
            client_secret="dummy_secret",
            refresh_token="dummy_token",
            sender_email="sender@bank.com"
        )
        with self.assertRaises(GmailServiceError) as ctx:
            service.send_email(to_email="invalidemail", subject="Test", html_body="<p>Hi</p>")
        self.assertIn("Invalid recipient email address format", str(ctx.exception))

    @patch("utils.gmail_service.build")
    @patch("utils.gmail_service.Credentials")
    def test_send_email_success(self, mock_creds_class, mock_build):
        mock_creds = MagicMock()
        mock_creds.valid = True
        mock_creds_class.return_value = mock_creds

        mock_service = MagicMock()
        mock_messages = MagicMock()
        mock_send = MagicMock()
        mock_send.execute.return_value = {"id": "msg_12345", "threadId": "th_67890"}
        mock_messages.send.return_value = mock_send
        mock_service.users.return_value.messages.return_value = mock_messages
        mock_build.return_value = mock_service

        service = GmailService(
            client_id="test_id",
            client_secret="test_secret",
            refresh_token="test_token",
            sender_email="sender@bank.com"
        )

        res = service.send_email(
            to_email="customer@example.com",
            subject="Test Subject",
            html_body="<p>Test Content</p>",
            plain_body="Test Content"
        )

        self.assertEqual(res["status"], "success")
        self.assertEqual(res["message_id"], "msg_12345")
        self.assertEqual(res["thread_id"], "th_67890")

        # Verify arguments sent to Gmail API
        mock_messages.send.assert_called_once()
        call_kwargs = mock_messages.send.call_args[1]
        self.assertEqual(call_kwargs["userId"], "me")
        raw_b64 = call_kwargs["body"]["raw"]
        decoded_bytes = base64.urlsafe_b64decode(raw_b64.encode("utf-8"))
        decoded_str = decoded_bytes.decode("utf-8")
        self.assertIn("customer@example.com", decoded_str)
        self.assertIn("sender@bank.com", decoded_str)
        self.assertIn("Test Subject", decoded_str)

    @patch("utils.mailer.send_email_via_gmail")
    def test_send_otp_email_success_and_failure(self, mock_send_via_gmail):
        # 1. Success case
        mock_send_via_gmail.return_value = {"status": "success", "message_id": "msg_999"}
        success = send_otp_email("user@example.com", "654321")
        self.assertTrue(success)

        # 2. Failure case
        mock_send_via_gmail.side_effect = GmailServiceError("API quota exceeded")
        failure = send_otp_email("user@example.com", "654321")
        self.assertFalse(failure)

    @patch("utils.mailer.send_email_via_gmail")
    def test_send_welcome_email_success_and_failure(self, mock_send_via_gmail):
        # 1. Success case
        mock_send_via_gmail.return_value = {"status": "success", "message_id": "msg_1000"}
        success = send_welcome_email("user@example.com", "Alice Smith", "1234567890")
        self.assertTrue(success)

        # 2. Failure case
        mock_send_via_gmail.side_effect = GmailServiceError("Auth error")
        failure = send_welcome_email("user@example.com", "Alice Smith", "1234567890")
        self.assertFalse(failure)


if __name__ == "__main__":
    unittest.main()
