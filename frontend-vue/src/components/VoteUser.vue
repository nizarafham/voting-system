<template>
    <div>
      <h2>Choose your candidate:</h2>
      <div v-for="candidate in candidates" :key="candidate.id">
        <h3>{{ candidate.name }} & {{ candidate.vice_name }}</h3>
        <p><strong>Vision:</strong> {{ candidate.vision }}</p>
        <p><strong>Mission:</strong> {{ candidate.mission }}</p>
        <button @click="vote(candidate.id)">Vote</button>
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