import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException
from services.survey.schema import SurveyCreate, SurveyUpdate


class TestSurveyService(unittest.IsolatedAsyncioTestCase):
    """Tests for SurveyService endpoints"""

    @patch("routes.survey.SurveyService.get_all_surveys", new_callable=AsyncMock)
    async def test_get_all_surveys_success(self, mock_get_all):
        """Test getting all surveys with pagination"""
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

        from services.survey.router import get_all_surveys
        result = await get_all_surveys(page=1, page_size=10)

        self.assertEqual(len(result["surveys"]), 2)
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["page"], 1)
        mock_get_all.assert_awaited_once_with(1, 10)

    @patch("routes.survey.SurveyService.get_all_surveys", new_callable=AsyncMock)
    async def test_get_all_surveys_empty(self, mock_get_all):
        """Test getting surveys when none exist"""
        mock_get_all.return_value = {
            "surveys": [],
            "total": 0,
            "page": 1,
            "total_pages": 0
        }

        from services.survey.router import get_all_surveys
        result = await get_all_surveys(page=1, page_size=10)

        self.assertEqual(len(result["surveys"]), 0)
        self.assertEqual(result["total"], 0)

    @patch("routes.survey.SurveyService.get_all_surveys", new_callable=AsyncMock)
    async def test_get_all_surveys_pagination_page_2(self, mock_get_all):
        """Test pagination on page 2"""
        mock_get_all.return_value = {
            "surveys": [MagicMock(id="survey11")],
            "total": 15,
            "page": 2,
            "total_pages": 2
        }

        from services.survey.router import get_all_surveys
        result = await get_all_surveys(page=2, page_size=10)

        self.assertEqual(result["page"], 2)
        self.assertEqual(result["total"], 15)
        mock_get_all.assert_awaited_once_with(2, 10)

    @patch("routes.survey.SurveyService.get_survey", new_callable=AsyncMock)
    async def test_get_survey_found(self, mock_get):
        """Test getting specific survey"""
        mock_survey = MagicMock(id="survey123", title="Test Survey", description="A test survey")
        mock_get.return_value = mock_survey

        from services.survey.router import get_survey
        result = await get_survey(survey_id="survey123")

        self.assertIn("survey", result)
        self.assertEqual(result["survey"], mock_survey)
        mock_get.assert_awaited_once_with("survey123")

    @patch("routes.survey.SurveyService.get_survey", new_callable=AsyncMock)
    async def test_get_survey_not_found(self, mock_get):
        """Test getting non-existent survey"""
        mock_get.return_value = None

        from services.survey.router import get_survey
        with self.assertRaises(HTTPException) as ctx:
            await get_survey(survey_id="nonexistent")
        
        self.assertEqual(ctx.exception.status_code, 404)
        self.assertEqual(ctx.exception.detail, "Survey not found")

    @patch("routes.survey.SurveyService.create_survey", new_callable=AsyncMock)
    async def test_create_survey_success(self, mock_create):
        """Test creating a new survey"""
        mock_survey = MagicMock(
            id="new_survey",
            title="New Survey",
            description="A new survey",
            created_by="user123",
            is_published=False
        )
        mock_create.return_value = mock_survey

        from services.survey.router import create_survey
        payload = SurveyCreate(
            title="New Survey",
            description="A new survey",
            created_by="user123",
            is_published=False
        )
        result = await create_survey(survey_data=payload)

        self.assertEqual(result, mock_survey)
        mock_create.assert_awaited_once()

    @patch("routes.survey.SurveyService.update_survey", new_callable=AsyncMock)
    async def test_update_survey_success(self, mock_update):
        """Test updating a survey"""
        mock_survey = MagicMock(
            id="survey123",
            title="Updated Title",
            description="Updated description"
        )
        mock_update.return_value = mock_survey

        from services.survey.router import update_survey
        payload = SurveyUpdate(
            title="Updated Title",
            description="Updated description"
        )
        result = await update_survey(survey_id="survey123", survey_data=payload)

        self.assertEqual(result, mock_survey)
        mock_update.assert_awaited_once()

    @patch("routes.survey.SurveyService.update_survey", new_callable=AsyncMock)
    async def test_update_survey_partial(self, mock_update):
        """Test updating survey with partial data"""
        mock_survey = MagicMock(title="Only Title Updated")
        mock_update.return_value = mock_survey

        from services.survey.router import update_survey
        payload = SurveyUpdate(title="Only Title Updated")
        result = await update_survey(survey_id="survey123", survey_data=payload)

        self.assertEqual(result, mock_survey)
        mock_update.assert_awaited_once()

    @patch("routes.survey.SurveyService.delete_survey", new_callable=AsyncMock)
    async def test_delete_survey_success(self, mock_delete):
        """Test deleting a survey"""
        mock_delete.return_value = True

        from services.survey.router import delete_survey
        result = await delete_survey(survey_id="survey123")

        self.assertEqual(result["message"], "Deleted")
        mock_delete.assert_awaited_once_with("survey123")

    @patch("routes.survey.SurveyService.delete_survey", new_callable=AsyncMock)
    async def test_delete_survey_not_found(self, mock_delete):
        """Test deleting non-existent survey"""
        mock_delete.return_value = False

        from services.survey.router import delete_survey
        with self.assertRaises(HTTPException) as ctx:
            await delete_survey(survey_id="nonexistent")
        
        self.assertEqual(ctx.exception.status_code, 404)
        self.assertEqual(ctx.exception.detail, "Survey not found")


if __name__ == "__main__":
    unittest.main()
