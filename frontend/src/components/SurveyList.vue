<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { surveyAPI, type SurveyResponse } from '@/api/survey'
import SurveyCard from './SurveyCard.vue'

const surveys = ref<SurveyResponse[]>([])
const isLoading = ref(false)
const error = ref<string | null>(null)
const currentPage = ref(1)
const pageSize = ref(10)
const totalSurveys = ref(0)

const totalPages = computed(() => Math.ceil(totalSurveys.value / pageSize.value))

const fetchSurveys = async () => {
  isLoading.value = true
  error.value = null
  try {
    const response = await surveyAPI.getSurveys(currentPage.value, pageSize.value)
    surveys.value = response.surveys || []
    totalSurveys.value = response.total || surveys.value.length
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to fetch surveys'
    surveys.value = []
  } finally {
    isLoading.value = false
  }
}

const goToPage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    fetchSurveys()
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    goToPage(currentPage.value + 1)
  }
}

const prevPage = () => {
  if (currentPage.value > 1) {
    goToPage(currentPage.value - 1)
  }
}

onMounted(() => {
  fetchSurveys()
})
</script>

<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-gray-900">Surveys</h2>
      <div class="text-sm text-gray-600">
        Showing {{ surveys.length > 0 ? (currentPage - 1) * pageSize + 1 : 0 }} -
        {{ Math.min(currentPage * pageSize, totalSurveys) }} of {{ totalSurveys }} surveys
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
      <p class="text-red-800">{{ error }}</p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-8">
      <p class="text-gray-600">Loading surveys...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="surveys.length === 0" class="text-center py-8">
      <p class="text-gray-600">No surveys found</p>
    </div>

    <!-- Surveys Grid (Card Style) -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
      <SurveyCard v-for="survey in surveys" :key="survey._id" :survey="survey" />
    </div>

    <!-- Pagination Controls -->
    <div v-if="surveys.length > 0" class="bg-gray-50 rounded-lg p-4 border border-gray-200">
      <div class="flex items-center justify-center gap-2">
        <button
          @click="prevPage"
          :disabled="currentPage === 1 || isLoading"
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition font-medium"
        >
          ← Previous
        </button>

        <div class="flex gap-1">
          <button
            v-for="page in Math.min(5, totalPages)"
            :key="page"
            @click="goToPage(page)"
            :disabled="isLoading"
            :class="[
              'px-3 py-2 rounded-lg transition font-medium',
              currentPage === page
                ? 'bg-blue-600 text-white'
                : 'bg-white border border-gray-300 hover:bg-gray-100 text-gray-900',
            ]"
          >
            {{ page }}
          </button>
          <span v-if="totalPages > 5" class="px-2 py-2 text-gray-600">...</span>
        </div>

        <button
          @click="nextPage"
          :disabled="currentPage === totalPages || isLoading"
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition font-medium"
        >
          Next →
        </button>
      </div>

      <div class="text-center mt-3 text-sm text-gray-600">
        Page <span class="font-semibold">{{ currentPage }}</span> of
        <span class="font-semibold">{{ totalPages }}</span>
        ({{ surveys.length > 0 ? (currentPage - 1) * pageSize + 1 : 0 }} -
        {{ Math.min(currentPage * pageSize, totalSurveys) }} of
        <span class="font-semibold">{{ totalSurveys }}</span> surveys)
      </div>
    </div>
  </div>
</template>
