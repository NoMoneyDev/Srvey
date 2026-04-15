<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const surveyId = route.params.id as string

const API_URL = import.meta.env.VITE_API_URL

const data = ref<any>(null)
const isLoading = ref(true)
const error = ref<string | null>(null)
const isUpdating = ref(false)

async function togglePublish() {
  if (!data.value) return

  isUpdating.value = true

  try {
    const token = localStorage.getItem('token')

    const res = await fetch(`${API_URL}/survey/${surveyId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        is_published: !data.value.is_published
      })
    })

    if (!res.ok) throw new Error(`Error ${res.status}`)

    const updated = await res.json()

    data.value.is_published = updated.is_published
  } catch (err: any) {
    alert(err.message || 'Failed to update survey')
  } finally {
    isUpdating.value = false
  }
}

async function fetchAnalytics() {
  try {
    const token = localStorage.getItem('token')

    const res = await fetch(`${API_URL}/survey/${surveyId}/analytics`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!res.ok) throw new Error(`Error ${res.status}`)

    data.value = await res.json()
    data.value.is_published = data.value.is_published // for easier access in template
  } catch (err: any) {
    error.value = err.message || 'Failed to load analytics'
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchAnalytics)
</script>

<template>
  <div class="min-h-screen bg-gray-50 py-8 px-4">
    <div class="max-w-4xl mx-auto">

      <!-- Header -->
      <div class="mb-6 flex items-center justify-between">
        <h1 class="text-3xl font-bold text-gray-900">Survey Analytics</h1>

        <button
            v-if="data"
            @click="togglePublish"
            :disabled="isUpdating"
            class="rounded border border-black px-4 py-2 text-sm text-black hover:bg-black hover:text-white transition disabled:opacity-50"
        >
            {{ data?.is_published ? 'Unpublish' : 'Publish' }}
        </button>
    </div>

      <!-- Loading -->
      <div v-if="isLoading" class="text-center py-10 text-gray-500">
        Loading analytics...
      </div>

      <!-- Error -->
      <div v-else-if="error" class="p-4 bg-red-50 border border-red-200 rounded">
        <p class="text-red-700">{{ error }}</p>
      </div>

      <!-- Content -->
      <div v-else-if="data">

        <!-- Total responses -->
        <div class="mb-6 p-4 bg-white rounded shadow">
          <p class="text-lg text-gray-800">
            Total Responses:
            <span class="font-semibold">{{ data.total_responses }}</span>
          </p>
        </div>

        <!-- Questions -->
        <div
          v-for="q in data.questions"
          :key="q.question_id"
          class="mb-6 p-5 bg-white rounded shadow"
        >
          <!-- Question header -->
          <div class="mb-3">
            <h2 class="text-lg font-semibold text-gray-900">
              {{ q.question }}
            </h2>
            <p class="text-sm text-gray-500">
              Type: {{ q.type }} | Answers: {{ q.total_answers }}
            </p>
          </div>

          <!-- Multiple choice / checkbox -->
          <div v-if="['multiple_choice','checkbox'].includes(q.type)">
            <div v-if="!q.distribution || Object.keys(q.distribution).length === 0" class="text-gray-400">
              No responses
            </div>

            <div v-else class="space-y-1">
              <div
                v-for="(count, option) in q.distribution"
                :key="option"
                class="text-gray-800"
              >
                {{ option }}: {{ count }}
              </div>
            </div>
          </div>

          <!-- Rating -->
          <div v-else-if="q.type === 'rating'">
            <div v-if="q.total_answers === 0" class="text-gray-400">
              No responses
            </div>

            <div v-else class="text-gray-800 space-y-1">
              <p>Average: {{ Number(q.average).toFixed(2) }}</p>
              <p>Min: {{ q.min }}</p>
              <p>Max: {{ q.max }}</p>
            </div>
          </div>

          <!-- Text -->
          <div v-else-if="q.type === 'text'">
            <div v-if="!q.responses || q.responses.length === 0" class="text-gray-400">
              No responses
            </div>

            <ul v-else class="list-disc pl-5 space-y-1 text-gray-800 max-h-40 overflow-auto">
              <li v-for="(txt, i) in q.responses" :key="i">
                {{ txt }}
              </li>
            </ul>
          </div>

        </div>

      </div>

    </div>
  </div>
</template>

<style scoped>
</style>