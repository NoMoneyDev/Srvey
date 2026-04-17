import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException
from services.auth.schema import GoogleTokenRequest


class TestAuthEndpoints(unittest.IsolatedAsyncioTestCase):

    @patch("routes.auth.id_token.verify_oauth2_token")
    @patch("routes.auth.UserService.find_one", new_callable=AsyncMock)
    @patch("routes.auth.UserService.create_user", new_callable=AsyncMock)
    async def test_google_auth_success_new_user(self, mock_create_user, mock_find_one, mock_verify_token):
        """Test successful Google authentication with new user creation"""
        google_user = {
            "sub": "123456",
            "email": "newuser@example.com",
            "name": "New User",
            "picture": "https://example.com/pic.jpg",
            "email_verified": True
        }
        mock_verify_token.return_value = google_user
        mock_find_one.return_value = None
        
        mock_new_user = MagicMock()
        mock_new_user.email = "newuser@example.com"
        mock_create_user.return_value = mock_new_user

        from services.auth.router import google_auth
        result = await google_auth(GoogleTokenRequest(access_token="valid-token"))

        self.assertIn("access_token", result)
        self.assertEqual(result["token_type"], "bearer")
        self.assertEqual(result["name"], "New User")
        mock_create_user.assert_awaited_once()

    @patch("routes.auth.id_token.verify_oauth2_token")
    @patch("routes.auth.UserService.find_one", new_callable=AsyncMock)
    async def test_google_auth_success_existing_user(self, mock_find_one, mock_verify_token):
        """Test successful Google authentication with existing user"""
        google_user = {
            "sub": "123456",
            "email": "existing@example.com",
            "name": "Existing User",
            "picture": "https://example.com/pic.jpg",
            "email_verified": True
        }
        mock_verify_token.return_value = google_user
        
        mock_existing_user = MagicMock()
        mock_existing_user.email = "existing@example.com"
        mock_find_one.return_value = mock_existing_user

        from services.auth.router import google_auth
        result = await google_auth(GoogleTokenRequest(access_token="valid-token"))

        self.assertIn("access_token", result)
        self.assertEqual(result["token_type"], "bearer")
        self.assertEqual(result["name"], "Existing User")

    @patch("routes.auth.id_token.verify_oauth2_token")
    async def test_google_auth_invalid_token(self, mock_verify_token):
        """Test Google auth with invalid token"""
        mock_verify_token.side_effect = ValueError("Invalid token")

        from services.auth.router import google_auth
        with self.assertRaises(HTTPException) as ctx:
            await google_auth(GoogleTokenRequest(access_token="invalid-token"))
        
        self.assertEqual(ctx.exception.status_code, 401)

    @patch("routes.auth.id_token.verify_oauth2_token")
    @patch("routes.auth.UserService.find_one", new_callable=AsyncMock)
    async def test_google_auth_response_has_picture(self, mock_find_one, mock_verify_token):
        """Test that response includes picture URL"""
        google_user = {
            "sub": "123456",
            "email": "user@example.com",
            "name": "Test User",
            "picture": "https://example.com/avatar.jpg",
            "email_verified": True
        }
        mock_verify_token.return_value = google_user
        mock_find_one.return_value = MagicMock()

        from services.auth.router import google_auth
        result = await google_auth(GoogleTokenRequest(access_token="valid-token"))

        self.assertEqual(result["picture"], "https://example.com/avatar.jpg")

    @patch("routes.auth.id_token.verify_oauth2_token")
    @patch("routes.auth.UserService.find_one", new_callable=AsyncMock)
    async def test_google_auth_response_has_default_picture_when_missing(self, mock_find_one, mock_verify_token):
        """Test that response includes empty string for picture if missing"""
        google_user = {
            "sub": "123456",
            "email": "user@example.com",
            "name": "Test User",
            "email_verified": True
        }
        mock_verify_token.return_value = google_user
        mock_find_one.return_value = MagicMock()

        from services.auth.router import google_auth
        result = await google_auth(GoogleTokenRequest(access_token="valid-token"))

        self.assertEqual(result["picture"], "")

    @patch("routes.auth.jwt.encode")
    @patch("routes.auth.id_token.verify_oauth2_token")
    @patch("routes.auth.UserService.find_one", new_callable=AsyncMock)
    async def test_google_auth_jwt_token_creation(self, mock_find_one, mock_verify_token, mock_encode):
        """Test JWT token is created with correct claims"""
        google_user = {
            "sub": "123456",
            "email": "user@example.com",
            "name": "Test User",
            "picture": "https://example.com/pic.jpg",
        }
        mock_verify_token.return_value = google_user
        mock_find_one.return_value = MagicMock()
        mock_encode.return_value = "encoded.jwt.token"

        from services.auth.router import google_auth
        result = await google_auth(GoogleTokenRequest(access_token="valid-token"))

        # Verify jwt.encode was called
        mock_encode.assert_called_once()
        call_args = mock_encode.call_args
        payload = call_args[0][0]
        
        self.assertEqual(payload["sub"], "user@example.com")
        self.assertIn("exp", payload)


if __name__ == "__main__":
    unittest.main()
