<template>
  <div
    class="container cursor-pointer p-3 h-full m-2 flex flex-col justify-evenly max-w-xs rounded overflow-hidden drop-shadow bg-white"
  >
    <div class="product-image w-full flex justify-center">
      <img
        class="h-40"
        v-if="product.image"
        :src="product_image"
        :alt="product.category"
      />
    </div>
    <div class="px-6 py-4">
      <div class="font-bold text-lg mb-2 line-clamp-title">
        {{ product.title }}
      </div>
      <p
        class="text-gray-700 text-base line-clamp-description"
        v-if="product.description !== 'null'"
      >
        {{ product.description }}
      </p>
      <p v-else>No description available</p>
    </div>
    <div class="px-6 pt-4 pb-2 flex flex-col text-center">
      <span
        class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2"
        >{{ product.category }}
      </span>
      <button
        class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        v-if="userId"
        @click="removeProduct(product.id)"
      >
        Remove
      </button>
    </div>
  </div>
</template>

<script setup>
import { inject } from "vue";

const axios = inject("axios");
const props = defineProps({
  product: {
    type: Object,
  },
  userId: {
    type: String,
  },
});
const removeProduct = inject("removeProduct");
const product_image = `${axios.defaults.baseURL}/image/${props.product.image}`;
</script>

<style scoped>
.line-clamp-title {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.line-clamp-description {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.container {
  height: 376px;
}
</style>
