<template>
  <div>
    <form class="login" @submit.prevent="login">
      <h1>Sign in</h1>
      <label>User name</label>
      <input required v-model="username" type="text" placeholder="Username" />
      <label>Password</label>
      <input
        required
        v-model="password"
        type="password"
        placeholder="Password"
      />
      <hr />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  mounted() {
    // redirect if already logged in
    if (this.$store.state.jwt && this.$store.state.jwt.length > 0) {
      this.$router.push("/films");
    }
  },
  methods: {
    login: function() {
      const { username, password } = this;
      this.$store.dispatch("obtainToken", { username, password }).then(() => {
        setTimeout(() => {
          this.$router.push("/films").catch((err) => console.log(err));
        }, 1000);
      });
    },
  },
};
</script>

<style></style>
