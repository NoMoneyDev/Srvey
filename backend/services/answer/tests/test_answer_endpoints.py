import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from services.answer.schema import AnswerCreate


class TestAnswerEndpoints(unittest.IsolatedAsyncioTestCase):

    @patch("services.services.answer.AnswerService.get_all_answers", new_callable=AsyncMock)
    async def test_get_all_answers_success(self, mock_get_all):
        """Test getting all answers for a question"""
        mock_answers = [
            MagicMock(id="a1", text="Answer 1"),
            MagicMock(id="a2", text="Answer 2"),
        ]
        mock_get_all.return_value = mock_answers

        from services.answer.router import get_all_answers
        result = await get_all_answers(question_id="question456")

        self.assertEqual(len(result), 2)
        mock_get_all.assert_awaited_once_with("question456")

    @patch("services.services.answer.AnswerService.get_all_answers", new_callable=AsyncMock)
    async def test_get_all_answers_empty(self, mock_get_all):
        """Test getting answers when none exist"""
        mock_get_all.return_value = []

        from services.answer.router import get_all_answers
        result = await get_all_answers(question_id="question456")

        self.assertEqual(len(result), 0)

    @patch("services.services.answer.AnswerService.create_answer", new_callable=AsyncMock)
    async def test_create_single_answer_success(self, mock_create):
        """Test creating a single answer"""
        mock_answer = MagicMock(
            id="new_a1",
            question_id="question456",
            text="Option A"
        )
        mock_create.return_value = mock_answer

        from services.answer.router import create_answer
        payload = [
            AnswerCreate(
                question_id="question456",
                text="Option A"
            )
        ]
        result = await create_answer(answer_data=payload)

        self.assertEqual(len(result), 1)
        mock_create.assert_awaited_once()

    @patch("services.services.answer.AnswerService.create_answer", new_callable=AsyncMock)
    async def test_create_multiple_answers_success(self, mock_create):
        """Test creating multiple answers in batch"""
        mock_answers = [
            MagicMock(id="a1", text="Option A"),
            MagicMock(id="a2", text="Option B"),
            MagicMock(id="a3", text="Option C"),
        ]
        mock_create.side_effect = mock_answers

        from services.answer.router import create_answer
        payload = [
            AnswerCreate(question_id="question456", text="Option A"),
            AnswerCreate(question_id="question456", text="Option B"),
            AnswerCreate(question_id="question456", text="Option C"),
        ]
        result = await create_answer(answer_data=payload)

        self.assertEqual(len(result), 3)
        self.assertEqual(mock_create.await_count, 3)

    @patch("services.services.answer.AnswerService.create_answer", new_callable=AsyncMock)
    async def test_create_answers_empty_list(self, mock_create):
        """Test creating answers with empty list"""
        from services.answer.router import create_answer
        result = await create_answer(answer_data=[])

        self.assertEqual(len(result), 0)
        mock_create.assert_not_awaited()

    @patch("services.services.answer.AnswerService.get_all_answers", new_callable=AsyncMock)
    async def test_get_all_answers_correct_question_id(self, mock_get_all):
        """Test that get_all_answers receives correct question_id"""
        mock_get_all.return_value = []

        from services.answer.router import get_all_answers
        await get_all_answers(question_id="my_question_id")

        mock_get_all.assert_awaited_once_with("my_question_id")

    @patch("services.services.answer.AnswerService.create_answer", new_callable=AsyncMock)
    async def test_create_answers_preserves_data(self, mock_create):
        """Test that create_answer receives correct data"""
        mock_answer = MagicMock()
        mock_create.return_value = mock_answer

        from services.answer.router import create_answer
        payload = [
            AnswerCreate(
                question_id="question456",
                text="Option A",
                order=1
            )
        ]
        result = await create_answer(answer_data=payload)

        self.assertEqual(len(result), 1)
        call_args = mock_create.call_args
        self.assertEqual(call_args.kwargs["question_id"], "question456")
        self.assertEqual(call_args.kwargs["text"], "Option A")

    @patch("services.services.answer.AnswerService.create_answer", new_callable=AsyncMock)
    async def test_create_answers_with_special_characters(self, mock_create):
        """Test creating answers with special characters"""
        mock_answer = MagicMock()
        mock_create.return_value = mock_answer

        from services.answer.router import create_answer
        payload = [
            AnswerCreate(
                question_id="question456",
                text="Option with \"quotes\" and 'apostrophes'"
            )
        ]
        result = await create_answer(answer_data=payload)

        self.assertEqual(len(result), 1)

    @patch("services.services.answer.AnswerService.create_answer", new_callable=AsyncMock)
    async def test_create_answers_batch_processing(self, mock_create):
        """Test that all answers are processed in batch"""
        mock_create.side_effect = [
            MagicMock(id="a1"),
            MagicMock(id="a2"),
            MagicMock(id="a3"),
            MagicMock(id="a4"),
        ]

        from services.answer.router import create_answer
        payload = [
            AnswerCreate(question_id="q1", text="A"),
            AnswerCreate(question_id="q1", text="B"),
            AnswerCreate(question_id="q1", text="C"),
            AnswerCreate(question_id="q1", text="D"),
        ]
        result = await create_answer(answer_data=payload)

        self.assertEqual(len(result), 4)
        self.assertEqual(mock_create.await_count, 4)


if __name__ == "__main__":
    unittest.main()
