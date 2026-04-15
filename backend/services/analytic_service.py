from collections import defaultdict
from http.client import responses
from typing import Dict, List
from bson import ObjectId

from models import Answer, Question, Response, Survey


class AnalyticService:

    @staticmethod
    async def get_survey_analytics(survey_id: str) -> Dict:
        # get all questions
        questions = await Question.find({"survey_id": survey_id}).to_list()

        # get all responses
        responses = await Response.find({"survey_id": survey_id}).to_list()
        response_ids = [r.id for r in responses]
        # get all answers
        answers = await Answer.find({
            "response_id": {"$in": response_ids}
        }).to_list()

        # group answers by question
        grouped_answers = defaultdict(list)
        for a in answers:
            grouped_answers[a.question_id].append(a.answer)

        survey = await Survey.get(survey_id)

        result = {
            "survey_id": survey_id,
            "total_responses": len(responses),
            "is_published": survey.is_published,
            "questions": []
        }

        for q in questions:
            qid = q.id
            q_answers = grouped_answers.get(qid, [])

            analytics = {
                "question_id": qid,
                "question": q.question,
                "type": q.type,
                "total_answers": len(q_answers)
            }

            # ================= TYPE HANDLING =================

            if q.type in ["multiple_choice", "checkbox"]:
                counter = defaultdict(int)

                for ans_list in q_answers:
                    for val in ans_list:
                        counter[val] += 1

                analytics["distribution"] = counter

            elif q.type == "rating":
                values = []
                for ans_list in q_answers:
                    for v in ans_list:
                        try:
                            values.append(float(v))
                        except:
                            pass

                avg = sum(values) / len(values) if values else 0
                analytics["average"] = avg
                analytics["min"] = min(values) if values else None
                analytics["max"] = max(values) if values else None

            elif q.type == "text":
                texts = []
                for ans_list in q_answers:
                    texts.extend(ans_list)

                analytics["responses"] = texts[:50]  # limit

            result["questions"].append(analytics)

        return result