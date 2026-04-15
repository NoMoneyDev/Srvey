<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { surveyAPI, type QuestionPayload } from '@/api/survey'

const router = useRouter()

interface QuestionForm extends QuestionPayload {
  id: string
  min?: number
  max?: number
}

type QuestionType = 'text' | 'rating' | 'multiple_choice' | 'checkbox'

interface QuestionTypeOption {
  value: QuestionType
  label: string
  description: string
  icon: string
}

const QUESTION_TYPES: QuestionTypeOption[] = [
  {
    value: 'text',
    label: 'Text',
    description: 'Short or long text response',
    icon: '📝',
  },
  {
    value: 'multiple_choice',
    label: 'Multiple Choice',
    description: 'Select one option from a list',
    icon: '⭕',
  },
  {
    value: 'checkbox',
    label: 'Checkbox',
    description: 'Select multiple options',
    icon: '☑️',
  },
  {
    value: 'rating',
    label: 'Rating',
    description: 'Rate on a scale',
    icon: '⭐',
  },
]

const surveyTitle = ref('')
const surveyDescription = ref('')
const questions = ref<QuestionForm[]>([])
const isLoading = ref(false)
const error = ref('')
const success = ref('')
const showTypeSelector = ref(false)
const showPublishPrompt = ref(false)
const createdSurveyId = ref('')
const isPublishing = ref(false)
const publishSurvey = ref(false)

const questionIdCounter = ref(0)

const selectQuestionType = (type: QuestionType) => {
  questionIdCounter.value++
  questions.value.push({
    id: `q-${questionIdCounter.value}`,
    question: '',
    type,
    choices: [],
    required: false,
    order: questions.value.length + 1,
    min: type === 'rating' ? 1 : undefined,
    max: type === 'rating' ? 10 : undefined,
  })
  showTypeSelector.value = false
}

const addQuestion = () => {
  if (questions.value.length === 0) {
    showTypeSelector.value = true
  } else {
    showTypeSelector.value = true
  }
}

const removeQuestion = (id: string) => {
  const index = questions.value.findIndex((q) => q.id === id)
  if (index > -1) {
    questions.value.splice(index, 1)
    updateQuestionOrder()
  }
}

const updateQuestionOrder = () => {
  questions.value.forEach((q, index) => {
    q.order = index + 1
  })
}

const moveQuestionUp = (id: string) => {
  const index = questions.value.findIndex((q) => q.id === id)
  if (index > 0) {
    const temp = questions.value[index - 1]!
    questions.value[index - 1] = questions.value[index]!
    questions.value[index] = temp
    updateQuestionOrder()
  }
}

const moveQuestionDown = (id: string) => {
  const index = questions.value.findIndex((q) => q.id === id)
  if (index < questions.value.length - 1) {
    const temp = questions.value[index]!
    questions.value[index] = questions.value[index + 1]!
    questions.value[index + 1] = temp
    updateQuestionOrder()
  }
}

const addChoice = (id: string) => {
  const question = questions.value.find((q) => q.id === id)
  if (question) {
    question.choices.push('')
  }
}

const removeChoice = (id: string, index: number) => {
  const question = questions.value.find((q) => q.id === id)
  if (question) {
    question.choices.splice(index, 1)
  }
}

const isFormValid = computed(() => {
  return (
    surveyTitle.value.trim() !== '' &&
    questions.value.length > 0 &&
    questions.value.every((q) => q.question.trim() !== '')
  )
})

const askPublishPrompt = () => {
  showPublishPrompt.value = true
}

const createSurvey = async () => {
  error.value = ''
  success.value = ''
  isLoading.value = true

  try {
    const surveyData = {
      title: surveyTitle.value,
      description: surveyDescription.value || undefined,
      is_published: publishSurvey.value,
    }

    const questionsPayload = questions.value.map((q) => {
      if (q.type === 'rating') {
        return {
          question: q.question,
          type: q.type,
          choices: [String(q.min ?? 1), String(q.max ?? 10)],
          required: q.required,
          order: q.order,
        }
      }

      return {
        question: q.question,
        type: q.type,
        choices: q.choices.filter((c) => c.trim() !== ''),
        required: q.required,
        order: q.order,
      }
    })
    
    const result = await surveyAPI.createSurvey(surveyData)
    await surveyAPI.createSurveyQuestions(result._id, questionsPayload)
    success.value = 'Survey created successfully!'
    createdSurveyId.value = result._id
    showPublishPrompt.value = false
    router.push(`/surveys/${result._id}/take`)
  } catch (err: unknown) {
    const error_msg = (err as any)?.response?.data?.detail || 'Failed to create survey'
    error.value = error_msg as string
  } finally {
    isLoading.value = false
  }
}

const publishSurveyNow = async () => {
  publishSurvey.value = true
  createSurvey()
}

const skipPublish = () => {
  publishSurvey.value = false
  createSurvey()
}

const resetForm = () => {
  surveyTitle.value = ''
  surveyDescription.value = ''
  questions.value = []
  questionIdCounter.value = 0
  error.value = ''
  success.value = ''
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
    <div class="max-w-4xl mx-auto">
      
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-4xl font-bold text-gray-900 mb-2">Create a New Survey</h1>
        <p class="text-lg text-gray-600">Build your survey by adding a title, description, and questions</p>
      </div>

      <!-- Alerts -->
      <div v-if="error" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
        <p class="text-red-800">❌ {{ error }}</p>
      </div>

      <div v-if="success" class="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
        <p class="text-green-800">✅ {{ success }}</p>
      </div>

      <!-- Form -->
      <form @submit.prevent="askPublishPrompt" class="space-y-6">

        <!-- Survey Info -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Survey Details</h2>

          <div class="space-y-4">
            <input
              v-model="surveyTitle"
              placeholder="Survey Title"
              class="w-full px-4 py-2 border rounded-lg text-black"
              required
            />

            <textarea
              v-model="surveyDescription"
              placeholder="Description"
              class="w-full px-4 py-2 border rounded-lg text-black"
            />
          </div>
        </div>

        <!-- Questions -->
        <div v-if="questions.length > 0" class="space-y-4">
          <div
            v-for="(question, idx) in questions"
            :key="question.id"
            class="bg-white p-6 rounded-lg shadow"
          >
            <div class="flex justify-between mb-4">
              <span class="text-black">Question {{ idx + 1 }}</span>
              <button @click="removeQuestion(question.id)" type="button" class="text-red-600">
                Remove
              </button>
            </div>

            <!-- Question text -->
            <textarea
              v-model="question.question"
              placeholder="Enter question"
              class="w-full px-4 py-2 border rounded-lg text-black"
            />

            <!-- Question type -->
            <div class="mt-3 text-sm text-black">
              {{ QUESTION_TYPES.find(t => t.value === question.type)?.label }}
            </div>

            <!-- Required -->
            <label class="flex items-center gap-2 mt-2 text-black">
              <input type="checkbox" v-model="question.required" />
              Required
            </label>

            <!-- Choices -->
            <div
              v-if="['multiple_choice', 'checkbox'].includes(question.type)"
              class="mt-4 space-y-2"
            >
              <div class="flex justify-between">
                <span class="text-sm text-black">Options</span>
                <button type="button" @click="addChoice(question.id)" class="text-blue-600">
                  + Add
                </button>
              </div>

              <div
                v-for="(choice, cIdx) in question.choices"
                :key="cIdx"
                class="flex gap-2"
              >
                <input
                  v-model="question.choices[cIdx]"
                  class="flex-1 px-3 py-2 border rounded text-black"
                />
                <button
                  @click="removeChoice(question.id, cIdx)"
                  type="button"
                  class="text-red-600"
                >
                  Remove
                </button>
              </div>
            </div>

            <!-- Rating -->
            <div v-if="question.type === 'rating'" class="mt-4 space-y-3">
              <span class="text-sm text-black">Rating Range</span>

              <div class="flex gap-4">
                <div class="flex-1">
                  <label class="text-xs text-black">Min</label>
                  <input
                    type="number"
                    v-model.number="question.min"
                    class="w-full px-3 py-2 border rounded text-black"
                  />
                </div>

                <div class="flex-1">
                  <label class="text-xs text-black">Max</label>
                  <input
                    type="number"
                    v-model.number="question.max"
                    class="w-full px-3 py-2 border rounded text-black"
                  />
                </div>
              </div>
            </div>

          </div>
        </div>

        <!-- Add Question -->
        <button
          type="button"
          @click="addQuestion"
          class="px-4 py-2 bg-blue-500 text-white rounded"
        >
          Add Question
        </button>

        <!-- Submit -->
        <button
          type="submit"
          class="px-6 py-2 bg-green-600 text-white rounded"
        >
          Create Survey
        </button>

      </form>

      <!-- Publish Prompt Modal -->
      <div
        v-if="showPublishPrompt"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      >
        <div class="bg-white rounded-lg p-6 w-full max-w-md">
          <h2 class="text-xl font-bold mb-4 text-black">Last Step!</h2>
          <p class="text-black mb-4">
            Do you want to publish now?
          </p>

          <div class="flex gap-3">
            <button
              type="button"
              @click="skipPublish"
              class="flex-1 px-4 py-2 border rounded text-black"
            >
              Publish Later
            </button>

            <button
              type="button"
              @click="publishSurveyNow"
              class="flex-1 px-4 py-2 bg-blue-600 text-white rounded"
            >
              Publish Now
            </button>
          </div>
        </div>
      </div>

      <!-- Question Type Selector -->
      <div
        v-if="showTypeSelector"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
        @click.self="showTypeSelector = false"
      >
        <div class="bg-white rounded-lg p-6 w-full max-w-md">
          <h2 class="text-xl font-bold mb-4 text-black">Select Question Type</h2>

          <div class="grid gap-3">
            <button
              v-for="type in QUESTION_TYPES"
              :key="type.value"
              @click="selectQuestionType(type.value)"
              class="p-4 border rounded hover:bg-gray-100 text-left"
            >
              <div class="text-2xl">{{ type.icon }}</div>
              <div class="font-semibold text-black">{{ type.label }}</div>
              <div class="text-sm text-black">{{ type.description }}</div>
            </button>
          </div>

          <button
            @click="showTypeSelector = false"
            class="mt-4 w-full py-2 border rounded text-black"
          >
            Cancel
          </button>
        </div>
      </div>

    </div>
  </div>
</template>