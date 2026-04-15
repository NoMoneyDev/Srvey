<template>
  <div class="flex flex-col flex-1 h-full gap-5">

    <!-- Question Title -->
    <div>
      <p class="text-sm text-gray-400">
        Question {{ index + 1 }} of {{ total }}
      </p>
      <h2 class="text-xl font-semibold text-gray-900">
        {{ question.question }}
      </h2>
    </div>

    <!-- Input -->
    <textarea
      v-model="answer"
      class="flex-1 w-full px-4 py-3 text-sm rounded-xl border border-gray-200 bg-gray-50 text-gray-900 resize-none outline-none focus:border-indigo-400 focus:bg-white transition font-sans leading-relaxed"
      placeholder="Type your answer here…"
    />

    <!-- Button -->
    <button
      @click="submit"
      :disabled="question.required && !answer.trim()"
      class="mt-auto px-6 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white disabled:bg-gray-300 disabled:cursor-not-allowed transition"
    >
      Next
    </button>

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  question: any
  index: number
  total: number
}>()

const emit = defineEmits<{
  (e: 'answer', payload: { questionId: string; value: string }): void
  (e: 'next'): void
}>()

const answer = ref('')

function submit() {
  emit('answer', { questionId: props.question._id, value: answer.value })
  emit('next')
}
</script>