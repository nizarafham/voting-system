<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      socket: null
    };
  },
  mounted() {
    this.socket = new WebSocket("wss://192.168.2.11:8000/ws/");

    this.socket.onopen = () => {
      console.log("WebSocket Connected");
    };

    this.socket.onmessage = (event) => {
      console.log("Message from server:", event.data);
    };

    this.socket.onerror = (error) => {
      console.error("WebSocket Error:", error);
    };

    this.socket.onclose = () => {
      console.log("WebSocket Closed");
    };
  },
};
</script>
