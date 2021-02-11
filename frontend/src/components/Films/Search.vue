<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col"></div>
      <div class="col">
        <br />
        <h2>Search Film</h2>
      </div>
      <div class="col"></div>
    </div>
    <div class="row" v-if="fetchedFilms">
      <div class="col"></div>
      <div class="col">
        <h5>Search Results for "{{ query }}":</h5>
      </div>
      <div class="col"></div>
    </div>
    <div class="row" v-if="fetchedFilms">
      <b-table
        striped
        bordered
        style="margin: 50px 50px"
        id="my-table"
        :items="items"
        :head-variant="'dark'"
        :fields="fields"
        :per-page="perPage"
        :sort-by.sync="sortBy"
        :sort-desc.sync="sortDesc"
        :current-page="currentPage"
        small
      >
        <template #cell(title)="film">
          <router-link :to="{ name: 'Film', params: { id: film.item.id } }">{{
            film.item.title
          }}</router-link>
        </template>
      </b-table>

      <div>
        <b-pagination
          style="margin-left: 50px"
          v-model="currentPage"
          :total-rows="rows"
          :per-page="perPage"
          aria-controls="my-table"
        ></b-pagination>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
// import dayjs from "dayjs";
export default {
  name: "Search.vue",
  data() {
    return {
      results: {},
      fetchedFilms: false,
      query: "",
      currentPage: 1,
      perPage: 10,
      items: [],
      films: [],
      fields: [],
      sortBy: "averageScore",
      sortDesc: true,
    };
  },
  computed: {
    rows() {
      return this.films.length;
    },
  },
  mounted() {
    this.query = this.$route.query["query"];
    this.search();
  },
  methods: {
    async search() {
      let response = await axios.get(`http://localhost:8001/films/search`, {
        params: { query: this.query },
        headers: {
          Authorization: "Bearer " + this.$store.state.jwt,
        },
      });
      this.parseFilms(response.data.films);
    },
    parseFilms(films) {
      this.films = films;
      const items = films.map((film) => {
        if (film) {
          return {
            title: film["title"],
            releaseDate: film.release_date,
            averageScore: film.vote_average,
            id: film.id,
          };
        }
        return null;
      });
      items.forEach((item) => {
        if (item !== null) {
          this.items.push(item);
        }
      });
      this.fields = [
        { key: "title", sortable: true },
        { key: "releaseDate", sortable: true },
        { key: "averageScore", sortable: true },
      ];
      this.fetchedFilms = true;
    },
  },
};
</script>

<style></style>
