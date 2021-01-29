<template>
  <div id="app">
    <v-app>
      <v-app-bar app color="grey darken-4" dark>
        <v-app-bar-nav-icon
          @click.stop="sidebarMenu = !sidebarMenu"
        ></v-app-bar-nav-icon>
        <v-toolbar-title>Dashboard</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-icon>mdi-account</v-icon>
      </v-app-bar>
      <v-navigation-drawer
        v-model="sidebarMenu"
        app
        floating
        :permanent="sidebarMenu"
        :mini-variant.sync="mini"
        color="grey darken-4"
      >
        <v-list dense>
          <v-list-item>
            <v-list-item-action>
              <v-icon @click.stop="sidebarMenu = !sidebarMenu"
                >mdi-chevron-left</v-icon
              >
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
        <v-list-item class="px-2" @click="toggleMini = !toggleMini">
          <v-list-item-avatar>
            <v-icon>mdi-account-outline</v-icon>
          </v-list-item-avatar>
          <v-list-item-content class="text-truncate"> - </v-list-item-content>
          <v-btn icon small>
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
        </v-list-item>
        <v-divider></v-divider>
        <v-list>
          <v-list-item
            v-for="item in items"
            :key="item.title"
            link
            :to="item.href"
          >
            <v-list-item-icon>
              <v-icon color="primary">{{ item.icon }}</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title class="primary--text">{{
                item.title
              }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
      <v-content>
        <v-container class="px-4 py-0 fill-height" fluid>
          <v-row class="fill-height">
            <v-col>
              <transition name="fade">
                <router-view></router-view>
              </transition>
            </v-col>
          </v-row>
        </v-container>
        <v-footer app color="grey darken-4" class="py-3">
          <span class="ml-auto overline">PiTutor &copy;2021</span>
        </v-footer>
      </v-content>
    </v-app>
  </div>
</template>

<style lang="scss">
.theme--dark.v-application {
  background-color: #181818;
}

.theme--dark.v-card,
.theme--dark.v-data-table,
.theme--dark.v-tabs-items,
.theme--dark.v-tabs .v-tabs-bar {
  background-color: #232323;
}

.fade-enter-active,
.fade-leave-active {
  transition-property: opacity;
  transition-duration: 0.25s;
}

.fade-enter-active {
  transition-delay: 0.25s;
}

.fade-enter,
.fade-leave-active {
  opacity: 0;
}

::-webkit-scrollbar {
  width: 8px;
  background-color: #111;
}

::-webkit-scrollbar-thumb {
  background-color: #222;
}

::-webkit-scrollbar-thumb:hover {
  background-color: #444;
}

::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 4px rgba(0, 0, 0, 0.6);
  background-color: #333;
}

::-webkit-scrollbar-track:hover {
  background-color: #292929;
}
</style>
<script>
export default {
  name: "App",
  computed: {
    mini() {
      return this.$vuetify.breakpoint.smAndDown || this.toggleMini;
    },
  },
  data: () => ({
    sidebarMenu: true,
    toggleMini: false,
    items: [
      { title: "Home", href: "/", icon: "mdi-home-outline" },
      { title: "Logs", href: "/logs", icon: "mdi-format-list-bulleted" },
      { title: "Schedule", href: "/schedule", icon: "mdi-alarm" },
      { title: "Settings", href: "/settings", icon: "mdi-cog-outline" },
      { title: "Alerts", href: "/alerts", icon: "mdi-alarm-light-outline" },
      { title: "About", href: "/about", icon: "mdi-information-outline" },
    ],
  }),
};
</script>