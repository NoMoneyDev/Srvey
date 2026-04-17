import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from main import app
from services.survey.schema import SurveyCreate, SurveyUpdate


class TestSurveyEndpoints(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.valid_token = "Bearer valid.jwt.token"

    @patch("routes.utils.jwt.decode")
    @patch("routes.survey.SurveyService.get_all_surveys", new_callable=AsyncMock)
    async def test_get_all_surveys_success(self, mock_get_all, mock_jwt_decode):
        """Test getting all surveys with pagination"""
        mock_jwt_decode.return_value = {"sub": "user123"}
        
        mock_surveys = [
            MagicMock(id="survey1", title="Survey 1"),
            MagicMock(id="survey2", title="Survey 2"),
        ]
        mock_get_all.return_value = {
            "surveys": mock_surveys,
            "total": 2,
            "page": 1,
            "total_pages": 1
        }

        response = self.client.get("/survey/?page=1&page_size=10", headers={"Authorization": self.valid_token})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["surveys"]), 2)
        self.assertEqual(data["total"], 2)
        self.assertEqual(data["page"], 1)
        mock_get_all.assert_awaited_once_with(1, 10)

    @patch("routes.utils.jwt.decode")
    @patch("routes.survey.SurveyService.get_all_surveys", new_callable=AsyncMock)
    async def test_get_all_surveys_empty(self, mock_get_all, mock_jwt_decode):
        """Test getting surveys when none exist"""
        mock_jwt_decode.return_value = {"sub": "user123"}
        mock_get_all.return_value = {
            "surveys": [],
            "total": 0,
            "page": 1,
            "total_pages": 0
        }

        response = self.client.get("/survey/", headers={"Authorization": self.valid_token})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["surveys"]), 0)
        self.assertEqual(data["total"], 0)

    @patch("routes.utils.jwt.decode")
    @patch("routes.survey.SurveyService.get_survey", new_callable=AsyncMock)
    async def test_get_survey_found(self, mock_get, mock_jwt_decode):
        """Test getting specific survey"""
        mock_jwt_decode.return_value = {"sub": "user123"}
        
        mock_survey = MagicMock(id="survey123", title="Test Survey", description="A test survey")
        mock_get.return_value = mock_survey

        response = self.client.get("/survey/survey123", headers={"Authorization": self.valid_token})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("survey", data)
        mock_get.assert_awaited_once_with("survey123")

    @patch("routes.utils.jwt.decode")
    @patch("routes.survey.SurveyService.get_survey", new_callable=AsyncMock)
    async def test_get_survey_not_found(self, mock_get, mock_jwt_decode):
        """Test getting non-existent survey"""
        mock_jwt_decode.return_value = {"sub": "user123"}
        mock_get.return_value = None

        response = self.client.get("/survey/nonexistent", headers={"Authorization": self.valid_token})

        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["detail"], "Survey not found")

    @patch("routes.utils.jwt.decode")
    @patch("routes.survey.SurveyService.create_survey", new_callable=AsyncMock)
    async def test_create_survey_success(self, mock_create, mock_jwt_decode):
        """Test creating a new survey"""
        mock_jwt_decode.return_value = {"sub": "user123"}
        
        mock_survey = MagicMock(
            id="new_survey",
            title="New Survey",
            description="A new survey",
            created_by="user123",
            is_published=False
        )
        mock_create.return_value = mock_survey

        payload = {
            "title": "New Survey",
            "description": "A new survey",
            "created_by": "user123",
            "is_published": False
        }
        response = self.client.post("/survey/", json=payload, headers={"Authorization": self.valid_token})

        self.assertEqual(response.status_code, 200)
        mock_create.assert_awaited_once()

    @patch("routes.utils.jwt.decode")
    @patch("routes.survey.SurveyService.create_survey", new_callable=AsyncMock)
    async def test_create_survey_missing_required_field(self, mock_create, mock_jwt_decode):
        """Test creating survey with missing required field"""
        mock_jwt_decode.return_value = {"sub": "user123"}

        payload = {
            "description": "A new survey",
            "created_by": "user123"
            # Missing required 'title' field
        }
        response = self.client.post("/survey/", json=payload, headers={"Authorization": self.valid_token})

        self.assertEqual(response.status_code, 422)

    @patch("routes.utils.jwt.decode")
    @patch("routes.survey.SurveyService.update_survey", new_callable=AsyncMock)
    async def test_update_survey_success(self, mock_update, mock_jwt_decode):
        """Test updating a survey"""
        mock_jwt_decode.return_value = {"sub": "user123"}
        
        mock_survey = MagicMock(
            id="survey123",
            title="Updated Title",
            description="Updated description"
        )
        mock_update.return_value = mock_survey

        payload = {
            "title": "Updated Title",
            "description": "Updated description"
        }
        response = self.client.put("/survey/survey123", json=payload, headers={"Authorization": self.valid_token})

        self.assertEqual(response.status_code, 200)
        mock_update.assert_awaited_once()

    @patch("routes.utils.jwt.decode")
    @patch("routes.survey.SurveyService.update_survey", new_callable=AsyncMock)
    async def test_update_survey_not_found(self, mock_update, mock_jwt_decode):
        """Test updating non-existent survey"""
        mock_jwt_decode.return_value = {"sub": "user123"}
        mock_update.return_value = None

        payload = {"title": "Updated Title"}
        response = self.client.put("/survey/nonexistent", json=payload, headers={"Authorization": self.valid_token})

        self.assertEqual(response.status_code, 200)  # Service returns None, route doesn't check

    @patch("routes.utils.jwt.decode")
    @patch("routes.survey.SurveyService.delete_survey", new_callable=AsyncMock)
    async def test_delete_survey_success(self, mock_delete, mock_jwt_decode):
        """Test deleting a survey"""
        mock_jwt_decode.return_value = {"sub": "user123"}
        mock_delete.return_value = True

        response = self.client.delete("/survey/survey123", headers={"Authorization": self.valid_token})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "Deleted")
        mock_delete.assert_awaited_once_with("survey123")

    @patch("routes.utils.jwt.decode")
    @patch("routes.survey.SurveyService.delete_survey", new_callable=AsyncMock)
    async def test_delete_survey_not_found(self, mock_delete, mock_jwt_decode):
        """Test deleting non-existent survey"""
        mock_jwt_decode.return_value = {"sub": "user123"}
        mock_delete.return_value = False

        response = self.client.delete("/survey/nonexistent", headers={"Authorization": self.valid_token})

        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["detail"], "Survey not found")

    async def test_survey_endpoints_require_auth(self):
        """Test that survey endpoints require authentication"""
        response = self.client.get("/survey/")
        self.assertEqual(response.status_code, 403)

        response = self.client.post("/survey/", json={"title": "Test", "created_by": "user"})
        self.assertEqual(response.status_code, 403)

    @patch("routes.utils.jwt.decode")
    @patch("routes.survey.SurveyService.get_all_surveys", new_callable=AsyncMock)
    async def test_get_all_surveys_default_pagination(self, mock_get_all, mock_jwt_decode):
        """Test that default pagination values are used"""
        mock_jwt_decode.return_value = {"sub": "user123"}
        mock_get_all.return_value = {"surveys": [], "total": 0, "page": 1, "total_pages": 0}

        self.client.get("/survey/", headers={"Authorization": self.valid_token})

        # Default values should be page=1, page_size=10
        mock_get_all.assert_awaited_once_with(1, 10)


if __name__ == "__main__":
    unittest.main()
