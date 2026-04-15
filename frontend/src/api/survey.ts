const API_URL = import.meta.env.VITE_API_URL

export interface QuestionPayload {
  question: string
  type: 'text' | 'rating' | 'multiple_choice' | 'checkbox'
  choices: string[]
  required: boolean
  order: number
}

export interface CreateSurveyPayload {
  title: string
  description?: string
  is_published: boolean
}

export interface CreateSurveyQuestions {
  questions: QuestionPayload[]
}

export interface QuestionResponse extends QuestionPayload {
  _id: string
  survey_id: string
}

export type GetQuestionsResponse = QuestionResponse[]

export interface SurveyResponse {
  _id: string
  title: string
  description?: string
  created_by: string
  is_published: boolean
  created_at: string
}

export interface GetSurveysResponse {
  surveys: SurveyResponse[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

interface Answer {
  question_id: string   // ❌ camelCase
  value: unknown
  survey_id: string     // ❌ backend doesn't use this
}

const getAuthToken = () => localStorage.getItem('token')

async function fetchAPI<T>(
  method: string,
  url: string,
  body?: unknown
): Promise<T> {
  const options: RequestInit = {
    method,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${getAuthToken()}`,
    },
  }

  if (body) {
    options.body = JSON.stringify(body)
  }

  const response = await fetch(url, options)
  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`)
  }
  return response.json()
}

export const surveyAPI = {
  getMySurveys: async (skip: number = 0, limit: number = 10) => {
    const params = new URLSearchParams({ page: String(skip), page_size: String(limit) })
    return fetchAPI('GET', `${API_URL}/survey/me?${params}`)
  },

  createSurvey: async (surveyData: CreateSurveyPayload): Promise<SurveyResponse> => {
    return fetchAPI('POST', `${API_URL}/survey`, surveyData)
  },

  getSurveys: async (skip: number = 0, limit: number = 10): Promise<GetSurveysResponse> => {
    const params = new URLSearchParams({ page: String(skip), page_size: String(limit) })
    return fetchAPI<GetSurveysResponse>('GET', `${API_URL}/survey?${params}`)
  },

  getSurvey: async (surveyId: string): Promise<SurveyResponse> => {
    return fetchAPI<SurveyResponse>('GET', `${API_URL}/survey/${surveyId}`)
  },

  updateSurvey: async (surveyId: string, data: Partial<CreateSurveyPayload>) => {
    return fetchAPI('PUT', `${API_URL}/survey/${surveyId}`, data)
  },

  deleteSurvey: async (surveyId: string) => {
    await fetchAPI('DELETE', `${API_URL}/survey/${surveyId}`)
  },

  publishSurvey: async (surveyId: string) => {
    return fetchAPI('PUT', `${API_URL}/survey/${surveyId}`, { is_published: true })
  },

  createSurveyQuestions: async (surveyId: string, questionsData: CreateSurveyQuestions): Promise<QuestionResponse[]> => {
    return fetchAPI('POST', `${API_URL}/survey/${surveyId}/question`, questionsData)
  },

  getQuestions: async (surveyId: string): Promise<GetQuestionsResponse> => {
    return fetchAPI<GetQuestionsResponse>('GET', `${API_URL}/survey/${surveyId}/question`)
  },
  submitResponse: async (surveyId: string, answers: Answer[]) => {
  return fetchAPI(
    'POST',
    `${API_URL}/survey/${surveyId}/response`,
    answers
  )
}
}
