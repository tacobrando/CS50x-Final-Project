<script setup>
import { inject, reactive, onMounted, computed } from "vue";
import ProductCard from "../components/ProductCard.vue";
import Modal from "../components/Modal.vue";

const props = defineProps({
  userInfo: {
    type: Object,
  },
  cart: {
    type: Array,
  },
});
const axios = inject("axios");
const removeProduct = inject("removeProduct");
const checkout = inject("checkout");
const state = reactive({
  products: [],
  categories: ["all"],
  category: "all",
  showModal: false,
  product: null,
});
const url = `${axios.defaults.baseURL}/image/`;
function getProducts() {
  axios
    .get("/products")
    .then((response) => {
      state.products = response.data;
      for (let i = 0; i < response.data.length; i++) {
        state.categories.push(response.data[i].category);
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

function contains(obj) {
  for (let i = 0; i < props.cart.length; i++) {
    if (props.cart[i].id === obj.id) {
      return true;
    }
  }
  return false;
}

const categories = computed(() => {
  return state.categories.filter((item, index) => {
    return state.categories.indexOf(item) == index;
  });
});

const filteredList = computed(() => {
  if (state.category == "all") {
    return state.products;
  } else {
    return state.products.filter((item) => item.category == state.category);
  }
});

function display(category) {
  state.category = category;
}

function addToCart() {
  if (props.userInfo !== null) {
    axios
      .post("/add-to-cart", state.product)
      .then((response) => {
        location.reload();
      })
      .catch((error) => {
        alert(error.response.data.error);
        state.showModal = !state.showModal;
      });
  } else {
    alert("Please login to begin purchasing");
    location.href = "/login";
  }
}

function setProduct(product) {
  state.product = product;
  state.showModal = !state.showModal;
}

function toggle() {
  state.showModal = false;
}

onMounted(() => {
  getProducts();
});
</script>

<template>
  <div class="home">
    <h1 class="p-5 text-xl">Our Store</h1>
    <div
      class="categories flex flex-row px-6 pt-4 pb-2 touch-auto scroll-smooth overflow-y-hidden overflow-x-scroll whitespace-nowrap"
    >
      <span
        class="category w-fit cursor-pointer inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2"
        v-for="(category, index) in categories"
        :key="index"
        @click="display(category)"
      >
        {{ category }}
      </span>
    </div>
    <div class="products flex flex-wrap justify-center items-center p-3">
      <ProductCard
        v-for="product in filteredList"
        :product="product"
        :key="product.id"
        @click="setProduct(product)"
      />
    </div>
    <Modal v-if="state.showModal" @toggle="toggle">
      <div
        class="product flex flex-row items-start justify-start text-start h-full"
      >
        <img
          class="h-80 w-80 p-3"
          :src="url + state.product.image"
          :alt="state.product.description"
        />
        <div class="px-6 py-4">
          <div class="font-bold text-lg mb-2 line-clamp-title">
            {{ state.product.title }}
          </div>
          <p class="text-gray-700 text-base line-clamp-description">
            <strong>Description:</strong> {{ state.product.description }}
          </p>
          <p class="text-gray-700 text-base line-clamp-description">
            <strong>Price:</strong> ${{ state.product.price }}
          </p>
          <p class="text-gray-700 text-base line-clamp-description">
            <strong>Category:</strong> {{ state.product.category }}
          </p>
          <div class="py-4">
            <button
              class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              v-if="userInfo !== null && state.product.user_id == userInfo.id"
              @click="removeProduct(state.product.id)"
            >
              Remove
            </button>
            <div v-else class="purchase flex flex-col">
              <button
                v-if="!contains(state.product)"
                @click="checkout([state.product])"
                class="bg-blue-500 m-1 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              >
                Buy
              </button>
              <button
                v-if="!contains(state.product)"
                class="bg-purple-500 m-1 hover:bg-purple-600 text-white font-bold py-2 px-2 rounded focus:outline-none focus:shadow-outline"
                @click="addToCart"
              >
                Add to cart
              </button>
              <button
                v-else
                disabled
                class="bg-purple-200 m-1 text-white font-bold py-2 px-2 rounded focus:outline-none focus:shadow-outline"
              >
                ✓ Added
              </button>
            </div>
          </div>
        </div>
      </div>
    </Modal>
  </div>
</template>

<style>
@media only screen and (max-width: 1023px) {
  .product {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
}
</style>
