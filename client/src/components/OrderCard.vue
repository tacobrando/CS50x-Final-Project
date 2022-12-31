<template>
  <div
    class="container flex p-2 m-1 bg-white border border-gray-200 rounded-lg shadow-md"
  >
    <div class="status flex justify-start items-center w-20 mx-4">
      <strong>{{ order.status }}</strong>
    </div>
    <div class="items flex flex-col flex-grow justify-start items-start">
      <div
        class="item-title underline flex justify-start items-start text-start"
        v-for="item in order.items"
        :key="item.id"
      >
        {{ item.title }}
      </div>
    </div>
    <div class="status flex justify-center items-center mx-4">
      <strong>{{ order.created }}</strong>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  order: {
    type: Object,
  },
});
</script>

<style scoped></style>
