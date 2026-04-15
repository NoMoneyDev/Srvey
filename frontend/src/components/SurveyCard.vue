<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { SurveyResponse } from '@/api/survey'

interface Props {
  survey: SurveyResponse
}

const props = defineProps<Props>()
const router = useRouter()

const handleClick = () => {
  router.push(`/surveys/${props.survey._id}/take`)
}
</script>

<template>
  <div
    class="bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-gray-200 rounded-lg p-6 hover:shadow-lg hover:border-blue-400 transition cursor-pointer transform hover:scale-105"
    @click="handleClick"
  >
    <!-- Card Header -->
    <div class="mb-3">
      <h3 class="text-lg font-bold text-gray-900 line-clamp-2">{{ survey.title }}</h3>
    </div>

    <!-- Card Body -->
    <p v-if="survey.description" class="text-sm text-gray-700 mb-4 line-clamp-3">
      {{ survey.description }}
    </p>

    <!-- Card Footer with Metadata -->
    <div class="border-t border-gray-300 pt-4 space-y-2 text-xs text-gray-600">
      <div class="flex items-center justify-between">
        <span class="font-medium">Creator:</span>
        <span class="text-gray-800">{{ survey.created_by }}</span>
      </div>
      <div class="flex items-center justify-between">
        <span class="font-medium">Created:</span>
        <span class="text-gray-800">{{ new Date(survey.created_at).toLocaleDateString() }}</span>
      </div>
    </div>

    <!-- Call to Action -->
    <div class="mt-4 pt-4 border-t border-gray-300">
      <div class="text-center text-sm text-blue-600 font-semibold hover:text-blue-800">
        View Survey →
      </div>
    </div>
  </div>
</template>
