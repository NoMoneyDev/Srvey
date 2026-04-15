# API Endpoints Mapping - Frontend Testing Updated

## Backend Route Analysis

### Route Prefixes
```
/survey                 → Survey CRUD
/survey/{survey_id}/question       → Question operations
/survey/{survey_id}/response       → Response operations
/survey/{survey_id}/question/{question_id}/answer → Answer operations
/auth                   → Authentication
/users                  → User management
```

## Endpoint Details with Parameters

### Survey Endpoints

| Method | Backend Endpoint | Parameters | Frontend Test |
|--------|------------------|-----------|---|
| GET | `/survey` | `page: int = 1` `page_size: int = 10` | ✅ List Surveys |
| GET | `/survey/{survey_id}` | `survey_id: str` | ✅ Get Survey by ID |
| POST | `/survey` | `SurveyCreate` body | ✅ Create Survey |
| PUT | `/survey/{survey_id}` | `SurveyUpdate` body | ✅ Update Survey |
| DELETE | `/survey/{survey_id}` | `survey_id: str` | ✅ Delete Survey |

### Question Endpoints

| Method | Backend Endpoint | Parameters | Frontend Test |
|--------|------------------|-----------|---|
| GET | `/survey/{survey_id}/question` | `survey_id: str` (path) `question_id: str` (query) | ✅ Get Questions |
| POST | `/survey/{survey_id}/question` | `survey_id: str` (path) `List[QuestionCreate]` (body) | ✅ Create Questions |

### Response Endpoints

| Method | Backend Endpoint | Parameters | Frontend Test |
|--------|------------------|-----------|---|
| GET | `/survey/{survey_id}/response` | `survey_id: str` (path) `survey_id: str` (query) | ✅ List Responses |
| POST | `/survey/{survey_id}/response` | `survey_id: str` (path, query) `List[AnswerCreate]` (body) | ✅ Create Response |
| DELETE | `/survey/{survey_id}/response/{response_id}` | Both IDs in path | ✅ Delete Response |

### Answer Endpoints

| Method | Backend Endpoint | Parameters | Frontend Test |
|--------|------------------|-----------|---|
| GET | `/survey/{survey_id}/question/{question_id}/answer` | Both IDs in path, `question_id: str` (query) | ✅ Get Answers |
| POST | `/survey/{survey_id}/question/{question_id}/answer` | Both IDs in path, `List[AnswerCreate]` (body) | ✅ Create Answers |

### Auth Endpoints

| Method | Backend Endpoint | Parameters | Frontend Test |
|--------|------------------|-----------|---|
| POST | `/auth/google` | `access_token: str` (body) | ✅ Google Auth Test |

### User Endpoints

| Method | Backend Endpoint | Parameters |
|--------|------------------|-----------|
| DELETE | `/users/delete` | `user_id: str` (from JWT) |

## Frontend Testing Implementation

### Updated testing.ts (15 functions)

1. **getSurveys()** - Pagination support (page, page_size)
2. **getSurveyById(surveyId?)** - Get specific survey
3. **createSurvey()** - Creates with title and description
4. **updateSurvey(surveyId?)** - Updates title, description, is_published
5. **deleteSurvey(surveyId?)** - Deletes survey
6. **getQuestions(surveyId?)** - Fetch questions for survey
7. **createQuestions(surveyId?)** - Create batch questions
8. **getResponses(surveyId?)** - List responses with query param
9. **createResponse(surveyId?)** - Create response with answers
10. **deleteResponse(surveyId?, responseId?)** - Delete response
11. **getAnswers(surveyId?, questionId?)** - Fetch answers
12. **createAnswers(surveyId?, questionId?)** - Create batch answers
13. **googleAuth()** - Test OAuth endpoint
14. **healthCheck()** - Verify API connectivity

### Test Buttons (14 total)

**Health** (1)
- Health Check

**Survey** (6)
- List Surveys (with pagination)
- Get Survey by ID
- Create Survey (auto-generates)
- Update Survey
- Delete Survey
- [New] Get/Create/Delete chain testing

**Question** (2)
- Get Questions
- Create Questions

**Response** (3)
- List Responses
- Create Response
- Delete Response

**Answer** (2)
- Get Answers
- Create Answers

**Auth** (1)
- Google Auth Test

## Key Changes Made

### API Client (testing.ts)
✅ Updated all parameter names to match backend (page/page_size, not skip/limit)
✅ Added path parameters in URLs (/{survey_id}/{question_id})
✅ Added query parameters where needed
✅ Added new endpoints for CRUD completeness
✅ All functions use actual backend signatures
✅ Consistent error handling across all functions

### HomeView.vue
✅ Updated test button descriptions with exact endpoints
✅ Added 7 new test buttons
✅ Organized into 6 categories
✅ Each button maps to correct API function
✅ Parameter handling with optional defaults

## Testing Flow Recommendations

### Recommended Test Sequence
1. **Health Check** - Verify API responds
2. **Create Survey** - Generate test data
3. **List Surveys** - See newly created survey
4. **Get Survey by ID** - Test single survey retrieval
5. **Create Questions** - Add questions to survey
6. **Get Questions** - Verify questions created
7. **Create Response** - Submit responses
8. **List Responses** - View submitted responses
9. **Get Answers** - View question answers

### Testing with Real Data
- Copy actual survey_id/question_id/response_id from results
- Paste into function calls for testing dependent endpoints
- Chain tests together for integration testing

## Notes

- All parameters now match backend exactly
- Query parameters use correct names
- Path parameters properly formatted
- Response structures aligned with actual API
- Error handling consistent across all endpoints
- Support for optional IDs (uses test-* defaults)
- Can be extended with real ID parameters

## Files Updated

- `/frontend/src/api/testing.ts` - 15 test functions (450+ lines)
- `/frontend/src/views/HomeView.vue` - 14 test buttons

All changes verified with ESLint and TypeScript.
