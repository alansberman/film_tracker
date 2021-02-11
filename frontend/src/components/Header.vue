<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <span class="navbar-brand">Filmtracker</span>
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarNavDropdown"
        aria-controls="navbarNavDropdown"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavDropdown">
        <ul class="navbar-nav">
          <li class="nav-item">
            <div class="nav-link">
              <router-link to="/films">Home</router-link>
            </div>
          </li>
          <li class="nav-item">
            <div class="nav-link">
              <router-link to="/films">Films</router-link>
            </div>
          </li>
          <li class="nav-item">
            <div class="nav-link">
              <router-link to="/films/statistics">Statistics</router-link>
            </div>
          </li>
          <li class="nav-item">
            <div class="nav-link">
              <router-link to="/films/discover">Discover</router-link>
            </div>
          </li>
        </ul>
      </div>
      <form class="form-inline">
        <input
          class="form-control mr-sm-2"
          type="search"
          v-model="query"
          placeholder="Search"
          aria-label="Search"
        />
        <router-link :to="{ name: 'Search', query: { query: query } }">
          <button class="btn btn-outline-success my-2 my-sm-0">
            Search
          </button>
        </router-link>
      </form>
      <div>w</div>
      <div v-if="this.$store.state.jwt && this.$store.state.jwt.length > 0">
        <button
          class="btn btn-outline-success my-2 my-sm-0"
          v-on:click="logout"
        >
          Logout
        </button>
      </div>
    </nav>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Header.vue",
  data() {
    return {
      query: "",
    };
  },
  methods: {
    async logout() {
      await axios.get(`http://localhost:8001/auth/logout`, {
        headers: {
          Authorization: "Bearer " + this.$store.state.jwt,
        },
      });
      this.$store.commit("removeToken");

      this.$router.push({ name: "Login" });
    },
  },
};
</script>

<style></style>
