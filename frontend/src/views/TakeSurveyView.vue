<template>
  <div class="w-full px-4 py-8 min-h-screen flex flex-col">    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-12">
      <p class="text-gray-600 text-lg">Loading survey...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6">
      <h2 class="text-2xl font-bold text-red-900 mb-2">Error</h2>
      <p class="text-red-800">{{ error }}</p>
    </div>

    <!-- Survey Form -->
    <div v-else-if="sortedQuestions.length > 0" class="space-y-6 flex flex-col h-full">
      <!-- progress -->
      <div class="w-full h-1 bg-gray-100 rounded-full mb-8 overflow-hidden">
        <div
          class="h-full bg-indigo-500 rounded-full transition-all duration-500"
          :style="{ width: progressPct + '%' }"
        />
      </div>

      <!-- question card -->
      <Transition name="slide" mode="out-in">
        <div class="flex-1 flex" :key="currentIndex">
          <div
            v-if="!done && currentQuestion"
            class="bg-white border border-gray-100 rounded-2xl p-8 shadow-sm flex flex-col gap-5 flex-1"
          >
            <TextQuestion
              v-if="currentQuestion.type === 'text'"
              :question="currentQuestion"
              :index="currentIndex"
              :total="questions.length"
              @answer="handleAnswer"
              @next="handleNext"
            />
            <MultipleChoiceQuestion
              v-else-if="currentQuestion.type === 'multiple_choice'"
              :question="currentQuestion"
              :index="currentIndex"
              :total="questions.length"
              @answer="handleAnswer"
              @next="handleNext"
            />
            <CheckboxQuestion
              v-else-if="currentQuestion.type === 'checkbox'"
              :question="currentQuestion"
              :index="currentIndex"
              :total="questions.length"
              @answer="handleAnswer"
              @next="handleNext"
            />
            <RatingQuestion
              v-else-if="currentQuestion.type === 'rating'"
              :question="currentQuestion"
              :index="currentIndex"
              :total="questions.length"
              :is-last="currentIndex === questions.length - 1"
              @answer="handleAnswer"
              @next="handleNext"
            />
          </div>
        </div>
      </Transition>

      <!-- done screen -->
      <Transition name="fade">
        <div
          v-if="done"
          class="bg-white border border-gray-100 rounded-2xl p-8 shadow-sm flex flex-col items-center gap-4 text-center min-h-80 justify-center"
        >
          <div class="w-14 h-14 rounded-full bg-green-100 flex items-center justify-center text-green-600 text-2xl font-bold">
            ✓
          </div>
          <h2 class="text-xl font-medium text-gray-900">All done!</h2>
          <p class="text-sm text-gray-500">Your responses have been submitted.</p>
        </div>
      </Transition>
    </div>

    <!-- No Questions -->
    <div v-else class="text-center py-12">
      <p class="text-gray-600 text-lg">No questions in this survey yet</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { surveyAPI, type QuestionResponse } from '@/api/survey'
import TextQuestion          from '../components/questions/TextQuestion.vue'
import MultipleChoiceQuestion from '../components/questions/MultipleChoiceQuestion.vue'
import CheckboxQuestion      from '../components/questions/CheckboxQuestion.vue'
import RatingQuestion        from '../components/questions/RatingQuestion.vue'

interface Answer {
  questionId: string
  value: unknown
  surveyId: string
}

const route = useRoute()
const surveyId = route.params.id as string

const questions = ref<QuestionResponse[]>([])
const isLoading = ref(true)
const error = ref<string | null>(null)

function transformAnswers() {
  return answers.value.map(a => ({
    question_id: a.questionId,
    answer: Array.isArray(a.value) ? a.value : [String(a.value)]
  }))
}

onMounted(async () => {
  try {
    const questionsResponse = await surveyAPI.getQuestions(surveyId)
    questions.value = Array.isArray(questionsResponse) ? questionsResponse : []
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load questions'
    questions.value = []
  } finally {
    isLoading.value = false
  }
})

const sortedQuestions = computed(() => {
  if (!Array.isArray(questions.value)) return []
  return [...questions.value].sort((a, b) => a.order - b.order)
})

const currentIndex = ref(0)
const answers      = ref<Answer[]>([])
const done         = ref(false)

const currentQuestion = computed(() => sortedQuestions.value[currentIndex.value] || null)
const progressPct = computed(() => {
  const length = sortedQuestions.value.length
  if (length === 0) return 0

  // if done → force 100%
  if (done.value) return 100

  return Math.round(((currentIndex.value + 1) / length) * 100)
})

function handleAnswer(payload: { questionId: string; value: unknown }) {
  const i = answers.value.findIndex(a => a.questionId === payload.questionId)
  const record: Answer = { ...payload, surveyId }
  if (i >= 0) answers.value[i] = record
  else answers.value.push(record)
}

async function handleNext() {
  if (currentIndex.value < sortedQuestions.value.length - 1) {
    currentIndex.value++
    return
  }

  try {
    await surveyAPI.submitResponse(
      surveyId,
      transformAnswers()
    )

    done.value = true

  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Submit failed'
  }
}
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active { transition: all 0.22s ease; }
.slide-enter-from   { opacity: 0; transform: translateX(28px); }
.slide-leave-to     { opacity: 0; transform: translateX(-28px); }

.fade-enter-active,
.fade-leave-active  { transition: opacity 0.3s ease; }
.fade-enter-from,
.fade-leave-to      { opacity: 0; }
</style>
