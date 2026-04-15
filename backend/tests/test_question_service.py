import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from schemas.question import QuestionCreate


class TestQuestionService(unittest.IsolatedAsyncioTestCase):
    """Tests for QuestionService endpoints"""

    @patch("services.question_service.QuestionService.get_all_questions", new_callable=AsyncMock)
    async def test_get_all_questions_success(self, mock_get_all):
        """Test getting all questions for a survey"""
        mock_questions = [
            MagicMock(id="q1", text="Question 1"),
            MagicMock(id="q2", text="Question 2"),
        ]
        mock_get_all.return_value = mock_questions

        from routes.question import get_all_questions
        result = await get_all_questions(survey_id="survey123")

        self.assertEqual(len(result), 2)
        mock_get_all.assert_awaited_once_with("survey123")

    @patch("services.question_service.QuestionService.get_all_questions", new_callable=AsyncMock)
    async def test_get_all_questions_empty(self, mock_get_all):
        """Test getting questions when none exist"""
        mock_get_all.return_value = []

        from routes.question import get_all_questions
        result = await get_all_questions(survey_id="survey123")

        self.assertEqual(len(result), 0)

    @patch("services.question_service.QuestionService.get_all_questions", new_callable=AsyncMock)
    async def test_get_all_questions_correct_survey_id(self, mock_get_all):
        """Test that get_all_questions receives correct survey_id"""
        mock_get_all.return_value = []

        from routes.question import get_all_questions
        await get_all_questions(survey_id="my_survey_id")

        mock_get_all.assert_awaited_once_with("my_survey_id")

    @patch("services.question_service.QuestionService.create_question", new_callable=AsyncMock)
    async def test_create_single_question_success(self, mock_create):
        """Test creating a single question"""
        mock_question = MagicMock(
            id="new_q1",
            survey_id="survey123",
            question="What is your name?",
            type="text"
        )
        mock_create.return_value = mock_question

        from routes.question import create_question
        payload = [
            QuestionCreate(
                survey_id="survey123",
                question="What is your name?",
                type="text",
                choices=["Option 1"],
                required=True,
                order=1
            )
        ]
        result = await create_question(question_data=payload)

        self.assertEqual(len(result), 1)
        mock_create.assert_awaited_once()

    @patch("services.question_service.QuestionService.create_question", new_callable=AsyncMock)
    async def test_create_multiple_questions_success(self, mock_create):
        """Test creating multiple questions in batch"""
        mock_questions = [
            MagicMock(id="q1", question="Question 1"),
            MagicMock(id="q2", question="Question 2"),
            MagicMock(id="q3", question="Question 3"),
        ]
        mock_create.side_effect = mock_questions

        from routes.question import create_question
        payload = [
            QuestionCreate(survey_id="survey123", question="Question 1", type="text", choices=[], required=True, order=1),
            QuestionCreate(survey_id="survey123", question="Question 2", type="text", choices=[], required=True, order=2),
            QuestionCreate(survey_id="survey123", question="Question 3", type="text", choices=[], required=True, order=3),
        ]
        result = await create_question(question_data=payload)

        self.assertEqual(len(result), 3)
        self.assertEqual(mock_create.await_count, 3)

    @patch("services.question_service.QuestionService.create_question", new_callable=AsyncMock)
    async def test_create_questions_empty_list(self, mock_create):
        """Test creating questions with empty list"""
        from routes.question import create_question
        result = await create_question(question_data=[])

        self.assertEqual(len(result), 0)
        mock_create.assert_not_awaited()

    @patch("services.question_service.QuestionService.create_question", new_callable=AsyncMock)
    async def test_create_questions_preserves_data(self, mock_create):
        """Test that create_question receives correct data"""
        mock_question = MagicMock()
        mock_create.return_value = mock_question

        from routes.question import create_question
        payload = [
            QuestionCreate(
                survey_id="survey123",
                question="What is your age?",
                type="multiple_choice",
                choices=["20-30", "30-40"],
                required=True,
                order=1
            )
        ]
        result = await create_question(question_data=payload)

        self.assertEqual(len(result), 1)
        call_args = mock_create.call_args
        self.assertEqual(call_args.kwargs["survey_id"], "survey123")
        self.assertEqual(call_args.kwargs["question"], "What is your age?")

    @patch("services.question_service.QuestionService.create_question", new_callable=AsyncMock)
    async def test_create_questions_batch_processing(self, mock_create):
        """Test that all questions are processed in batch"""
        mock_create.side_effect = [
            MagicMock(id="q1"),
            MagicMock(id="q2"),
            MagicMock(id="q3"),
        ]

        from routes.question import create_question
        payload = [
            QuestionCreate(survey_id="s1", question="Q1", type="text", choices=[], required=True, order=1),
            QuestionCreate(survey_id="s1", question="Q2", type="text", choices=[], required=True, order=2),
            QuestionCreate(survey_id="s1", question="Q3", type="text", choices=[], required=True, order=3),
        ]
        result = await create_question(question_data=payload)

        self.assertEqual(len(result), 3)
        self.assertEqual(mock_create.await_count, 3)


if __name__ == "__main__":
    unittest.main()
