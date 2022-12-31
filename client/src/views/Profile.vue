<template>
  <div class="profile text-center">
    <div class="title pt-6">
      <strong class="text-4xl">My Profile</strong>
    </div>
    <div class="p-6 flex flex-col justify-center items-center">
      <img class="h-32 w-32" src="../assets/profile.png" alt="profile" />
      <h3 class="pt-3"><strong>Username:</strong> {{ userInfo.username }}</h3>
      <h3 class="pt-3"><strong>Joined:</strong> {{ userInfo.created }}</h3>
    </div>
    <div class="options">
      <button ref="productTab" @click="changeTab" class="p-3 underline">
        My Products
      </button>
      <button ref="orderTab" @click="changeTab" class="p-3">My Orders</button>
    </div>
    <AddProductModal v-if="state.showForm" @toggleModal="showModal" />
    <div
      v-if="state.tab == 'products'"
      class="my-products flex flex-wrap justify-center items-center p-3"
    >
      <button
        @click="showModal"
        ref="formToggle"
        class="cursor-pointer p-3 h-full m-2 flex flex-col justify-center items-center max-w-xs rounded overflow-hidden border-zinc-600 hover:bg-gray-300 bg-gray-200"
        style="height: 376px; width: 320px"
      >
        <h1 class="text-6xl">+</h1>
        Add Product
      </button>
      <ProductCard
        class="cursor-default"
        v-for="product in state.products"
        :product="product"
        :key="product.id"
        :userId="userInfo.id"
      />
    </div>
    <div v-else class="orders flex flex-col justify-center items-center">
      <OrderCard
        v-for="order in state.orders.reverse()"
        :key="order.id"
        :order="order"
      />
    </div>
  </div>
</template>
<script setup>
import axios from "axios";
import { reactive, ref, onMounted, computed } from "vue";
import AddProductModal from "../components/AddProductModal.vue";
import ProductCard from "../components/ProductCard.vue";
import OrderCard from "../components/OrderCard.vue";

const props = defineProps({
  userInfo: {
    type: Object,
  },
});

const formToggle = ref();
const productTab = ref();
const orderTab = ref();

const state = reactive({
  showForm: false,
  products: null,
  switchTab: false,
  orders: null,
  tab: "products",
});

function changeTab() {
  state.switchTab = !state.switchTab;
  state.tab = state.switchTab ? "products" : "orders";
  if (state.tab == "products") {
    productTab.value.style.textDecoration = "underline";
    orderTab.value.style.textDecoration = "none";
  } else {
    orderTab.value.style.textDecoration = "underline";
    productTab.value.style.textDecoration = "none";
  }
}

function showModal() {
  state.showForm = !state.showForm;
}

function userProducts() {
  axios
    .get(`/user/${props.userInfo.username}/products`)
    .then((response) => {
      state.products = response.data;
    })
    .catch((error) => {
      return error;
    });
}

function userOrders() {
  axios
    .get("/get-orders")
    .then((response) => {
      state.orders = response.data;
    })
    .catch((error) => {
      return error;
    });
}
onMounted(() => {
  userProducts();
  userOrders();
});
</script>

<style>
textarea {
  resize: none;
}
</style>
