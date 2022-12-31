<template>
  <div class="cart flex flex-col justify-center items-center p-6">
    <div class="title text-5xl p-2">
      <strong>My Cart</strong>
    </div>
    <div class="container">
      <div
        class="card flex flex-col justify-start items-center p-3 m-2 bg-white border border-gray-200 rounded-lg shadow-md md:flex-row"
        v-for="product in cart"
        :key="product.id"
      >
        <span>
          <img
            class="h-24 rounded"
            :src="imageUrl + product.image"
            :alt="product.category"
          />
        </span>
        <span class="p-2 flex flex-col justify-center flex-grow">
          <strong>{{ product.title }}</strong>
          <p><strong>Price: </strong>${{ product.price }}</p>
          <p><strong>Description: </strong>${{ product.description }}</p>
          <p><strong>Category: </strong>${{ product.category }}</p>
        </span>
        <span class="cart-options flex flex-col justify-end items-end">
          <button
            class="bg-red-500 m-1 hover:bg-red-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            @click="removeFromCart(product.index)"
          >
            Remove
          </button>
        </span>
      </div>
      <div
        v-if="cart.length > 0"
        class="total flex justify-between items-center p-3 m-2 bg-white border border-gray-200 rounded-lg shadow-md"
      >
        <span> <strong>Total:</strong> ${{ total }} </span>
        <span>
          <button
            @click="checkout(cart)"
            class="bg-blue-500 m-1 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Checkout
          </button>
        </span>
      </div>
      <div v-else class="empty">
        <h1 class="text-center pt-10 text-2xl">Empty 😔</h1>
      </div>
    </div>
  </div>
</template>
<script setup>
import { inject } from "vue";

const props = defineProps({
  cart: {
    type: Array,
  },
  total: {
    type: Number,
  },
});
const axios = inject("axios");
const imageUrl = `${axios.defaults.baseURL}/image/`;
const checkout = inject("checkout");

function removeFromCart(index) {
  axios
    .get(`/remove-from-cart/${index}`)
    .then((response) => {
      location.reload();
    })
    .catch((error) => {
      return error;
    });
}
</script>

<style scoped></style>
