<template>
  <div class="flex flex-col gap-1">
    <span class="text-xs font-medium text-gray-400 uppercase tracking-wide">
      Question {{ index + 1 }} of {{ total }}
    </span>
    <h2 class="text-xl font-medium text-gray-900 leading-snug">
      {{ question.question }}
      <span v-if="question.required" class="text-red-400 ml-0.5">*</span>
    </h2>
  </div>
</template>

<script setup lang="ts">
defineProps<{ question: any; index: number; total: number }>()
</script>
