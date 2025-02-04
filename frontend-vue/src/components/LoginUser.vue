<template>
  <div>
    <input v-model="nim" placeholder="NIM" />
    <input v-model="email" placeholder="Email" />
    <button @click="login">Login</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      nim: "",
      email: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post("http://localhost:8000/login/", {
          nim: this.nim,
          email: this.email,
        });

        alert(response.data.message);
        this.$router.push("/verify-token");
        
      } catch (error) {
        if (error.response) {
          alert(`Error: ${error.response.data.error || "Terjadi kesalahan"}`);
        } else {
          alert("Gagal menghubungi server");
        }
      }
    },
  },
};
</script>
