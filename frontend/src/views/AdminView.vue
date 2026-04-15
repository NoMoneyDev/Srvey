<script setup lang="ts">
import { ref, watch } from 'vue'
import { adminAPI } from '@/api/admin'
import { surveyAPI } from '@/api/survey'

const activeTab = ref<'surveys' | 'users'>('surveys')

const surveys = ref<any[]>([])
const users = ref<any[]>([])

const questions = ref<Record<string, any[]>>({})
const expandedSurveyId = ref<string | null>(null)

const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const totalPages = ref(0)

const isLoading = ref(false)
const error = ref<string | null>(null)

/* ================= FETCH ================= */

const fetchSurveys = async () => {
  isLoading.value = true
  error.value = null

  try {
    const res = await adminAPI.getAllSurveys(page.value, pageSize.value)
    surveys.value = res.surveys || []
    total.value = res.total || 0
    totalPages.value = res.total_pages || 0
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load surveys'
  } finally {
    isLoading.value = false
  }
}

const fetchUsers = async () => {
  isLoading.value = true
  error.value = null

  try {
    const res = await adminAPI.getAllUsers(page.value, pageSize.value)
    users.value = res.users || []
    total.value = res.total || 0
    totalPages.value = res.total_pages || 0
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load users'
  } finally {
    isLoading.value = false
  }
}

/* ================= QUESTIONS ================= */

const loadQuestions = async (surveyId: string) => {
  if (questions.value[surveyId]) return

  try {
    const res = await adminAPI.getSurveyQuestions(surveyId)
    questions.value[surveyId] = res.questions || []
  } catch (err) {
    console.error(err)
  }
}

const toggleSurvey = async (id: string) => {
  if (expandedSurveyId.value === id) {
    expandedSurveyId.value = null
    return
  }

  expandedSurveyId.value = id
  await loadQuestions(id)
}

/* ================= ACTIONS ================= */

const deleteSurvey = async (id: string) => {
  if (!confirm('Delete this survey?')) return

  try {
    await adminAPI.deleteSurvey(id)
    surveys.value = surveys.value.filter(s => s.id !== id)
  } catch (err: any) {
    alert(err.message || 'Failed to delete survey')
  }
}

const deleteUser = async (userId: string) => {
  if (!confirm('Delete this user?')) return

  try {
    await adminAPI.deleteUser(userId)
    users.value = users.value.filter(u => u.id !== userId)
  } catch (err: any) {
    alert(err.message || 'Failed to delete user')
  }
}

/* ================= PAGINATION ================= */

const nextPage = () => {
  if (page.value < totalPages.value) page.value++
}

const prevPage = () => {
  if (page.value > 1) page.value--
}

/* ================= WATCH ================= */

watch([page, activeTab], () => {
  if (activeTab.value === 'surveys') fetchSurveys()
  else fetchUsers()
}, { immediate: true })
</script>

<template>
  <div class="min-h-screen bg-gray-50 py-8 px-4">
    <div class="mx-auto max-w-4xl">

      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
      </div>

      <!-- Tabs -->
      <div class="mb-6 flex gap-4">
        <button
          @click="activeTab = 'surveys'"
          :class="activeTab === 'surveys' ? 'border-black text-black' : 'border-gray-300 text-gray-500'"
          class="border-b-2 px-4 py-2 text-sm"
        >
          Surveys
        </button>

        <button
          @click="activeTab = 'users'"
          :class="activeTab === 'users' ? 'border-black text-black' : 'border-gray-300 text-gray-500'"
          class="border-b-2 px-4 py-2 text-sm"
        >
          Users
        </button>
      </div>

      <!-- Loading -->
      <div v-if="isLoading" class="py-10 text-center text-gray-500">
        Loading...
      </div>

      <!-- Error -->
      <div v-else-if="error" class="rounded border border-red-200 bg-red-50 p-4">
        <p class="text-red-700">{{ error }}</p>
      </div>

      <!-- ================= SURVEYS ================= -->
      <div v-else-if="activeTab === 'surveys'">
        <p class="mb-4 text-sm text-gray-500">{{ total }} survey(s)</p>

        <div v-if="surveys.length > 0" class="space-y-4">
          <div
            v-for="survey in surveys"
            :key="survey.id"
            @click="toggleSurvey(survey.id)"
            class="cursor-pointer rounded-lg border border-gray-100 bg-white p-4 shadow-sm hover:shadow-md transition"
          >
            <div class="flex items-start justify-between gap-4">
              <div>
                <h2 class="text-xl font-medium text-gray-900">
                  {{ survey.title }}
                </h2>

                <p v-if="survey.description" class="mt-1 text-gray-600">
                  {{ survey.description }}
                </p>

                <p class="mt-1 text-sm text-gray-500">
                  Owner: {{ survey.owner_name }}
                </p>
              </div>

              <!-- DELETE BUTTON -->
              <button
                @click.stop="deleteSurvey(survey.id)"
                class="rounded border border-red-500 px-3 py-1 text-xs text-red-500 hover:bg-red-500 hover:text-white transition"
              >
                Delete
              </button>
            </div>

            <p class="mt-3 text-sm text-gray-500">
              Created: {{ new Date(survey.created_at).toLocaleDateString() }}
            </p>

            <!-- QUESTIONS -->
            <div v-if="expandedSurveyId === survey.id" class="mt-4 border-t pt-4">
              <div v-if="!questions[survey.id]" class="text-gray-400">
                Loading questions...
              </div>

              <div v-else-if="questions[survey.id].length === 0" class="text-gray-400">
                No questions
              </div>

              <div v-else class="space-y-2">
                <div
                  v-for="q in questions[survey.id]"
                  :key="q.id"
                  class="rounded bg-gray-50 p-3"
                >
                  <p class="font-medium text-gray-900">{{ q.question }}</p>
                  <p class="text-sm text-gray-500">Type: {{ q.type }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="text-center text-gray-500">
          No surveys found
        </div>
      </div>

      <!-- ================= USERS ================= -->
      <div v-else>
        <p class="mb-4 text-sm text-gray-500">{{ total }} user(s)</p>

        <div v-if="users.length > 0" class="space-y-3">
          <div
            v-for="user in users"
            :key="user.id"
            class="flex items-center justify-between rounded border bg-white p-4"
          >
            <div>
              <p class="font-medium text-gray-900">{{ user.name }}</p>
              <p class="text-sm text-gray-500">{{ user.email }}</p>
            </div>

            <button
              @click="deleteUser(user.id)"
              class="rounded border border-red-500 px-3 py-1 text-sm text-red-500 hover:bg-red-500 hover:text-white transition"
            >
              Delete
            </button>
          </div>
        </div>

        <div v-else class="text-center text-gray-500">
          No users found
        </div>
      </div>

      <!-- Pagination -->
      <div class="flex items-center justify-between pt-6">
        <button
          @click="prevPage"
          :disabled="page === 1"
          class="rounded border border-black px-4 py-2 text-sm text-black disabled:opacity-50"
        >
          Previous
        </button>

        <div class="text-sm text-gray-600">
          Page {{ page }} / {{ totalPages }}
        </div>

        <button
          @click="nextPage"
          :disabled="page === totalPages"
          class="rounded border border-black px-4 py-2 text-sm text-black disabled:opacity-50"
        >
          Next
        </button>
      </div>

    </div>
  </div>
</template>