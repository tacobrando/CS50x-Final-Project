<script setup>
import { reactive, onBeforeMount, inject, provide } from "vue";
import { useRoute } from "vue-router";
import Navbar from "./components/Navbar.vue";

const route = useRoute();
const axios = inject("axios");
const state = reactive({
  isLogged: reactive(false),
  userInfo: null,
  cart: [],
  total: 0,
});

function removeProduct(id) {
  if (confirm("Are you sure?")) {
    axios
      .get(`/remove-product/${id}`)
      .then((response) => {
        location.reload();
      })
      .catch((error) => {
        return error;
      });
  } else {
    return;
  }
}
provide("removeProduct", removeProduct);

function getCart() {
  axios
    .get("/cart")
    .then((response) => {
      response.data.forEach((item, index) => {
        item.index = index;
        state.cart.push(item);
        state.total += item.price;
      });
    })
    .catch((error) => {
      return error;
    });
}

function checkLogin() {
  axios
    .get("/user")
    .then((response) => {
      if (response.data.username) {
        state.userInfo = {
          id: response.data.id,
          username: response.data.username,
          created: response.data.created,
        };
        state.isLogged = true;
      }
    })
    .catch((error) => {
      return error;
    });
}

function checkout(cart) {
  if (state.userInfo !== null) {
    axios
      .post("/checkout", cart)
      .then((response) => {
        alert("Transaction successful!");
        location.href = "/";
      })
      .catch((error) => {
        console.log(error);
      });
  } else {
    alert("Please login to begin purchasing");
    location.href = "/login";
  }
}

provide("checkout", checkout);

onBeforeMount(() => {
  checkLogin();
  getCart();
});
</script>

<template>
  <nav>
    <Navbar :isLogged="state.isLogged" />
    <!-- <Sidebar /> -->
  </nav>
  <div class="main bg-gray-100">
    <router-view
      :isLogged="state.isLogged"
      :userInfo="state.userInfo"
      :cart="state.cart"
      :total="state.total"
    />
  </div>
</template>

<style scoped>
.main {
  margin-top: 56px;
  min-height: 92vh;
  background-color: rgb(243 244 246);
}
</style>
