<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { surveyAPI } from '@/api/survey'

const router = useRouter()

const surveys = ref<any[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const totalPages = ref(0)

const isLoading = ref(false)
const error = ref<string | null>(null)

const fetchSurveys = async () => {
  isLoading.value = true
  error.value = null

  try {
    const res = await surveyAPI.getMySurveys(page.value, pageSize.value)
    surveys.value = res.surveys || []
    total.value = res.total || 0
    totalPages.value = res.total_pages || 0
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to load your surveys'
  } finally {
    isLoading.value = false
  }
}

const goToAnalytics = (id: string) => {
  router.push(`/analytics/${id}`)
}

const nextPage = () => {
  if (page.value < totalPages.value) {
    page.value++
  }
}

const prevPage = () => {
  if (page.value > 1) {
    page.value--
  }
}

watch(page, fetchSurveys, { immediate: true })
</script>

<template>
  <div class="min-h-screen bg-gray-50 py-8 px-4">
    <div class="mx-auto max-w-4xl">
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-900">My Surveys</h1>
        <p class="mt-1 text-sm text-gray-500">{{ total }} survey(s)</p>
      </div>

      <div v-if="isLoading" class="py-10 text-center text-gray-500">
        Loading your surveys...
      </div>

      <div v-else-if="error" class="rounded border border-red-200 bg-red-50 p-4">
        <p class="text-red-700">{{ error }}</p>
      </div>

      <div v-else-if="surveys.length > 0" class="space-y-4">
        <div
            v-for="survey in surveys"
            :key="survey.id"
            @click="goToAnalytics(survey._id)"
            class="cursor-pointer rounded-lg border border-gray-100 bg-white p-4 shadow-sm transition-shadow duration-300 hover:shadow-md"
        >
          <div class="flex items-start justify-between gap-4">
            <div>
              <h2 class="text-xl font-medium text-gray-900">{{ survey.title }}</h2>
              <p v-if="survey.description" class="mt-1 text-gray-600">
                {{ survey.description }}
              </p>
            </div>

            <span
              class="shrink-0 rounded-full px-3 py-1 text-xs font-medium"
              :class="survey.is_published ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'"
            >
              {{ survey.is_published ? 'Published' : 'Draft' }}
            </span>
          </div>

          <p class="mt-3 text-sm text-gray-500">
            Created: {{ new Date(survey.created_at).toLocaleDateString() }}
          </p>
        </div>
      </div>

      <div v-else class="rounded-lg border border-dashed border-gray-300 bg-white p-10 text-center">
        <p class="text-gray-600">You do not have any surveys yet.</p>
      </div>

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