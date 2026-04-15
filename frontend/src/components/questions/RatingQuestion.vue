<template>
  <div class="flex flex-col flex-1 h-full gap-5">

    <!-- Title -->
    <div>
      <p class="text-sm text-gray-400">
        Question {{ index + 1 }} of {{ total }}
      </p>
      <h2 class="text-xl font-semibold text-gray-900">
        {{ question.question }}
      </h2>
    </div>

    <!-- Center content (grows) -->
    <div class="flex flex-col flex-1 justify-center gap-5">

      <div class="text-center text-5xl select-none">
        {{ emoji }}
      </div>

      <div class="text-center">
        <span class="text-4xl font-medium text-gray-900">{{ displayValue }}</span>
        <span class="text-base text-gray-400"> / {{ max }}</span>
      </div>

      <div class="flex items-center gap-3">
        <span class="text-sm text-gray-400 w-5 text-center">{{ min }}</span>

        <input
          type="range"
          :min="min"
          :max="max"
          v-model.number="rawValue"
          step="0.1"
          class="flex-1 accent-indigo-500"
        />

        <span class="text-sm text-gray-400 w-5 text-center">{{ max }}</span>
      </div>

    </div>

    <!-- Button -->
    <button
      @click="submit"
      class="mt-auto px-6 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white transition"
    >
      {{ isLast ? 'Submit' : 'Next' }}
    </button>

  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{
  question: any
  index: number
  total: number
  isLast?: boolean
}>()

const emit = defineEmits<{
  (e: 'answer', payload: { questionId: string; value: number }): void
  (e: 'next'): void
}>()

// Data shape: choices[0] = min value, choices[1] = max value
// e.g. choices: ["1", "10"]
const min = computed(() => Number(props.question.choices[0]) || 1)
const max = computed(() => Number(props.question.choices[1]) || 10)

const rawValue    = ref((min.value + max.value) / 2)
const displayValue = computed(() => rawValue.value.toFixed(1))

const emoji = computed(() => {
  const pct = (rawValue.value - min.value) / (max.value - min.value)
  if (pct < 0.2) return '😢'
  if (pct < 0.4) return '😕'
  if (pct < 0.6) return '😐'
  if (pct < 0.8) return '🙂'
  return '😄'
})

function submit() {
  emit('answer', { questionId: props.question._id, value: rawValue.value })
  emit('next')
}
</script>
