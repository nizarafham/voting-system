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
      const response = await axios.get('http://localhost:8000/candidates/');
      this.candidates = response.data;
      this.user = this.$route.params.user;
    },
    methods: {
      async vote(candidateId) {
        const response = await axios.post('http://localhost:8000/vote/', {
          user_id: this.user.id,
          candidate_id: candidateId
        });
        alert(response.data.message);
        if (response.status === 200) {
          this.$router.push('/login');
        }
      }
    }
  };
  </script>