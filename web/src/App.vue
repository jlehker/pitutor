<template>
  <v-app>
    <v-card width="450" class="mx-auto mt-5">
      <v-card-title class="pb-0">
        <h1>PetTutor Control</h1>
      </v-card-title>
      <v-card-text>Status: {{ status }}</v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-btn color="info" @click="feed()">Manual Feed</v-btn>
        <v-btn color="success">Start Schedule</v-btn>
        <v-btn color="error">Stop Schedule</v-btn>
      </v-card-actions>
    </v-card>
  </v-app>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      status: ''
    };
  },
  created() {
    this.timer = setInterval(this.getStatus(), 100)
  }
  methods: {
    async feed() {
      await this.axios.get("http://raspberrypi.home:8000/feed");
    },
    getStatus() {
      await this.axios.get("http://raspberrypi.home:8000/api/status").then(res => this.status = res.data.status);
    }
  },
  beforeDestroy () {
      clearInterval(this.timer)
  }
};
</script>