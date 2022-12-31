<template>
  <div class="login w-full h-full flex justify-center items-center flex-col">
    <div class="title text-4xl mb-6 mt-6">Login</div>
    <div class="error p-2 rounded text-red-500 mb-3" v-if="state.error">
      {{ state.error }}
    </div>
    <form
      @submit.prevent="login()"
      class="w-full flex flex-col justify-center items-center"
    >
      <div class="mb-4">
        <label
          class="block text-gray-700 text-sm font-bold mb-2"
          for="username"
        >
          Username
        </label>
        <input
          class="h-10 border mt-1 rounded px-4 w-full bg-gray-50"
          id="username"
          type="text"
          placeholder="Username"
          v-model="state.form.username"
        />
      </div>
      <div class="mb-4">
        <label
          class="block text-gray-700 text-sm font-bold mb-2"
          for="password"
        >
          Password
        </label>
        <input
          class="h-10 border mt-1 rounded px-4 w-full bg-gray-50"
          id="password"
          type="password"
          placeholder="Password"
          v-model="state.form.password"
        />
      </div>
      <button
        class="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        type="submit"
      >
        Login
      </button>
    </form>
  </div>
</template>

<script setup>
import { reactive, inject, onMounted } from "vue";
import { useRouter } from "vue-router";
const url = new URL("/", window.location.origin);
const props = defineProps({
  isLogged: {
    type: Boolean,
  },
});
const axios = inject("axios");
const state = reactive({
  form: {
    username: "",
    password: "",
  },
  error: null,
});

function login() {
  axios
    .post("/login", state.form)
    .then((response) => {
      if (response.status == 200) {
        location.href = url.toString();
      }
    })
    .catch((error) => {
      state.error = error.response.data["error"];
    });
}
onMounted(() => {
  if (props.isLogged == true) {
    console.log("Already logged in");
    location.href = url.toString();
  } else {
    return;
  }
});
</script>
