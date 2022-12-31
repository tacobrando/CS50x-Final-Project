<template>
  <div
    class="register w-full flex justify-center items-center flex-col bg-gray-100"
  >
    <div class="title text-4xl mb-6 mt-6">Registration</div>
    <div class="erro p-2 rounded text-red-500 mb-3" v-if="state.error">
      {{ state.error }}
    </div>
    <form
      @submit.prevent="register()"
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
      <div class="mb-6">
        <label
          class="block text-gray-700 text-sm font-bold mb-2"
          for="password"
        >
          Confirm Password
        </label>
        <input
          class="h-10 border mt-1 rounded px-4 w-full bg-gray-50"
          id="password"
          type="password"
          placeholder="Confirm Password"
          v-model="state.form.confirmation"
        />
      </div>
      <div class="flex items-center justify-between">
        <button
          class="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          type="submit"
        >
          Register
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, inject, onMounted } from "vue";
import { useRouter } from "vue-router";

const props = defineProps({
  isLogged: {
    type: Boolean,
  },
});

const router = useRouter();
const axios = inject("axios");
const state = reactive({
  form: {
    username: "",
    password: "",
    confirmation: "",
  },
  error: null,
});

function register() {
  let userInfo = state.form;
  if (userInfo.username.length < 4) {
    return (state.error = "Invalid Username");
  } else if (state.form.password.length < 8) {
    return (state.error = "Password must be 8 characters or more");
  } else if (userInfo.password !== userInfo.confirmation) {
    return (state.error = "Passwords do not match");
  } else {
    axios
      .post("/register", userInfo)
      .then((response) => {
        if (response.status == 200) {
          location.href = "/";
        }
      })
      .catch((error) => {
        state.error = error.response.data.error;
      });
  }
}
onMounted(() => {
  if (props.isLogged == true) {
    console.log("Already logged in");
    router.push("/");
  }
});
</script>
