export interface Question {
  _id: string
  survey_id: string
  question: string
  type: 'text' | 'multiple_choice' | 'checkbox' | 'rating'
  choices: string[]
  required: boolean
  order: number
}

export interface SurveyAnswer {
  questionId: string
  surveyId: string
  value: unknown
}

export interface Survey {
  _id: string
  title: string
  description?: string
  created_by: string
  created_at: string
}