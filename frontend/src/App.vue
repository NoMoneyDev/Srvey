<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
</script>

<template>
  <div class="flex flex-col min-h-screen w-full">
    <header class="flex-shrink-0 w-full">
      <Navbar />
    </header>

    <main class="flex-1 w-full overflow-y-auto">
      <RouterView />
    </main>
  </div>
</template>