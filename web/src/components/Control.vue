<template>
  <div>
    <v-row>
      <v-col lg="4" cols="sm" class="pb-2">
        <v-card>
          <v-row class="no-gutters">
            <div class="col-auto">
              <div class="cyan fill-height">&nbsp;</div>
            </div>
            <div class="col pa-3 py-4 cyan--text">
              <h5 class="text-truncate text-uppercase">Bluetooth Status</h5>
              <h1>{{ status.bluetooth }}</h1>
            </div>
          </v-row>
        </v-card>
      </v-col>
      <v-col lg="4" cols="sm" class="pb-2">
        <v-card>
          <v-row class="no-gutters">
            <div class="col-auto">
              <div class="primary fill-height">&nbsp;</div>
            </div>
            <div class="col pa-3 py-4 primary--text">
              <h5 class="text-truncate text-uppercase">Schedule</h5>
              <h1>{{ status.schedule }}</h1>
            </div>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col lg="4" cols="md" class="pb-2">
        <v-card min-height="131">
          <v-card-title class="font-weight-light text-truncate primary--text">
            Manual Control
          </v-card-title>
          <v-card-actions>
            <v-btn @click="feed()" rounded color="primary"> Feed </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col lg="4" cols="md" class="pb-2">
        <v-card min-height="131">
          <v-card-title class="font-weight-light text-truncate success--text">
            Schedule
          </v-card-title>
          <v-card-actions>
            <v-btn @click="startSchedule()" outlined rounded color="success">
              Start
            </v-btn>
            <v-btn @click="stopSchedule()" rounded color="error"> Stop </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: "Control",
  data() {
    return {
      status: "",
    };
  },
  created() {
    this.timer = setInterval(this.getStatus, 1500);
  },
  beforeDestroy() {
    clearInterval(this.timer);
  },
  methods: {
    async feed() {
      await this.axios.post("https://pitutor.home/api/feed");
    },
    async startSchedule() {
      await this.axios.post("https://pitutor.home/api/schedule/start");
    },
    async stopSchedule() {
      await this.axios.post("https://pitutor.home/api/schedule/stop");
    },
    getStatus() {
      this.axios
        .get("https://pitutor.home/api/status")
        .then((res) => (this.status = res.data));
    },
  },
};
</script>
