"""
End-to-end test suite for Auth endpoints and Gmail API delivery flow
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json
from datetime import datetime, timedelta

# Ensure backend directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app


class TestAuthFlow(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    @patch("routes.auth.send_welcome_email")
    @patch("routes.auth.create_user")
    @patch("routes.auth.get_user_by_account")
    @patch("routes.auth.get_user_by_email")
    def test_register_flow(self, mock_get_email, mock_get_acc, mock_create, mock_welcome):
        mock_get_email.return_value = None
        mock_get_acc.return_value = None
        mock_create.return_value = 1
        mock_welcome.return_value = True

        payload = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "password": "Password123!"
        }
        response = self.client.post("/api/auth/register", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("account_number", data)
        self.assertEqual(len(data["account_number"]), 10)
        mock_welcome.assert_called_once()

    @patch("routes.auth.send_otp_email")
    @patch("routes.auth.store_otp")
    @patch("routes.auth.count_recent_otps")
    @patch("routes.auth.verify_password")
    @patch("routes.auth.get_user_by_account")
    def test_login_flow_with_gmail(self, mock_get_acc, mock_verify_pw, mock_count, mock_store, mock_send_otp):
        mock_get_acc.return_value = {
            "id": 42,
            "name": "Jane Doe",
            "account_number": "1234567890",
            "email": "jane@example.com",
            "password_hash": "dummy_hash"
        }
        mock_verify_pw.return_value = True
        mock_count.return_value = 0
        mock_send_otp.return_value = True

        payload = {
            "account_number": "1234567890",
            "password": "Password123!"
        }
        with patch.dict(os.environ, {"DEBUG_OTP": "false"}):
            response = self.client.post("/api/auth/login", json=payload)
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data.get("status"), "otp_sent")
            # Ensure OTP is NOT exposed in response
            self.assertNotIn("debug_otp", data)
            self.assertNotIn("otp", data)

    @patch("routes.auth.send_otp_email")
    @patch("routes.auth.store_otp")
    @patch("routes.auth.count_recent_otps")
    @patch("routes.auth.get_user_by_account")
    def test_resend_otp_flow_failure_handled(self, mock_get_acc, mock_count, mock_store, mock_send_otp):
        mock_get_acc.return_value = {
            "id": 42,
            "name": "Jane Doe",
            "account_number": "1234567890",
            "email": "jane@example.com"
        }
        mock_count.return_value = 0
        # Simulate Gmail API failure
        mock_send_otp.return_value = False

        payload = {"account_number": "1234567890"}
        response = self.client.post("/api/auth/resend-otp", json=payload)
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertEqual(data.get("error"), "Failed to send OTP email. Please try again.")

    @patch("routes.auth.mark_otp_used")
    @patch("routes.auth.get_valid_otp")
    @patch("routes.auth.get_user_by_account")
    def test_verify_otp_flow(self, mock_get_acc, mock_get_otp, mock_mark_used):
        mock_get_acc.return_value = {
            "id": 42,
            "name": "Jane Doe",
            "account_number": "1234567890",
            "email": "jane@example.com"
        }
        mock_get_otp.return_value = {
            "id": 99,
            "user_id": 42,
            "otp_code": "123456",
            "expires_at": datetime.now() + timedelta(minutes=5)
        }

        payload = {
            "account_number": "1234567890",
            "otp": "123456"
        }
        with patch.dict(os.environ, {"JWT_SECRET": "test_jwt_secret_key_1234567890123456"}):
            response = self.client.post("/api/auth/verify-otp", json=payload)
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn("token", data)
            self.assertEqual(data.get("user", {}).get("account_number"), "1234567890")
            mock_mark_used.assert_called_once_with(99)


if __name__ == "__main__":
    unittest.main()
