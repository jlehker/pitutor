<template>
  <div class="logs">
    <div>
      <h1 class="font-weight-light">Feed Report</h1>
      <v-card>
        <v-data-table
          :headers="headers"
          :items="reportItems"
          item-key="id"
          dark
        >
          <template v-slot:item="{ item }">
            <tr>
              <td>{{ item.name }}</td>
              <td>{{ item.timestamp }}</td>
            </tr>
          </template>
        </v-data-table>
      </v-card>
    </div>
  </div>
</template>

<script>
export default {
  name: "Logs",
  data: () => ({
    headers: [
      {
        text: "Logs",
        align: "left",
        sortable: false,
        value: "name",
      },
      { text: "Event Name", value: "name" },
      { text: "Timestamp", value: "timestamp" },
    ],
    reportItems: [],
  }),
  created() {
    this.timer = setInterval(this.getEvents, 1500);
  },
  beforeDestroy() {
    clearInterval(this.timer);
  },
  methods: {
    async getEvents() {
      await this.axios
        .get("http://raspberrypi.home:8000/api/events")
        .then((res) => (this.reportItems = res.data));
    },
  },
};
</script>
