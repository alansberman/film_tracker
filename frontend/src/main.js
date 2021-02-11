import Vue from "vue";
import App from "./App.vue";

import router from "./router";
import { BootstrapVue, BootstrapVueIcons } from "bootstrap-vue";
import "@/assets/global.css";

import axios from "axios";
import VueAxios from "vue-axios";
import jwt_decode from "jwt-decode";
import Vuex from "vuex";

Vue.use(Vuex);
Vue.use(VueAxios, axios);

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);

Vue.config.productionTip = false;

const store = new Vuex.Store({
  state: {
    jwt: localStorage.getItem("t"),
    endpoints: {
      obtainJWT: "http://localhost:8001/auth/obtain_token",
      refreshJWT: "http://localhost:8001/auth/refresh_token",
    },
  },
  mutations: {
    updateToken(state, newToken) {
      localStorage.setItem("t", newToken["token"]);
      state.jwt = newToken["token"];

      console.log(newToken["token"], "is the token");
    },
    removeToken(state) {
      localStorage.removeItem("t");
      state.jwt = null;
    },
  },
  actions: {
    obtainToken(username, password) {
      const payload = {
        username: password["username"],
        password: password["password"],
      };
      // console.log(username);
      // console.log(password);
      axios
        .post(this.state.endpoints.obtainJWT, payload)
        .then((response) => {
          this.commit("updateToken", response.data.token);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    refreshToken() {
      const payload = {
        token: this.state.jwt,
      };
      axios
        .post(this.state.endpoints.refreshJWT, payload)
        .then((response) => {
          this.commit("updateToken", response.data.token);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    inspectToken() {
      const token = this.state.jwt;
      if (token) {
        const decoded = jwt_decode(token);
        const exp = decoded.exp;
        const orig_iat = decoded.orig_iat;
        if (
          exp - Date.now() / 1000 < 1800 &&
          Date.now() / 1000 - orig_iat < 628200
        ) {
          this.dispatch("refreshToken");
        } else if (exp - Date.now() / 1000 < 1800) {
          // DO NOTHING, DO NOT REFRESH
        } else {
          // PROMPT USER TO RE-LOGIN, THIS ELSE CLAUSE COVERS THE CONDITION WHERE A TOKEN IS EXPIRED AS WELL
        }
      }
    },
  },
});

new Vue({
  router,
  render: (h) => h(App),
  store,
}).$mount("#app");
