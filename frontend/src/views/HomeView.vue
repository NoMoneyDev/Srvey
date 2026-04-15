<script setup lang="ts">
import { ref, computed } from 'vue'
import { type TestResult } from '@/api/testing'
import ApiTestingPanel from '@/components/ApiTestingPanel.vue'
import ApiTestingDashboard from '@/components/ApiTestingDashboard.vue'
import SurveyList from '@/components/SurveyList.vue'

const isLoading = ref(false)
const results = ref<TestResult[]>([])
const activeResult = ref<TestResult | null>(null)

const isAuthenticated = computed(() => localStorage.getItem('token') !== null)

const testEndpoint = async (action: () => Promise<TestResult>) => {
  isLoading.value = true
  try {
    const result = await action()
    results.value.unshift(result)
    activeResult.value = result
  } finally {
    isLoading.value = false
  }
}

const clearResults = () => {
  results.value = []
  activeResult.value = null
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 py-8 px-4">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-4xl font-bold text-gray-900 mb-2">Srvey - Survey Platform</h1>
        <p class="text-lg text-gray-600">
          Welcome to Srvey
        </p>
      </div>
<!-- 
      Authentication Status
      <div class="mb-6 p-4 rounded-lg" :class="isAuthenticated ? 'bg-green-50 border border-green-200' : 'bg-blue-50 border border-blue-200'">
        <p class="text-sm font-medium" :class="isAuthenticated ? 'text-green-800' : 'text-blue-800'">
          {{ isAuthenticated ? '✅ Authenticated' : '🔐 Not authenticated - Sign in to test API endpoints' }}
        </p>
      </div> -->

      <!-- Main Content -->
      <!-- <div v-if="!isAuthenticated" class="bg-white rounded-lg shadow-md p-8 text-center">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">Sign in to Get Started</h2>
        <p class="text-gray-600 mb-6">
          Use the Google Sign-in button in the navbar to authenticate and access the survey platform.
        </p>
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-6 inline-block">
          <p class="text-sm text-blue-800">
            <strong>After signing in:</strong><br />
            - Create and manage surveys<br />
            - Test API endpoints from the home page<br />
            - View survey responses and analytics
          </p>
        </div>
      </div> -->

      <!-- API Testing Section -->

        <!-- Surveys List -->
      <SurveyList />

        <!-- API Testing Tools -->
        <!-- <div class="mt-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-4">API Testing Dashboard</h2>
          <ApiTestingPanel :is-loading="isLoading" :on-test-endpoint="testEndpoint" />
          <ApiTestingDashboard
            :results="results"
            :active-result="activeResult"
            @clear="clearResults"
            @select-result="(result) => (activeResult = result)"
          />
        </div> -->
      <!-- </div> -->
    </div>
  </div>
</template>
