import Vue from "vue";
import VueRouter from "vue-router";
// import Home from "../views/Home.vue";
import Index from "../components/Films/Index";
import Film from "../components/Films/Film";
import Search from "../components/Films/Search";
import Statistics from "../components/Films/Statistics";
import Person from "../components/People/Person";
import Login from "../components/Authentication/Login";
import Discover from "../components/Films/Discover";
Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Login",
    component: Login,
  },
  {
    path: "/films",
    name: "Index",
    component: Index,
  },
  {
    path: "/films/discover",
    name: "Discover",
    component: Discover,
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
  {
    path: "/films/statistics",
    name: "Statistics",
    component: Statistics,
    props: true,
  },
  {
    path: "/films/search",
    name: "Search",
    component: Search,
  },
  {
    path: "/films/:id",
    name: "Film",
    component: Film,
    props: true,
  },

  {
    path: "/people/:id",
    name: "Person",
    component: Person,
    props: true,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
