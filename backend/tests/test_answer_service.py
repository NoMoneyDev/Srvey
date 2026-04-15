import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from schemas.answer import AnswerCreate


class TestAnswerService(unittest.IsolatedAsyncioTestCase):
    """Tests for AnswerService endpoints"""

    @patch("services.answer_service.AnswerService.get_all_answers", new_callable=AsyncMock)
    async def test_get_all_answers_success(self, mock_get_all):
        """Test getting all answers for a question"""
        mock_answers = [
            MagicMock(id="a1", text="Answer 1"),
            MagicMock(id="a2", text="Answer 2"),
        ]
        mock_get_all.return_value = mock_answers

        from routes.answer import get_all_answers
        result = await get_all_answers(question_id="question456")

        self.assertEqual(len(result), 2)
        mock_get_all.assert_awaited_once_with("question456")

    @patch("services.answer_service.AnswerService.get_all_answers", new_callable=AsyncMock)
    async def test_get_all_answers_empty(self, mock_get_all):
        """Test getting answers when none exist"""
        mock_get_all.return_value = []

        from routes.answer import get_all_answers
        result = await get_all_answers(question_id="question456")

        self.assertEqual(len(result), 0)

    @patch("services.answer_service.AnswerService.get_all_answers", new_callable=AsyncMock)
    async def test_get_all_answers_correct_question_id(self, mock_get_all):
        """Test that get_all_answers receives correct question_id"""
        mock_get_all.return_value = []

        from routes.answer import get_all_answers
        await get_all_answers(question_id="my_question_id")

        mock_get_all.assert_awaited_once_with("my_question_id")

    @patch("services.answer_service.AnswerService.create_answer", new_callable=AsyncMock)
    async def test_create_single_answer_success(self, mock_create):
        """Test creating a single answer"""
        mock_answer = MagicMock(
            id="new_a1",
            question_id="question456",
            answer="Option A"
        )
        mock_create.return_value = mock_answer

        from routes.answer import create_answer
        payload = [
            AnswerCreate(
                response_id="r1",
                question_id="question456",
                answer=["Option A"]
            )
        ]
        result = await create_answer(answer_data=payload)

        self.assertEqual(len(result), 1)
        mock_create.assert_awaited_once()

    @patch("services.answer_service.AnswerService.create_answer", new_callable=AsyncMock)
    async def test_create_multiple_answers_success(self, mock_create):
        """Test creating multiple answers in batch"""
        mock_answers = [
            MagicMock(id="a1", answer="Option A"),
            MagicMock(id="a2", answer="Option B"),
            MagicMock(id="a3", answer="Option C"),
        ]
        mock_create.side_effect = mock_answers

        from routes.answer import create_answer
        payload = [
            AnswerCreate(response_id="r1", question_id="question456", answer=["Option A"]),
            AnswerCreate(response_id="r1", question_id="question456", answer=["Option B"]),
            AnswerCreate(response_id="r1", question_id="question456", answer=["Option C"]),
        ]
        result = await create_answer(answer_data=payload)

        self.assertEqual(len(result), 3)
        self.assertEqual(mock_create.await_count, 3)

    @patch("services.answer_service.AnswerService.create_answer", new_callable=AsyncMock)
    async def test_create_answers_empty_list(self, mock_create):
        """Test creating answers with empty list"""
        from routes.answer import create_answer
        result = await create_answer(answer_data=[])

        self.assertEqual(len(result), 0)
        mock_create.assert_not_awaited()

    @patch("services.answer_service.AnswerService.create_answer", new_callable=AsyncMock)
    async def test_create_answers_preserves_data(self, mock_create):
        """Test that create_answer receives correct data"""
        mock_answer = MagicMock()
        mock_create.return_value = mock_answer

        from routes.answer import create_answer
        payload = [
            AnswerCreate(
                response_id="resp1",
                question_id="question456",
                answer=["Option A", "Option B"]
            )
        ]
        result = await create_answer(answer_data=payload)

        self.assertEqual(len(result), 1)
        call_args = mock_create.call_args
        self.assertEqual(call_args.kwargs["response_id"], "resp1")
        self.assertEqual(call_args.kwargs["question_id"], "question456")

    @patch("services.answer_service.AnswerService.create_answer", new_callable=AsyncMock)
    async def test_create_answers_with_special_characters(self, mock_create):
        """Test creating answers with special characters"""
        mock_answer = MagicMock()
        mock_create.return_value = mock_answer

        from routes.answer import create_answer
        payload = [
            AnswerCreate(
                response_id="r1",
                question_id="question456",
                answer=["Option with \"quotes\" and 'apostrophes'"]
            )
        ]
        result = await create_answer(answer_data=payload)

        self.assertEqual(len(result), 1)

    @patch("services.answer_service.AnswerService.create_answer", new_callable=AsyncMock)
    async def test_create_answers_batch_processing(self, mock_create):
        """Test that all answers are processed in batch"""
        mock_create.side_effect = [
            MagicMock(id="a1"),
            MagicMock(id="a2"),
            MagicMock(id="a3"),
            MagicMock(id="a4"),
        ]

        from routes.answer import create_answer
        payload = [
            AnswerCreate(response_id="r1", question_id="q1", answer=["A"]),
            AnswerCreate(response_id="r1", question_id="q1", answer=["B"]),
            AnswerCreate(response_id="r1", question_id="q1", answer=["C"]),
            AnswerCreate(response_id="r1", question_id="q1", answer=["D"]),
        ]
        result = await create_answer(answer_data=payload)

        self.assertEqual(len(result), 4)
        self.assertEqual(mock_create.await_count, 4)


if __name__ == "__main__":
    unittest.main()
