<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-blue-950">
    <div class="bg-white p-6 rounded-lg shadow-md w-96">
      <h2 class="text-xl font-semibold text-center mb-4">Verify Your Token</h2>

      <input
        v-model="token"
        class="w-full p-2 border border-gray-300 rounded-md focus:ring focus:ring-blue-300"
        placeholder="Enter your token"
      />
      <button
        @click="verifyToken"
        class="w-full mt-3 bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition"
      >
        Verify Token
      </button>

      <p v-if="errorMessage" class="mt-3 text-red-600 text-center">
        {{ errorMessage }}
      </p>

      <p v-if="successMessage" class="mt-3 text-green-600 text-center">
        {{ successMessage }}
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

export default {
  setup() {
    const token = ref('');
    const errorMessage = ref('');
    const successMessage = ref('');
    const failedAttempts = ref(0);

    const route = useRoute();
    const router = useRouter();

    // Ambil nim dari query parameter
    const nim = ref('');

    onMounted(() => {
      nim.value = route.query.nim || ''; // Jika tidak ada, tetap kosong
      if (!nim.value) {
        alert('NIM tidak ditemukan. Silakan login ulang.');
        router.push('/');
      }
    });

    const verifyToken = async () => {
      errorMessage.value = '';
      successMessage.value = '';

      try {
        const response = await axios.post('http://localhost:8000/verify_token/', {
          token: token.value,
          nim: nim.value, // Kirim nim dari query parameter
        });

        successMessage.value = response.data.message;
        if (response.data.user) {
          setTimeout(() => {
            router.push(`/vote?user=${encodeURIComponent(JSON.stringify(response.data.user))}`);
          }, 1500);
        }
      } catch (error) {
        failedAttempts.value++;
        errorMessage.value = error.response?.data?.error || 'Token verification failed';

        if (failedAttempts.value >= 2) {
          setTimeout(() => {
            router.push('/');
          }, 1000);
        }
      }
    };

    return { token, verifyToken, errorMessage, successMessage };
  }
};
</script>
