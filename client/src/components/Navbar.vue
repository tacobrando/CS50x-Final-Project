<template>
  <div
    class="navbar top-0 h-14 bg-white drop-shadow w-full flex items-center fixed z-10"
  >
    <div class="nav-main flex justify-start" style="margin: 10px">
      <router-link to="/">Home</router-link>
    </div>
    <div class="user-options w-full flex justify-end">
      <ul v-if="!props.isLogged">
        <li>
          <router-link to="/login">Login</router-link>
        </li>
        <li>
          <router-link to="/register">Register</router-link>
        </li>
      </ul>
      <ul v-if="props.isLogged">
        <li>
          <router-link to="/cart">Cart</router-link>
        </li>
        <li>
          <router-link to="/profile">Profile</router-link>
        </li>
        <li @click="logout()">Logout</li>
      </ul>
    </div>
  </div>
</template>
<script setup>
import { inject } from "vue";

const props = defineProps({
  isLogged: {
    type: Boolean,
  },
});
const axios = inject("axios");
function logout() {
  axios.get("/logout");
  location.href = "/";
}
</script>
<style>
.navbar ul {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.navbar li {
  margin: 10px;
  cursor: pointer;
}
</style>
