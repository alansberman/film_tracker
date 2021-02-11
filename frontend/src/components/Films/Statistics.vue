<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col"></div>
      <div class="col text-center">
        <br />
        <h2>Statistics</h2>
      </div>
      <div class="col"></div>
    </div>
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
      <div class="col text-center">
        <h5>Filters</h5>
        <b-form-checkbox-group
          id="checkbox-group-1"
          v-model="selectedFilters"
          :options="options"
        ></b-form-checkbox-group>
      </div>
    </div>
    <div class="row">
      <div class="col"></div>
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
      <div class="col"></div>
    </div>
    <div class="row">
      <div class="col"></div>
      <div class="col text-center">
        <h6>Select Genre(s) <small>hold ctrl-C to select multiple</small></h6>
        <b-form-select
          v-model="selectedGenres"
          :options="genreOptions"
          multiple
          style="width:150px"
        ></b-form-select>
        <br /><br />
      </div>
      <div class="col"></div>
    </div>
    <div class="row">
      <div class="col text-center">
        <b-button variant="success" @click="updateFilms">Filter</b-button>
      </div>
      <br />

      <br />
      <br />
    </div>

    <div class="card shadow" v-if="fetchedStatistics && searchAgain">
      <div id="text">
        <div class="row">
          <div class="col text-center">
            <br /><br />
            <h4>No films found. Please refine the filters and search again.</h4>
            <br /><br />
          </div>
        </div>
      </div>
    </div>

    <div id="text" v-if="!fetchedStatistics">
      <div class="row">
        <div class="col text-center">
          <div class="spinner-border text-success" role="status">
            <span class="sr-only">Loading...</span>
          </div>
        </div>
      </div>
    </div>

    <div class="card shadow" v-if="fetchedStatistics && !searchAgain">
      <div id="text">
        <div class="row">
          <div class="col text-center"></div>
          <div class="col text-center">
            <h5>Of {{ statistics.num_films }} films</h5>
          </div>
          <div class="col text-center"></div>
        </div>
        <div class="row">
          <div class="col text-center">
            <p>
              <b>{{ formatNumber(statistics.average_crit) }}%</b> are New York
              Times Critic's Picks
            </p>
          </div>
          <div class="col text-center">
            <p>
              I have liked
              <b>{{ formatNumber(statistics.liked_percentage) }}%</b>
            </p>
          </div>
          <div class="col text-center">
            <p>
              <b
                >{{
                  formatNumber(statistics.average_length.runtime__avg)
                }}min</b
              >
              is the average length
            </p>
          </div>
          <div class="col text-center">
            <p>
              <b>
                {{ formatNumber(statistics.average_rating[0]) }}
              </b>
              is the average rating
              <br />
              <b> {{ formatNumber(statistics.average_score[0]) }} </b>
              is my average score
            </p>
          </div>
        </div>

        <div class="row">
          <div class="col text-center" v-html="statistics.headline"></div>
          <br />
          <br />
        </div>

        <div class="row">
          <div class="col text-center">
            <h5>
              My Top Genres <br />
              <small v-if="wishlist">with average user rating</small>
              <small v-else>with my average score</small>
            </h5>
            <span v-for="(key, value) in statistics.genres" :key="key.id">
              {{ value }} : {{ formatNumberAsPercentage(key[0]) }}
              <span v-if="wishlist">
                ({{ formatNumber(key[1]["vote_average__avg"]) }})
              </span>
              <span v-else> ({{ formatNumber(key[2].score__avg) }})</span>
              <br />
            </span>
          </div>
          <div class="col text-center">
            <h5>My Most Recommended</h5>
            <span
              v-for="(key, value) in statistics.most_recommended"
              :key="key.id"
            >
              <router-link :to="{ name: 'Film', params: { id: key[0] } }">{{
                value
              }}</router-link>
              <br />
            </span>
          </div>

          <div class="col text-center">
            <h5>My Top Keywords</h5>
            <span v-for="(key, value) in statistics.keywords" :key="key.id"
              >{{ value }}<br
            /></span>
          </div>
        </div>

        <div class="row">
          <div v-for="chart in charts" :key="chart.id" class="col">
            <h5 v-if="chart.fetched">
              {{ chart.name }}
            </h5>
            <div style="width: 500px; height: 500px;">
              <Chart
                v-if="chart.fetched"
                :chartdata="chart.chartdata"
                :options="chartOptions"
              />
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col"></div>
          <div class="col text-center">
            <h4>My Top People</h4>
            <h6>
              with % of my movies
              <span v-if="!wishlist"
                >and my average score for their movies</span
              >
            </h6>
          </div>
          <div class="col"></div>
        </div>
        <div class="row">
          <div class="col">
            <h5>Directors</h5>
            <span
              v-for="(key, value) in statistics.nb_credits.directors"
              :key="key.id"
            >
              <router-link :to="{ name: 'Person', params: { id: key.id } }">{{
                value
              }}</router-link>
              {{ formatNumberAsPercentage(key.percentage) }}
              <span v-if="!wishlist">
                ({{ formatNumber(key.avg_rating) }})
              </span>
              <br />
            </span>
          </div>
          <div class="col">
            <h5>Producers</h5>
            <span
              v-for="(key, value) in statistics.nb_credits.producers"
              :key="key.id"
            >
              <router-link :to="{ name: 'Person', params: { id: key.id } }">{{
                value
              }}</router-link>
              {{ formatNumberAsPercentage(key.percentage) }}
              <span v-if="!wishlist">
                ({{ formatNumber(key.avg_rating) }})
              </span>
              <br />
            </span>
          </div>
          <div class="col">
            <h5>Editors</h5>
            <span
              v-for="(key, value) in statistics.nb_credits.editors"
              :key="key.id"
            >
              <router-link :to="{ name: 'Person', params: { id: key.id } }">{{
                value
              }}</router-link>
              {{ formatNumberAsPercentage(key.percentage) }}
              <span v-if="!wishlist">
                ({{ formatNumber(key.avg_rating) }})
              </span>
              <br />
            </span>
          </div>
          <div class="col">
            <h5>Screenwriters</h5>
            <span
              v-for="(key, value) in statistics.nb_credits.screenwriters"
              :key="key.id"
            >
              <router-link :to="{ name: 'Person', params: { id: key.id } }">{{
                value
              }}</router-link>
              {{ formatNumberAsPercentage(key.percentage) }}
              <span v-if="!wishlist">
                ({{ formatNumber(key.avg_rating) }})
              </span>
              <br />
            </span>
          </div>
          <div class="col">
            <h5>Directors of Photography</h5>
            <span
              v-for="(key, value) in statistics.nb_credits.photographers"
              :key="key.id"
            >
              <router-link :to="{ name: 'Person', params: { id: key.id } }">{{
                value
              }}</router-link>
              {{ formatNumberAsPercentage(key.percentage) }}
              <span v-if="!wishlist">
                ({{ formatNumber(key.avg_rating) }})
              </span>
              <br />
            </span>
          </div>
          <div class="col">
            <h5>Composers</h5>
            <span
              v-for="(key, value) in statistics.nb_credits.composers"
              :key="key.id"
            >
              <router-link :to="{ name: 'Person', params: { id: key.id } }">{{
                value
              }}</router-link>
              {{ formatNumberAsPercentage(key.percentage) }}
              <span v-if="!wishlist">
                ({{ formatNumber(key.avg_rating) }})
              </span>
              <br />
            </span>
          </div>
        </div>
        <div class="row">
          <div class="col">
            <hr />
          </div>
        </div>

        <div class="row">
          <div class="col">
            <h5>Actors</h5>
            <span v-for="(key, value) in statistics.cast" :key="key.id">
              <router-link :to="{ name: 'Person', params: { id: key.id } }">{{
                value
              }}</router-link>
              {{ formatNumberAsPercentage(key.percentage) }}
              <span v-if="!wishlist">
                ({{ formatNumber(key.avg_rating) }})
              </span>
              <br />
            </span>
          </div>
          <div class="col"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Chart from "../Chart";
import dayjs from "dayjs";

export default {
  name: "Statistics.vue",
  components: { Chart },
  data() {
    return {
      statistics: {},
      wishlist: false,
      options: [
        { text: "Liked", value: "liked" },
        { text: "Disliked", value: "disliked" },
        { text: "Wishlisted", value: "wishlisted" },
        { text: "Added", value: "added" },
        { text: "Ignore Dates", value: "ignoreDates" },
      ],
      searchAgain: false,
      fetchedStatistics: false,
      minTime: null,
      maxTime: null,
      startDate: null,
      endDate: null,
      films: {},
      selectedFilters: [],
      selectedGenres: [],
      genreOptions: [],
      charts: [],
      features: [
        { name: "chart", label: "My Films By Release Year" },
        { name: "runtime-chart", label: "My Films By Runtime" },
        { name: "decades-chart", label: "My Films By Release Decade" },
      ],
      chartdata: {
        labels: [],
        datasets: [],
      },
      chartOptions: {
        responsive: true,
        legend: {
          display: true,
        },
        title: {
          text: "My Films By Decade",
          display: true,
        },
        scales: {
          xAxes: [
            {
              gridLines: {
                display: false,
              },
            },
          ],
          yAxes: [
            {
              position: "left",
              ticks: {
                beginAtZero: true,
                stepSize: 1,
              },
            },
          ],
        },
      },
    };
  },

  async mounted() {
    this.fetchFilms();
  },
  computed: {
    getStartDate() {
      return this.startDate;
    },
    getEndDate() {
      return this.endDate;
    },
  },
  methods: {
    async fetchFilms(constraints = null) {
      // const params = Object.assign({}, this.$route.query, constraints);
      let response = await axios.get(`http://localhost:8001/films/statistics`, {
        params: constraints,
        headers: {
          Authorization: "Bearer " + this.$store.state.jwt,
        },
      });

      let genre_response = await axios.get(
        `http://localhost:8001/films/genres`
      );
      this.genreOptions = genre_response["data"]["genres"].map((genre) => {
        return {
          value: genre["id"],
          text: genre["name"],
        };
      });

      if (response.data.noFilmsFound) {
        this.fetchedStatistics = true;
        this.searchAgain = true;
        return;
      }

      this.statistics = response.data.statistics;
      this.films = response.data.statistics.films;
      if (!this.startDate && !this.endDate) {
        this.setUpDateBoundaries();
      }
      this.charts = [];

      this.wishlist = response.data.wishlist;
      this.fetchCharts(constraints);
      this.searchAgain = false;
      this.fetchedStatistics = true;
    },
    formatNumber(number) {
      if (number !== undefined && number !== null) {
        return number.toFixed(2);
      }
      return null;
    },
    setUpDateBoundaries() {
      if (this.films !== undefined) {
        this.films = this.films.sort((a, b) =>
          dayjs(a.release_date) > dayjs(b.release_date) ? 1 : -1
        );
        this.startDate = dayjs(this.films[0]["release_date"]).format(
          "YYYY-MM-DD"
        );
        this.endDate = dayjs().format("YYYY-MM-DD");
      }
    },
    formatDate(date) {
      if (!date) {
        return null;
      }
      return dayjs(date).format("YYYY-MM-DD");
    },
    updateFilms() {
      this.fetchedStatistics = false;
      let filters = {};
      for (const item of this.selectedFilters) {
        if (item === "ignoreDates") {
          continue;
        }
        if (item === "disliked") {
          filters["liked"] = "False";
        } else {
          filters[item] = "True";
        }
      }

      let mustIgnoreDates = false;
      this.selectedFilters.forEach((filter) => {
        if (filter === "ignoreDates") {
          mustIgnoreDates = true;
        }
      });

      let constraints = mustIgnoreDates
        ? filters
        : Object.assign({}, filters, {
            release_date__gte: this.startDate,
            release_date__lte: this.endDate,
          });

      if (this.minTime) {
        constraints = Object.assign({}, constraints, {
          runtime__gte: this.minTime,
        });
      }

      if (this.maxTime) {
        constraints = Object.assign({}, constraints, {
          runtime__lte: this.maxTime,
        });
      }

      if (this.selectedGenres && this.selectedGenres.length > 0) {
        constraints = Object.assign({}, constraints, {
          genre__in: this.selectedGenres.join("&"),
        });
      }

      this.fetchFilms(constraints);
    },
    formatNumberAsPercentage(number) {
      if (number !== undefined && number !== null) {
        return number.toFixed(2).toString() + "%";
      }
      return null;
    },
    async setUpChart(name, label, constraints) {
      try {
        // const params = Object.assign({}, this.$route.query, constraints);
        // console.log(params);
        let response = await axios.get(`http://localhost:8001/films/${name}`, {
          params: constraints,
          headers: {
            Authorization: "Bearer " + this.$store.state.jwt,
          },
        });
        const one = response.data.data["one"];
        const two = response.data.data["two"];
        const chart = {};
        chart.chartdata = {};
        chart.chartdata.labels = response.data["labels"];
        chart.chartdata.datasets = [
          {
            backgroundColor: "rgba(0, 0, 255, 0.2)",
            borderWidth: 1,
            borderColor: "blue",
            data: one,
            label: ["Count"],
          },
          {
            backgroundColor: "rgba(255,255,255, 0.1)",
            borderWidth: 1,
            borderColor: "red",
            type: "line",
            data: two,
            label: ["My Score"],
          },
        ];
        this.chartOptions.title.text = label;
        chart.id = `${name}_${Math.random().toString()}`;
        chart.fetched = true;
        return chart;
      } catch (e) {
        console.log(e);
        return null;
      }
    },
    async fetchCharts(constraints = null) {
      for (const feature of this.features) {
        const chart = await this.setUpChart(
          feature["name"],
          feature["label"],
          constraints
        );
        if (chart) {
          this.charts.push(chart);
        }
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
