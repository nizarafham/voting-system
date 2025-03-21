<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-blue-950">
    <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-2xl">
      <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Choose your candidate:</h2>
      <div class="flex flex-wrap -mx-4">
        <div
          v-for="candidate in candidates"
          :key="candidate.id"
          class="w-full md:w-1/2 px-4 mb-8"
        >
          <div class="border p-6 rounded-md flex flex-col justify-between h-full">
            <div>
              <h3 class="text-xl font-semibold mb-3">
                {{ candidate.name }} & {{ candidate.vice_name }}
              </h3>
              <p class="mb-2"><strong>Vision:</strong> {{ candidate.vision }}</p>
              <p class="mb-3"><strong>Mission:</strong> {{ candidate.mission }}</p>
            </div>
            <div class="flex justify-center">
              <button
                @click="vote(candidate.id)"
                class="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition flex items-center justify-center"
                :disabled="isVoting"
              >
                <span v-if="isVoting && votingCandidateId === candidate.id" class="mr-2">
                  <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </span>
                {{ isVoting && votingCandidateId === candidate.id ? 'Voting...' : 'Vote' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Vote Result Modal -->
    <div v-if="showResultModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
        <h3 class="text-xl font-semibold text-center mb-4" :class="voteSuccess ? 'text-green-600' : 'text-red-600'">
          {{ voteSuccess ? 'Vote Successfully Cast' : 'Vote Failed' }}
        </h3>
        <p class="text-center mb-6">
          {{ voteMessage }}
        </p>
        <button 
          @click="closeModal" 
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
    const candidates = ref([]);
    const user = ref(null);
    const isVoting = ref(false);
    const votingCandidateId = ref(null);
    const showResultModal = ref(false);
    const voteSuccess = ref(false);
    const voteMessage = ref('');
    const validSession = ref(false);
    
    const route = useRoute();
    const router = useRouter();
    
    onMounted(async () => {
      // Validate the session
      const queryToken = route.query.token || '';
      const userToken = localStorage.getItem('userToken');
      const storedUserData = localStorage.getItem('userData');
      const sessionTime = localStorage.getItem('sessionTime');
      const currentTime = new Date().getTime();
      
      // Check for session timeout (30 minutes) and token match
      const isSessionValid = sessionTime && 
                            (currentTime - parseInt(sessionTime)) < 30 * 60 * 1000 &&
                            queryToken === userToken;
      
      validSession.value = isSessionValid;
      
      if (!validSession.value) {
        router.push('/');
        return;
      }
      
      try {
        // Get user data from query or localStorage
        if (route.query.user) {
          try {
            user.value = JSON.parse(decodeURIComponent(route.query.user));
          } catch (e) {
            // If parsing fails, try getting from localStorage
            if (storedUserData) {
              user.value = JSON.parse(storedUserData);
            } else {
              router.push('/');
              return;
            }
          }
        } else if (storedUserData) {
          user.value = JSON.parse(storedUserData);
        } else {
          router.push('/');
          return;
        }
        
        // Fetch candidates
        const response = await axios.get('http://localhost:8000/candidates/');
        candidates.value = response.data;
      } catch (error) {
        console.error("Error loading data:", error);
        router.push('/');
      }
    });
    
    const vote = async (candidateId) => {
      if (isVoting.value || !validSession.value) return;
      
      isVoting.value = true;
      votingCandidateId.value = candidateId;
      
      try {
        const response = await axios.post(
          'http://localhost:8000/vote/',
          {
            nim: user.value.nim, 
            candidate_id: candidateId
          },
          {
            headers: {
              'Content-Type': 'application/json'
            }
          }
        );
        
        voteSuccess.value = true;
        voteMessage.value = response.data.message || 'Your vote has been recorded successfully.';
        showResultModal.value = true;
      } catch (error) {
        voteSuccess.value = false;
        voteMessage.value = error.response?.data?.message || "Terjadi kesalahan saat voting";
        showResultModal.value = true;
      } finally {
        isVoting.value = false;
      }
    };
    
    const closeModal = () => {
      showResultModal.value = false;
      if (voteSuccess.value) {
        // Clear all session data after successful vote
        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('sessionTime');
        localStorage.removeItem('sessionNim');
        localStorage.removeItem('sessionToken');
        localStorage.removeItem('userToken');
        localStorage.removeItem('userData');
        
        router.push('/');
      }
    };
    
    return {
      candidates,
      isVoting,
      votingCandidateId,
      showResultModal,
      voteSuccess,
      voteMessage,
      vote,
      closeModal
    };
  }
};
</script>