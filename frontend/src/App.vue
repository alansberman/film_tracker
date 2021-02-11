<template>
  <div id="app">
    <Header />
    <router-view />
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  text-align: center;
}

#nav {
  padding: 30px;
}

* {
  font-family: "Roboto", sans-serif;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
<script>
import Header from "./components/Header";
export default {
  components: { Header },
  computed: {
    isLoggedIn: function() {
      return this.$store.getters.isLoggedIn;
    },
  },
  methods: {
    logout: function() {
      this.$store.dispatch("logout").then(() => {
        this.$router.push("/login");
      });
    },
  },
};
</script>
