<template>
  <div class="flex justify-end pt-2">
    <button
      class="px-6 py-2.5 rounded-xl border border-gray-200 bg-white text-sm text-gray-800 hover:bg-gray-50 active:scale-95 transition disabled:opacity-40 disabled:cursor-not-allowed"
      :disabled="disabled"
      @click="$emit('next')"
    >
      {{ isLast ? 'Submit' : 'Next →' }}
    </button>
  </div>
</template>

<script setup lang="ts">
defineProps<{ disabled?: boolean; isLast?: boolean }>()
defineEmits<{ (e: 'next'): void }>()
</script>
