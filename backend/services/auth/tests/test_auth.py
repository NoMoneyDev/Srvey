import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import HTTPException
from services.auth.schema import GoogleTokenRequest

# Mock app to avoid MongoDB connection on import
app = None


class TestAuthEndpoints(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        from fastapi import FastAPI
        # Create a minimal app to avoid MongoDB connection
        cls.app = FastAPI()
        cls.client = None

    def setUp(self):
        from fastapi.testclient import TestClient
        # Build the app with routes directly
        from fastapi import FastAPI, APIRouter
        from services.auth.router import router as auth_router
        
        test_app = FastAPI()
        test_app.include_router(auth_router)
        self.client = TestClient(test_app)
        self.valid_token = "Bearer valid.jwt.token"
        self.invalid_token = "Bearer invalid.jwt.token"

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

        response = self.client.post("/auth/google", json={"access_token": "valid-token"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("access_token", data)
        self.assertEqual(data["token_type"], "bearer")
        self.assertEqual(data["name"], "New User")
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

        response = self.client.post("/auth/google", json={"access_token": "valid-token"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("access_token", data)
        self.assertEqual(data["token_type"], "bearer")
        self.assertEqual(data["name"], "Existing User")

    @patch("routes.auth.id_token.verify_oauth2_token")
    async def test_google_auth_invalid_token(self, mock_verify_token):
        """Test Google auth with invalid token"""
        mock_verify_token.side_effect = ValueError("Invalid token")

        response = self.client.post("/auth/google", json={"access_token": "invalid-token"})

        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertEqual(data["detail"], "Invalid Google token")

    async def test_google_auth_missing_token(self):
        """Test Google auth with missing token"""
        response = self.client.post("/auth/google", json={})

        self.assertEqual(response.status_code, 422)

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

        response = self.client.post("/auth/google", json={"access_token": "valid-token"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["picture"], "https://example.com/avatar.jpg")

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

        response = self.client.post("/auth/google", json={"access_token": "valid-token"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["picture"], "")


if __name__ == "__main__":
    unittest.main()
