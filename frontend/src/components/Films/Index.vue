<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col"></div>
      <div class="col text-center">
        <br />
        <h2>My Films</h2>
        <br />
      </div>
      <div class="col"></div>
    </div>

    <div class="row" v-if="films">
      <div class="col">
        <h4>I have watched {{ rows }} films</h4>
      </div>
    </div>

    <!-- <div class="row">
      <div class="col"></div>
      <div class="col text-center">
        <button
          type="button"
          class="btn btn-success"
          style="margin-bottom: 10px; margin-top: 10px"
        >
          <router-link :to="{ name: 'Statistics', query: { added: 'True' } }"
            >Statistics</router-link
          >
        </button>
      </div>
      <div class="col"></div>
    </div> -->

    <div class="row">
      <div class="col"></div>
      <div class="col">
        <b-form-input
          id="filter-input"
          v-model="searchQuery"
          type="search"
          placeholder="Type to Search"
        ></b-form-input>
      </div>
      <div class="col"></div>
    </div>

    <div class="row">
      <b-table
        striped
        bordered
        style="margin: 50px 50px"
        id="my-table"
        :items="items"
        :head-variant="'dark'"
        :fields="fields"
        :filter="searchQuery"
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

        <template #cell(liked)="film">
          <button
            type="button"
            class="btn btn-success"
            v-if="!film.item.liked && film.item.liked !== false"
          >
            <a
              href="{% url 'films:like' row.movie_db_id %}"
              style="color: white"
              >Like</a
            >
          </button>
          <button
            type="button"
            class="btn btn-danger"
            v-if="!film.item.liked && film.item.liked !== false"
          >
            <a
              href="{% url 'films:dislike' row.movie_db_id %}"
              style="color: white"
              >Dislike</a
            >
          </button>

          <span style="color: #3eaf7c" v-if="film.item.liked">Liked</span>
          <span style="color: red" v-if="film.item.liked === false"
            >Disliked</span
          >
        </template>
      </b-table>

      <b-pagination
        style="margin-left: 50px"
        v-model="currentPage"
        :total-rows="rows"
        :per-page="perPage"
        aria-controls="my-table"
      ></b-pagination>
    </div>

    <div class="row"></div>
  </div>
</template>

<script>
import axios from "axios";
import dayjs from "dayjs";
export default {
  name: "Index.vue",
  data() {
    return {
      films: {},
      fetchedFilms: false,
      perPage: 10,
      currentPage: 1,
      items: [],
      numFilms: 0,
      fields: [],
      sortBy: "myScore",
      sortDesc: true,
      searchQuery: null,
    };
  },

  async mounted() {
    this.fetchFilms();
  },
  computed: {
    rows() {
      return this.films.length;
    },
  },

  methods: {
    async fetchFilms() {
      let response = await axios.get(`http://localhost:8001/films`, {
        headers: {
          Authorization: "Bearer " + this.$store.state.jwt,
        },
      });
      if (response.data) {
        this.films = response.data.films;
        this.items = this.films.map((film) => {
          return {
            title: film.title,
            releaseDate: film.release_date,
            averageScore: film.vote_average,
            myScore: film.score,
            liked: film.liked,
            dateWatched: this.formatDate(film.date_watched),
            id: film.movie_db_id,
          };
        });
        this.fields = [
          { key: "title", sortable: true },
          { key: "releaseDate", sortable: true },
          { key: "averageScore", sortable: true },
          { key: "myScore", sortable: true },
          { key: "dateWatched", sortable: true },
          { key: "liked", label: "Status" },
        ];
      }
    },
    formatDate(date) {
      if (!date) {
        return null;
      }
      return dayjs(date).format("YYYY-MM-DD");
    },
    searchFilms() {},
  },
};
</script>

<style></style>
