<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-blue-950">
    <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
      <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Login</h2>

      <div class="space-y-4">
        <input
          v-model="nim"
          class="w-full p-3 border border-gray-300 rounded-md focus:ring focus:ring-blue-400"
          placeholder="NIM"
        />
        <input
          v-model="email"
          type="email"
          class="w-full p-3 border border-gray-300 rounded-md focus:ring focus:ring-blue-400"
          placeholder="Email"
        />
      </div>

      <button
        @click="login"
        class="w-full mt-5 bg-blue-600 text-white py-3 rounded-md hover:bg-blue-700 transition font-semibold"
      >
        Login
      </button>

      <p v-if="errorMessage" class="mt-4 text-red-600 text-center">
        {{ errorMessage }}
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref } from "vue";
import { useRouter } from "vue-router";

export default {
  setup() {
    const nim = ref("");
    const email = ref("");
    const errorMessage = ref("");
    const router = useRouter();

    const login = async () => {
      try {
        const response = await axios.post("http://localhost:8000/login/", {
          nim: nim.value,
          email: email.value,
        });
        
        localStorage.setItem('isLoggedIn', 'true');
        alert(response.data.message);
        router.push(`/verify-token?nim=${encodeURIComponent(nim.value)}`);
      } catch (error) {
        errorMessage.value = error.response?.data?.error || "Terjadi kesalahan";
      }
    };
    return { nim, email, login, errorMessage };
  },
};
</script>
