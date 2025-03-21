<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-blue-950">
    <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
      <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Login</h2>

      <div class="space-y-4">
        <input
          v-model="nim"
          class="w-full p-3 border border-gray-300 rounded-md focus:ring focus:ring-blue-400"
          placeholder="NIM"
          :disabled="isLoading"
        />
        <input
          v-model="email"
          type="email"
          class="w-full p-3 border border-gray-300 rounded-md focus:ring focus:ring-blue-400"
          placeholder="Email"
          :disabled="isLoading"
        />
      </div>

      <button
        @click="login"
        class="w-full mt-5 bg-blue-600 text-white py-3 rounded-md hover:bg-blue-700 transition font-semibold flex items-center justify-center"
        :disabled="isLoading"
      >
        <span v-if="isLoading" class="mr-2">
          <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </span>
        {{ isLoading ? 'Logging in...' : 'Login' }}
      </button>

      <p v-if="errorMessage" class="mt-4 text-red-600 text-center">
        {{ errorMessage }}
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

export default {
  setup() {
    const nim = ref("");
    const email = ref("");
    const errorMessage = ref("");
    const isLoading = ref(false);
    const router = useRouter();

    // Clear any previous session data on component mount
    onMounted(() => {
      // Clear previous session data when visiting login page
      localStorage.removeItem('isLoggedIn');
      localStorage.removeItem('sessionTime');
      localStorage.removeItem('sessionNim');
    });

    const login = async () => {
      if (isLoading.value) return;
      
      // Basic validation
      if (!nim.value || !email.value) {
        errorMessage.value = "NIM dan Email harus diisi";
        return;
      }
      
      errorMessage.value = "";
      isLoading.value = true;
      
      try {
        // eslint-disable-next-line
        const response = await axios.post("http://localhost:8000/login/", { 
          nim: nim.value,
          email: email.value,
        });
        
        // Store session information
        localStorage.setItem('isLoggedIn', 'true');
        localStorage.setItem('sessionTime', new Date().getTime().toString());
        localStorage.setItem('sessionNim', nim.value);
        
        // Create a session token with random value for additional security
        const sessionToken = generateSessionToken();
        localStorage.setItem('sessionToken', sessionToken);
        
        router.push(`/verify-token?nim=${encodeURIComponent(nim.value)}&token=${sessionToken}`);
      } catch (error) {
        errorMessage.value = error.response?.data?.error || "Terjadi kesalahan";
      } finally {
        isLoading.value = false;
      }
    };
    
    // Generate a random session token
    const generateSessionToken = () => {
      return Math.random().toString(36).substring(2, 15) + 
             Math.random().toString(36).substring(2, 15);
    };
    
    return { nim, email, login, errorMessage, isLoading };
  },
};
</script>