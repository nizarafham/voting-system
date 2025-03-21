<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-blue-950">
    <div class="bg-white p-6 rounded-lg shadow-md w-96">
      <h2 class="text-xl font-semibold text-center mb-4">Verify Your Token</h2>

      <input
        v-model="token"
        class="w-full p-2 border border-gray-300 rounded-md focus:ring focus:ring-blue-300"
        placeholder="Enter your token"
        :disabled="isLoading"
      />
      <button
        @click="verifyToken"
        class="w-full mt-3 bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition flex items-center justify-center"
        :disabled="isLoading"
      >
        <span v-if="isLoading" class="mr-2">
          <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </span>
        {{ isLoading ? 'Verifying...' : 'Verify Token' }}
      </button>

      <p v-if="errorMessage" class="mt-3 text-red-600 text-center">
        {{ errorMessage }}
      </p>

      <p v-if="successMessage" class="mt-3 text-green-600 text-center">
        {{ successMessage }}
      </p>
    </div>
    
    <!-- Custom Modal Popup -->
    <div v-if="showFailedModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
        <h3 class="text-xl font-semibold text-center mb-4 text-red-600">Verifikasi Gagal</h3>
        <p class="text-center mb-6">
          Anda telah gagal melakukan verifikasi sebanyak 2 kali. Silakan login kembali untuk mencoba lagi.
        </p>
        <button 
          @click="redirectToLogin" 
          class="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition font-semibold"
        >
          OK
        </button>
      </div>
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
    const isLoading = ref(false);
    const showFailedModal = ref(false);
    const validSession = ref(false);

    const route = useRoute();
    const router = useRouter();

    // Get NIM from query parameter
    const nim = ref('');
    const queryToken = ref('');

    onMounted(() => {
      // Validate the session
      nim.value = route.query.nim || '';
      queryToken.value = route.query.token || '';
      
      const sessionNim = localStorage.getItem('sessionNim');
      const sessionToken = localStorage.getItem('sessionToken');
      const sessionTime = localStorage.getItem('sessionTime');
      const currentTime = new Date().getTime();
      
      // Check for session timeout (30 minutes)
      const isSessionValid = sessionTime && 
                            (currentTime - parseInt(sessionTime)) < 30 * 60 * 1000 &&
                            nim.value === sessionNim &&
                            queryToken.value === sessionToken;
      
      validSession.value = isSessionValid;
      
      if (!validSession.value) {
        errorMessage.value = 'Sesi tidak valid. Silakan login ulang.';
        setTimeout(() => {
          router.push('/');
        }, 1500);
      }
    });

    const redirectToLogin = () => {
      showFailedModal.value = false;
      
      // Clear session data
      localStorage.removeItem('isLoggedIn');
      localStorage.removeItem('sessionTime');
      localStorage.removeItem('sessionNim');
      localStorage.removeItem('sessionToken');
      
      router.push('/');
    };

    const verifyToken = async () => {
      if (isLoading.value || !validSession.value) return;
      
      errorMessage.value = '';
      successMessage.value = '';
      isLoading.value = true;

      try {
        const response = await axios.post('http://localhost:8000/verify_token/', {
          token: token.value,
          nim: nim.value,
        });

        successMessage.value = response.data.message;
        if (response.data.user) {
          // Create a secure user token for the vote page
          const userToken = generateUserToken();
          localStorage.setItem('userToken', userToken);
          localStorage.setItem('userData', JSON.stringify(response.data.user));
          
          setTimeout(() => {
            router.push(`/vote?user=${encodeURIComponent(JSON.stringify(response.data.user))}&token=${userToken}`);
          }, 1500);
        }
      } catch (error) {
        failedAttempts.value++;
        errorMessage.value = error.response?.data?.error || 'Token verification failed';

        if (failedAttempts.value >= 2) {
          showFailedModal.value = true;
        }
      } finally {
        isLoading.value = false;
      }
    };
    
    // Generate a secure token for user verification
    const generateUserToken = () => {
      return Math.random().toString(36).substring(2, 15) + 
             Math.random().toString(36).substring(2, 15);
    };

    return { 
      token, 
      verifyToken, 
      errorMessage, 
      successMessage, 
      isLoading, 
      showFailedModal,
      redirectToLogin
    };
  }
};
</script>