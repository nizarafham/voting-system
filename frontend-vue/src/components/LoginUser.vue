<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100">
    <div class="bg-white p-6 rounded-lg shadow-md w-96">
      <h2 class="text-xl font-semibold text-center mb-4">Login</h2>

      <input
        v-model="nim"
        class="w-full p-2 border border-gray-300 rounded-md focus:ring focus:ring-blue-300"
        placeholder="NIM"
      />
      <input
        v-model="email"
        type="email"
        class="w-full mt-3 p-2 border border-gray-300 rounded-md focus:ring focus:ring-blue-300"
        placeholder="Email"
      />
      <button
        @click="login"
        class="w-full mt-3 bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition"
      >
        Login
      </button>

      <p v-if="errorMessage" class="mt-3 text-red-600 text-center">
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
      errorMessage.value = "";

      try {
        const response = await axios.post("http://localhost:8000/login/", {
          nim: nim.value,
          email: email.value,
        });

        alert(response.data.message);
        
        // Redirect ke verify-token dengan nim di query parameter
        router.push(`/verify-token?nim=${encodeURIComponent(nim.value)}`);
      } catch (error) {
        errorMessage.value = error.response?.data?.error || "Terjadi kesalahan";
      }
    };

    return { nim, email, login, errorMessage };
  },
};
</script>
