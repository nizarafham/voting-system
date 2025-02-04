<template>
    <div>
      <input v-model="token" placeholder="Token" />
      <button @click="verifyToken">Verify Token</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        token: ''
      };
    },
    methods: {
      async verifyToken() {
        const response = await axios.post('http://localhost:8000/verify_token/', {
          token: this.token
        });
        alert(response.data.message);
        if (response.data.user) {
          this.$emit('verified', response.data.user);
          this.$router.push('/vote');
        } else {
          alert(response.data.message || 'Token verification failed');
        }
      }
    }
  };
  </script>