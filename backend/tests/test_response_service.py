import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException
from schemas.answer import AnswerCreate


class TestResponseService(unittest.IsolatedAsyncioTestCase):
    """Tests for ResponseService endpoints"""

    @patch("services.response_service.ResponseService.get_all_responses", new_callable=AsyncMock)
    async def test_get_all_responses_success(self, mock_get_all):
        """Test getting all responses for a survey"""
        mock_responses = [
            MagicMock(id="r1", survey_id="survey123", user_id="user1"),
            MagicMock(id="r2", survey_id="survey123", user_id="user2"),
        ]
        mock_get_all.return_value = mock_responses

        from routes.response import get_all_responses
        result = await get_all_responses(survey_id="survey123")

        self.assertEqual(len(result), 2)
        mock_get_all.assert_awaited_once_with("survey123")

    @patch("services.response_service.ResponseService.get_all_responses", new_callable=AsyncMock)
    async def test_get_all_responses_empty(self, mock_get_all):
        """Test getting responses when none exist"""
        mock_get_all.return_value = []

        from routes.response import get_all_responses
        result = await get_all_responses(survey_id="survey123")

        self.assertEqual(len(result), 0)

    @patch("services.response_service.ResponseService.get_all_responses", new_callable=AsyncMock)
    async def test_get_all_responses_correct_survey_id(self, mock_get_all):
        """Test that get_all_responses receives correct survey_id"""
        mock_get_all.return_value = []

        from routes.response import get_all_responses
        await get_all_responses(survey_id="my_survey_id")

        mock_get_all.assert_awaited_once_with("my_survey_id")

    @patch("services.response_service.ResponseService.create_response", new_callable=AsyncMock)
    @patch("services.answer_service.AnswerService.create_answer", new_callable=AsyncMock)
    async def test_create_response_success(self, mock_answer_create, mock_response_create):
        """Test creating a response with answers"""
        mock_response = MagicMock(
            id="r1",
            survey_id="survey123",
            user_id="user123"
        )
        mock_response_create.return_value = mock_response
        
        mock_answers = [
            MagicMock(id="ans1", response_id="r1"),
            MagicMock(id="ans2", response_id="r1"),
        ]
        mock_answer_create.side_effect = mock_answers

        from routes.response import create_response
        payload = [
            AnswerCreate(response_id="r1", question_id="q1", answer=["answer1"]),
            AnswerCreate(response_id="r1", question_id="q2", answer=["answer2"]),
        ]
        result = await create_response(
            survey_id="survey123",
            answer_data=payload,
            user_id="user123"
        )

        self.assertEqual(len(result), 2)
        mock_response_create.assert_awaited_once()
        self.assertEqual(mock_answer_create.await_count, 2)

    @patch("services.response_service.ResponseService.create_response", new_callable=AsyncMock)
    async def test_create_response_without_answers(self, mock_response_create):
        """Test creating a response without answers"""
        mock_response = MagicMock(
            id="r1",
            survey_id="survey123",
            user_id="user123"
        )
        mock_response_create.return_value = mock_response

        from routes.response import create_response
        result = await create_response(
            survey_id="survey123",
            answer_data=[],
            user_id="user123"
        )

        self.assertEqual(len(result), 0)
        mock_response_create.assert_awaited_once_with({
            "survey_id": "survey123",
            "user_id": "user123"
        })

    @patch("services.response_service.ResponseService.create_response", new_callable=AsyncMock)
    @patch("services.answer_service.AnswerService.create_answer", new_callable=AsyncMock)
    async def test_create_response_user_id_from_token(self, mock_answer_create, mock_response_create):
        """Test that create_response receives user_id from token"""
        mock_response_create.return_value = MagicMock()
        mock_answer_create.return_value = MagicMock()

        from routes.response import create_response
        payload = []
        await create_response(
            survey_id="survey123",
            answer_data=payload,
            user_id="authenticated_user"
        )

        call_args = mock_response_create.call_args
        self.assertEqual(call_args[0][0]["user_id"], "authenticated_user")
        self.assertEqual(call_args[0][0]["survey_id"], "survey123")

    @patch("services.response_service.ResponseService.create_response", new_callable=AsyncMock)
    @patch("services.answer_service.AnswerService.create_answer", new_callable=AsyncMock)
    async def test_create_response_with_many_answers(self, mock_answer_create, mock_response_create):
        """Test creating response with many answers"""
        mock_response_create.return_value = MagicMock()
        mock_answer_create.return_value = MagicMock()

        from routes.response import create_response
        payload = [
            AnswerCreate(response_id="r1", question_id=f"q{i}", answer=[f"answer{i}"])
            for i in range(10)
        ]
        
        result = await create_response(
            survey_id="survey123",
            answer_data=payload,
            user_id="user123"
        )

        self.assertEqual(len(result), 10)
        self.assertEqual(mock_answer_create.await_count, 10)

    @patch("services.response_service.ResponseService.delete_response", new_callable=AsyncMock)
    async def test_delete_response_success(self, mock_delete):
        """Test deleting a response"""
        mock_delete.return_value = True

        from routes.response import delete_response
        result = await delete_response(response_id="response456")

        self.assertEqual(result["message"], "Deleted")
        mock_delete.assert_awaited_once_with("response456")

    @patch("services.response_service.ResponseService.delete_response", new_callable=AsyncMock)
    async def test_delete_response_not_found(self, mock_delete):
        """Test deleting non-existent response"""
        mock_delete.return_value = False

        from routes.response import delete_response
        with self.assertRaises(HTTPException) as ctx:
            await delete_response(response_id="nonexistent")
        
        self.assertEqual(ctx.exception.status_code, 404)

    @patch("services.response_service.ResponseService.delete_response", new_callable=AsyncMock)
    async def test_delete_response_correct_response_id(self, mock_delete):
        """Test that delete_response receives correct response_id"""
        mock_delete.return_value = True

        from routes.response import delete_response
        await delete_response(response_id="specific_response_id")

        mock_delete.assert_awaited_once_with("specific_response_id")


if __name__ == "__main__":
    unittest.main()
