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
                class="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition"
              >
                Vote
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        candidates: [],
        user: null
      };
    },
    async created() {
      if (!localStorage.getItem('isLoggedIn')) {
        window.location.href = '/'; 
      }
      const response = await axios.get('http://localhost:8000/candidates/');
      this.candidates = response.data;
      this.user = this.$route.query.user ? JSON.parse(this.$route.query.user) : null;
    },
    methods: {
      async vote(candidateId) {
      try {
        const response = await axios.post(
          'http://localhost:8000/vote/',
          {
            nim: this.user.nim, 
            candidate_id: candidateId
          },
          {
            headers: {
              'Content-Type': 'application/json'
            }
          }
        );
        alert(response.data.message);
        if (response.status === 200) {
          this.$router.push('/'); // ini path login
        }
      } catch (error) {
        console.error("Error saat voting:", error.response?.data?.message || "Terjadi kesalahan saat voting");
        alert(error.response?.data?.message || "Terjadi kesalahan saat voting");
      }
    }
}
  };
  </script>