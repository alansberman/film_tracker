<template>
  <div class="container-fluid" v-if="fetchedFilm">
    <div class="row">
      <div class="col"></div>
      <div class="col text-center ">
        <br />

        <h2>{{ data.film.title }}</h2>
        <button
          v-if="!data.watched && !data.wishlisted"
          type="button"
          class="btn btn-info"
          style="margin-bottom: 10px; margin-top: 10px"
          @click="wishlist"
        >
          Wishlist
        </button>
        &nbsp;
        <button
          v-if="!data.watched"
          type="button"
          class="btn btn-success"
          style="margin-bottom: 10px; margin-top: 10px"
        >
          <a
            data-toggle="collapse"
            href="#collapseExample"
            aria-expanded="false"
            aria-controls="collapseExample"
          >
            Add
          </a>
        </button>
      </div>
      <div class="col"></div>
    </div>

    <div class="row">
      <div class="col">
        <div class="card text-center">
          <div class="collapse" id="collapseExample">
            <div class="card card-body">
              <b-form inline>
                <label class="sr-only" for="score">My Score</label>
                <b-form-input
                  id="score"
                  v-model="score"
                  type="number"
                  placeholder="Enter score"
                ></b-form-input>

                <label class="sr-only" for="comments">Comments</label>
                <b-form-input
                  id="comments"
                  v-model="comments"
                  placeholder="Enter comments"
                ></b-form-input>

                <label class="sr-only" for="dateWatched">Date Watched</label>
                <b-form-datepicker
                  id="dateWatched"
                  v-model="dateWatched"
                  placeholder="Enter date watched"
                ></b-form-datepicker>

                <div class="form-check">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    v-model="liked"
                    id="flexCheckDefault"
                  />
                  <label class="form-check-label" for="flexCheckDefault">
                    Liked
                  </label>
                </div>

                <b-button variant="success" @click="add">Add film</b-button>
              </b-form>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col">
        <div class="card text-center">
          <div class="card-header">Genre(s)</div>
          <div class="card-body">
            <h5 class="card-title">{{ data.film.genres }}</h5>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card text-center">
          <div class="card-header">Directed by</div>
          <div class="card-body">
            <h5
              class="card-title"
              v-for="director in data.credits.directors"
              :key="director.id"
            >
              <router-link :to="{ name: 'Person', params: { id: director.id } }"
                >{{ director.name }}
              </router-link>
            </h5>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card text-center">
          <div class="card-header">Release Date</div>
          <div class="card-body">
            <h5 class="card-title">{{ data.film.release_date }}</h5>
          </div>
        </div>
      </div>
    </div>
    <div class="card shadow text-justify">
      <div id="text">
        <div class="row">
          <div class="col">
            <div if v-if="data.where">
              <h5>Where To Watch</h5>
              <div>
                <b-form-select
                  style="width: 250px;"
                  v-model="selectedCountry"
                  :options="countryOptions"
                ></b-form-select>
                <br />
                <br />
              </div>
              <h6 v-if="selectedCountry && selectedCountry.watch.length >= 1">
                Free to subscribers:
                <span v-for="option in selectedCountry.watch" :key="option.id">
                  <span
                    v-for="key in option"
                    :key="key.id"
                    style="margin-right: 5px;"
                  >
                    <img :src="key" style="width: 50px; height: 50px" />
                  </span>
                  &nbsp;
                </span>
              </h6>
              <h6 v-if="selectedCountry && selectedCountry.rent.length >= 1">
                Rent:
                <span v-for="option in selectedCountry.rent" :key="option.id">
                  <span
                    v-for="key in option"
                    :key="key.id"
                    style="margin-right: 5px;"
                  >
                    <img :src="key" style="width: 50px; height: 50px" />
                  </span>
                </span>
              </h6>
              <h6 v-if="selectedCountry && selectedCountry.buy.length >= 1">
                Buy:
                <span v-for="option in selectedCountry.buy" :key="option.id">
                  <span
                    v-for="key in option"
                    :key="key.id"
                    style="margin-right: 5px;"
                  >
                    <img :src="key" style="width: 50px; height: 50px" />
                  </span>
                  &nbsp;
                </span>
              </h6>
              <hr />
            </div>
            <h5>Overview</h5>
            <p>{{ data.film.overview }}</p>
            <hr />
            <div v-if="data.film.keywords">
              <h5>Keywords</h5>
              <p>{{ data.film.keywords }}</p>
              <hr />
            </div>
            <div v-if="data.review">
              <h5>
                <a :href="data.review.link.url">New York Times Review</a>
                <small v-if="data.review.critics_pick === 1"
                  >&nbsp;<b>Critic's Pick</b></small
                >
              </h5>
              <p>
                "{{ data.review.summary_short }}"
                <span> - {{ data.review.byline }}</span>
              </p>
              <hr />
            </div>
            <div v-if="data.film.recommendations">
              <h5>Recommendations</h5>
              <span v-for="item in data.film.recommendations" :key="item.id">
                <router-link :to="{ name: 'Film', params: { id: item.id } }"
                  >{{ item.title }}
                </router-link>
                |
              </span>
            </div>
            <hr />
            <div>
              <h5>Cast</h5>
              <span v-for="person in data.cast" :key="person.id">
                <router-link :to="{ name: 'Person', params: { id: person.id } }"
                  >{{ person.name }}
                </router-link>
                <span v-if="person.role"> as {{ person.role }} </span>
                <br />
              </span>
              <hr />
            </div>
            <div v-if="data.film.budget > 0">
              <h5>Budget</h5>
              ${{ data.film.budget.toLocaleString() }}
              <hr />
            </div>
            <div v-if="data.film.revenue > 0">
              <h5>Box Office</h5>
              ${{ data.film.revenue.toLocaleString() }}
              <hr />
              <h5>Runtime: {{ data.film.runtime }}min</h5>
              <hr />
            </div>
            <div v-if="data.credits.producers">
              <h5>Producers</h5>
              <span
                v-for="producer in data.credits.producers"
                :key="producer.id"
              >
                <router-link
                  :to="{ name: 'Person', params: { id: producer.id } }"
                  >{{ producer.name }}
                </router-link>
              </span>
              <hr />
            </div>

            <div v-if="data.credits.editors">
              <h5>Editors</h5>
              <span v-for="editor in data.credits.editors" :key="editor.id">
                <router-link :to="{ name: 'Person', params: { id: editor.id } }"
                  >{{ editor.name }}
                </router-link>
              </span>
              <hr />
            </div>

            <div v-if="data.credits.screenwriters">
              <h5>Screenplay By</h5>
              <span
                v-for="screenwriter in data.credits.screenwriters"
                :key="screenwriter.id"
              >
                <router-link
                  :to="{ name: 'Person', params: { id: screenwriter.id } }"
                  >{{ screenwriter.name }}
                </router-link>
              </span>
              <hr />
            </div>
            <div v-if="data.credits.story.length > 0">
              <h5>Story By</h5>
              <span
                v-for="screenwriter in data.credits.story"
                :key="screenwriter.id"
              >
                <router-link
                  :to="{ name: 'Person', params: { id: screenwriter.id } }"
                  >{{ screenwriter.name }}
                </router-link>
              </span>
              <hr />
            </div>

            <div v-if="data.credits.photographers">
              <h5>Cinematographers</h5>
              <span
                v-for="photog in data.credits.photographers"
                :key="photog.id"
              >
                <router-link :to="{ name: 'Person', params: { id: photog.id } }"
                  >{{ photog.name }}
                </router-link>
              </span>
              <hr />
            </div>

            <div v-if="data.credits.composers">
              <h5>Original Music Composers</h5>
              <span
                v-for="composer in data.credits.composers"
                :key="composer.id"
              >
                <router-link
                  :to="{ name: 'Person', params: { id: composer.id } }"
                  >{{ composer.name }}
                </router-link>
              </span>
              <hr />
            </div>
          </div>
          <div class="col text-center">
            <br />
            <img
              :src="data.poster"
              style="width: 500px; height: 550px"
              alt="poster"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import dayjs from "dayjs";

export default {
  name: "Film.vue",
  props: ["id"],
  data() {
    return {
      data: {},
      fetchedFilm: false,
      selectedCountry: null,
      countryOptions: [],
      adding: false,
      comments: "",
      score: null,
      dateWatched: null,
      liked: false,
    };
  },
  computed: {
    // thanks to https://github.com/vuejs/vue-router/issues/311
    getFullPath() {
      return this.$route.path;
    },
  },
  watch: {
    getFullPath() {
      this.fetchedFilm = false;
      this.fetchFilm();
    },
  },
  async mounted() {
    this.fetchFilm();
  },
  //   computed: {
  //     rows() {
  //       return this.films.length;
  //     },
  //   },

  methods: {
    async fetchFilm() {
      let response = await axios.get(
        `http://localhost:8001/films/${this.$route.params.id}/view`
      );

      if (response.data) {
        this.data = response.data;
        this.fetchedFilm = true;
        this.countryOptions.push({
          value: null,
          text: "Select a country",
        });
        //  { value: null, text: 'Please select an option' },
        for (const [key, value] of Object.entries(response.data.where)) {
          this.countryOptions.push({
            value: value,
            text: key,
          });
        }
      }
    },
    formatDate(date) {
      if (!date) {
        return null;
      }
      return dayjs(date).format("DD/MM/YYYY");
    },
    async wishlist() {
      let response = await axios.get(
        `http://localhost:8001/films/${this.$route.params.id}/wishlist`,
        {
          headers: {
            Authorization: "Bearer " + this.$store.state.jwt,
          },
        }
      );
      if (response.status === 200) {
        this.$router.push({ name: "Index" });
      }
    },
    async add() {
      let response = await axios.post(
        `http://localhost:8001/films/${this.$route.params.id}/add`,
        {
          score: this.score,
          comments: this.comments,
          date_watched: this.dateWatched,
          liked: this.liked,
        },
        {
          headers: {
            Authorization: "Bearer " + this.$store.state.jwt,
          },
        }
      );
      if (response.status === 200) {
        this.$router.push({ name: "Index" });
      }
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
