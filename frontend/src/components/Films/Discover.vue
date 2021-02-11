<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col"></div>
      <div class="col text-center">
        <br />
        <h2>Discover</h2>
        <br />
      </div>
      <div class="col"></div>
    </div>

    <div class="card shadow text-justify">
      <div id="text">
        <div class="row">
          <div class="col">
            <label for="start-date">Choose a start date</label>
            <b-input-group class="mb-3">
              <b-form-input
                id="start-date"
                v-model="startDate"
                placeholder="YYYY-MM-DD"
                autocomplete="off"
              ></b-form-input>
              <b-input-group-append>
                <b-form-datepicker
                  v-model="startDate"
                  button-only
                  right
                  aria-controls="start-date"
                ></b-form-datepicker>
              </b-input-group-append>
            </b-input-group>
            <br />
          </div>
          <div class="col">
            <label for="start-date">Choose an end date</label>
            <b-input-group class="mb-3">
              <b-form-input
                id="end-date"
                v-model="endDate"
                placeholder="YYYY-MM-DD"
                autocomplete="off"
              ></b-form-input>
              <b-input-group-append>
                <b-form-datepicker
                  v-model="endDate"
                  button-only
                  right
                  aria-controls="end-date"
                ></b-form-datepicker>
              </b-input-group-append>
            </b-input-group>
            <br />
          </div>
        </div>
        <div class="row">
          <div class="col"></div>
        </div>
        <div class="row">
          <div class="col">
            <div class="col text-center">
              <h6>
                Select Genre(s) <small>hold ctrl-C to select multiple</small>
              </h6>
              <b-form-select
                v-model="selectedGenres"
                :options="genreOptions"
                multiple
              ></b-form-select>
              <br /><br />
            </div>
          </div>
          <div class="col"></div>
        </div>
        <div class="row">
          <div class="col text-center">
            <b-form-group
              label="Minimum runtime"
              label-for="input-min-runtime"
              label-cols-sm="8"
              label-cols-lg="6"
            >
              <b-form-input
                id="input-min-runtime"
                v-model="minTime"
                type="number"
                min="0"
              ></b-form-input>
            </b-form-group>
          </div>
          <div class="col text-center">
            <b-form-group
              label="Maximum runtime"
              label-for="input-max-runtime"
              label-cols-sm="8"
              label-cols-lg="6"
            >
              <b-form-input
                id="input-max-runtime"
                v-model="maxTime"
                type="number"
                min="0"
              ></b-form-input>
            </b-form-group>
          </div>
        </div>
        <div class="row">
          <div class="col"></div>
          <div class="col text-center">
            <b-button variant="success" @click="discover()">Discover</b-button>
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
              <router-link
                :to="{ name: 'Film', params: { id: film.item.id } }"
                >{{ film.item.title }}</router-link
              >
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
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Discover.vue",
  data() {
    return {
      selectedGenres: [],
      genreOptions: [],
      minTime: 0,
      maxTime: 0,
      startDate: null,
      endDate: null,
      fetchedFilms: false,
      currentPage: 1,
      perPage: 10,
      items: [],
      films: [],
      fields: [],
      sortBy: "averageScore",
      sortDesc: true,
    };
  },
  async mounted() {
    this.setup();
  },
  computed: {
    rows() {
      return this.films.length;
    },
  },
  methods: {
    async discover() {
      this.fetchedFilms = false;
      let constraints = {};

      if (this.startDate) {
        constraints = Object.assign({}, constraints, {
          "primary_release_date.gte": this.startDate,
        });
      }

      if (this.endDate) {
        constraints = Object.assign({}, constraints, {
          "primary_release_date.lte": this.endDate,
        });
      }

      if (this.minTime) {
        constraints = Object.assign({}, constraints, {
          "with_runtime.gte": this.minTime,
        });
      }

      if (this.maxTime) {
        constraints = Object.assign({}, constraints, {
          "with_runtime.lte": this.maxTime,
        });
      }

      if (this.selectedGenres && this.selectedGenres.length > 0) {
        constraints = Object.assign({}, constraints, {
          with_genres: this.selectedGenres.join("&"),
        });
      }
      let response = await axios.get(`http://localhost:8001/films/discover`, {
        params: constraints,
      });

      console.log(response);
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
    async setup() {
      let genre_response = await axios.get(
        `http://localhost:8001/films/genres`
      );
      this.genreOptions = genre_response["data"]["genres"].map((genre) => {
        return {
          value: genre["id"],
          text: genre["name"],
        };
      });
    },
  },
};
</script>

<style></style>
