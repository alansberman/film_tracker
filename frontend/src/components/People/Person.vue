<template>
  <div class="back shadow">
    <div class="container-fluid">
      <div class="row">
        <div class="col"></div>
        <div class="col text-center">
          <br />
          <h2>{{ person.name }}</h2>
          <br />
          <button
            type="button"
            class="btn btn-success"
            style="margin-bottom: 10px; margin-top: 10px"
          >
            <a href="{% url 'people:like' person.id %}" style="color: white"
              >Like</a
            >
          </button>
        </div>
        <div class="col"></div>
      </div>

      <div class="row">
        <div class="card body-card ">
          <div id="text">
            <div class="row">
              <div class="col">
                <div v-if="person.known_for_department">
                  <h5>Known for</h5>
                  {{ person.known_for_department }}
                  <hr />
                </div>
                <div v-if="person.place_of_birth">
                  <h5>Place of Birth</h5>
                  <p>{{ person.place_of_birth }}</p>
                  <hr />
                </div>
                <div v-if="person.biography">
                  <h5>Biography</h5>
                  <p>{{ person.biography }}</p>
                  <hr />
                </div>
              </div>
              <div class="col" v-if="person.image">
                <div class="col text-center">
                  <br />
                  <img
                    :src="person.image"
                    style="width: 500px; height: 550px"
                    alt="poster"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col">
          <h4>Film Credits</h4>
          <b-table
            striped
            bordered
            id="my-table"
            :items="filmItems"
            :head-variant="'dark'"
            :fields="filmFields"
            :per-page="perPage"
            :sort-by.sync="sortBy"
            :sort-desc.sync="sortDesc"
            :current-page="currentPageFilm"
            small
          >
            <template #cell(title)="film">
              <router-link
                :to="{ name: 'Film', params: { id: film.item.id } }"
                >{{ film.item.title }}</router-link
              >
            </template>
          </b-table>

          <b-pagination
            v-model="currentPageFilm"
            :total-rows="filmRows"
            :per-page="perPage"
            aria-controls="my-table"
          ></b-pagination>
        </div>
        <div class="col">
          <h4>TV Credits</h4>
          <b-table
            striped
            bordered
            id="my-table-tv"
            :items="tvItems"
            :head-variant="'dark'"
            :fields="tvFields"
            :per-page="perPage"
            :sort-by.sync="sortBy"
            :sort-desc.sync="sortDesc"
            :current-page="currentPageTv"
            small
          >
            <template #cell(title)="tv">
              <router-link :to="{ name: 'Film', params: { id: tv.item.id } }">{{
                tv.item.name
              }}</router-link>
            </template>
          </b-table>

          <b-pagination
            v-model="currentPageTv"
            :total-rows="tvRows"
            :per-page="perPage"
            aria-controls="my-table-tv"
          ></b-pagination>
        </div>
      </div>

      <!-- <div class="row">
      <div class="col"></div>
      <div class="col text-center">
        <br />
        <h2>{{ person.name }}</h2>
        <br />
        <button
          type="button"
          class="btn btn-success"
          style="margin-bottom: 10px; margin-top: 10px"
        >
          <a href="{% url 'people:like' person.id %}" style="color: white"
            >Like</a
          >
        </button>
      </div>
      <div class="col"></div>
    </div>
    <div class="row">
      <div class="card body-card shadow">
        <div id="text">
          <div class="row">
            <div class="col">
              <h5>Known for</h5>
              {{ person.known_for_department }}
              <hr />
              {% if person.place_of_birth %}
              <h5>Place of Birth</h5>
              <p>{{ person.place_of_birth }}</p>
              <hr />
              {% endif %} {% if person.biography %}
              <h5>Biography</h5>
              <p>{{ person.biography }}</p>
              <hr />
              {% endif %}
            </div>
            {% if person.image %}
            <div class="col">
              <div class="col text-center">
                <br />
                <img
                  :src="person.image"
                  style="width: 500px; height: 550px"
                  alt="poster"
                />
              </div>
            </div>
            {% endif %}
          </div>
          <div class="row">
            <div class="col">
              <h5>Movie Credits</h5>
              <table class="table table-striped" style="width: 100%">
                <thead class="thead-dark">
                  <tr>
                    <th scope="col">Title</th>
                    <th scope="col">Role</th>
                    <th scope="col">Average Score</th>
                    <th scope="col">Release Date</th>
                  </tr>
                </thead>
                <tbody>
                  {% for row in movie_credits %}
                  <tr>
                    <td>
                      <a :href="row.movie_url">{{ row.title }}</a>
                    </td>
                    <td>{{ row.job }}</td>
                    <td>{{ row.vote_average }}</td>
                    <td>{{ row.release_date }}</td>
                  </tr>
                  {% endfor %}
                </tbody>
              </table>
            </div>
            {% if tv_credits %}
            <div class="col">
              <h5>TV Credits</h5>
              <table class="table table-striped" style="width: 100%">
                <thead class="thead-dark">
                  <tr>
                    <th scope="col">Name</th>
                    <th scope="col">Role</th>
                    <th scope="col">No. of Episodes</th>
                    <th scope="col">Avg. Score</th>
                    <th scope="col">Original Air Date</th>
                  </tr>
                </thead>
                <tbody>
                  {% for row in tv_credits %}
                  <tr>
                    <td>
                      <a href="{% url 'shows:view' row.show_id %}">{{
                        row.name
                      }}</a>
                    </td>
                    <td>{{ row.job }}</td>
                    <td>{{ row.episode_count }}</td>
                    <td>{{ row.vote_average }}</td>
                    <td>{{ row.release_date }}</td>
                  </tr>
                  {% endfor %}
                </tbody>
              </table>
            </div>
            {% endif %} -->
    </div>
  </div>
  <!-- </div>
      </div>
    </div>
  </div> -->
</template>

<script>
import axios from "axios";
import dayjs from "dayjs";

export default {
  name: "Person.vue",
  props: ["id"],
  data() {
    return {
      person: {},
      filmCredits: {},
      tvCredits: {},
      fetchedPerson: false,
      perPage: 10,
      currentPageFilm: 1,
      currentPageTv: 1,
      filmItems: [],
      numFilms: 0,
      tvItems: [],
      tvFields: [],
      filmFields: [],
      sortBy: "averageScore",
      sortDesc: true,
    };
  },
  computed: {
    // thanks to https://github.com/vuejs/vue-router/issues/311
    getFullPath() {
      return this.$route.path;
    },
    filmRows() {
      return this.filmCredits.length;
    },
    tvRows() {
      return this.tvCredits.length;
    },
  },
  watch: {
    getFullPath() {
      this.fetchedPerson = false;
      this.fetchPerson();
    },
  },
  async mounted() {
    this.fetchPerson();
  },

  methods: {
    async fetchPerson() {
      let response = await axios.get(
        `http://localhost:8001/people/${this.$route.params.id}/view`
      );
      console.log(response);
      if (response.data) {
        this.person = response.data["person"];
        this.filmCredits = response.data["movie_credits"];
        this.tvCredits = response.data["tv_credits"];
        this.fetchedPerson = true;
        this.filmItems = this.filmCredits.map((film) => {
          return {
            title: film.title,
            averageScore: film.vote_average,
            releaseDate: this.formatDate(film.release_date),
            id: film.movie_id,
            role: film.job ? film.job : "N/A",
          };
        });
        this.filmFields = [
          { key: "title", sortable: true },
          { key: "role", sortable: false },
          { key: "averageScore", sortable: true },
          { key: "releaseDate", sortable: true },
        ];
        this.tvItems = this.tvCredits.map((show) => {
          return {
            name: show.name,
            averageScore: show.vote_average,
            episodes: show.episode_count,
            releaseDate: this.formatDate(show.release_date),
            id: show.show_id,
            role: show.job ? show.job : "N/A",
          };
        });
        this.tvFields = [
          { key: "name", sortable: true },
          { key: "role", sortable: false },
          { key: "episodes", sortable: true },
          { key: "averageScore", sortable: true },
          { key: "releaseDate", sortable: true },
        ];
      }
    },
    formatDate(date) {
      if (!date) {
        return null;
      }
      return dayjs(date).format("DD/MM/YYYY");
    },
  },
};
</script>

<style>
/* thanks https://css-tricks.com/almanac/properties/b/box-shadow/ */
.shadow {
  -webkit-box-shadow: 3px 3px 5px 6px #ccc; /* Safari 3-4, iOS 4.0.2 - 4.2, Android 2.3+ */
  -moz-box-shadow: 3px 3px 5px 6px #ccc; /* Firefox 3.5 - 3.6 */
  box-shadow: 3px 3px 5px 6px #ccc; /* Opera 10.5, IE 9, Firefox 4+, Chrome 6+, iOS 5 */
}

#text {
  padding: 10px;
}
</style>
