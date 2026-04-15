<script setup lang="ts">
import { RouterLink, useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import { GoogleSignInButton, type CredentialResponse } from 'vue3-google-signin'
import { RegisterUser } from '@/api/user'

const router = useRouter()
const userPicture = ref<string | null>(null)
const dropdownOpen = ref(false)

onMounted(() => {
  userPicture.value = localStorage.getItem("user_picture")
})

const handleLoginSuccess = async (response: CredentialResponse) => {
  await RegisterUser(response.credential ?? '')
  userPicture.value = localStorage.getItem("user_picture")
}

const toggleDropdown = () => dropdownOpen.value = !dropdownOpen.value

const logout = () => {
  localStorage.removeItem("token")
  localStorage.removeItem("user_picture")
  localStorage.removeItem("user_name")
  userPicture.value = null
  dropdownOpen.value = false
  router.push("/")
}
</script>

<template>
  <nav class="w-full bg-slate-900 px-8 py-4 flex items-center justify-between shadow-md">
    <div class="text-2xl font-bold text-white">Srvey</div>

    <div class="flex gap-8 items-center">
      <RouterLink to="/" class="text-white no-underline transition-colors duration-300 hover:text-blue-500">Home</RouterLink>
      <RouterLink
        v-if="userPicture"
        to="/surveys/create"
        class="text-white no-underline transition-colors duration-300 hover:text-blue-500"
      >
        Create Survey
      </RouterLink>

      <RouterLink
        v-if="userPicture"
        to="/analytics"
        class="text-white no-underline transition-colors duration-300 hover:text-blue-500"
      >
        My Surveys
      </RouterLink>

      <GoogleSignInButton
        v-if="!userPicture"
        @success="handleLoginSuccess"
        size="medium"
        shape="pill"
        theme="outline"
      />

      <div v-else class="relative">
        <img
          :src="userPicture"
          @click="toggleDropdown"
          class="w-9 h-9 rounded-full cursor-pointer ring-2 ring-white hover:ring-blue-500 transition-all"
          referrerpolicy="no-referrer"
        />
        <div v-if="dropdownOpen" class="absolute right-0 mt-2 w-36 bg-white rounded-lg shadow-lg overflow-hidden z-50">
          <button @click="logout" class="w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 text-left transition-colors">
            Logout
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>