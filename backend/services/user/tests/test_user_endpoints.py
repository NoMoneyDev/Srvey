import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException


class TestUserEndpoints(unittest.IsolatedAsyncioTestCase):

    @patch("routes.utils.jwt.decode")
    @patch("routes.user.UserService.delete_user", new_callable=AsyncMock)
    async def test_delete_user_success(self, mock_delete, mock_jwt_decode):
        """Test successful user deletion"""
        mock_jwt_decode.return_value = {"sub": "user123"}
        mock_delete.return_value = True

        from services.user.router import delete_user
        result = await delete_user(user_id="user123")

        self.assertEqual(result["message"], "Deleted")
        mock_delete.assert_awaited_once_with("user123")

    @patch("routes.utils.jwt.decode")
    @patch("routes.user.UserService.delete_user", new_callable=AsyncMock)
    async def test_delete_user_not_found(self, mock_delete, mock_jwt_decode):
        """Test user deletion when user not found"""
        mock_jwt_decode.return_value = {"sub": "nonexistent"}
        mock_delete.return_value = False

        from services.user.router import delete_user
        with self.assertRaises(HTTPException) as ctx:
            await delete_user(user_id="nonexistent")
        
        self.assertEqual(ctx.exception.status_code, 404)
        self.assertEqual(ctx.exception.detail, "User not found")

    @patch("routes.utils.jwt.decode")
    @patch("routes.user.UserService.delete_user", new_callable=AsyncMock)
    async def test_delete_user_extracts_correct_user_id(self, mock_delete, mock_jwt_decode):
        """Test that delete extracts correct user_id from JWT token"""
        mock_jwt_decode.return_value = {"sub": "specific-user-id"}
        mock_delete.return_value = True

        from services.user.router import delete_user
        result = await delete_user(user_id="specific-user-id")

        self.assertEqual(result["message"], "Deleted")
        mock_delete.assert_awaited_once_with("specific-user-id")

    @patch("routes.utils.jwt.decode")
    @patch("routes.user.UserService.delete_user", new_callable=AsyncMock)
    async def test_delete_user_returns_correct_response(self, mock_delete, mock_jwt_decode):
        """Test that delete returns correct response structure"""
        mock_jwt_decode.return_value = {"sub": "user123"}
        mock_delete.return_value = True

        from services.user.router import delete_user
        result = await delete_user(user_id="user123")

        self.assertIsInstance(result, dict)
        self.assertIn("message", result)
        self.assertEqual(result["message"], "Deleted")


if __name__ == "__main__":
    unittest.main()
