<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container animate-top">
          <div
            class="close-btn p-2 text-end cursor-pointer"
            @click="toggleModal"
          >
            X
          </div>
          <div class="modal-body fade-in">
            <div class="title text-2xl">Add a product</div>
            <form
              class="add-product"
              @submit.prevent="upload()"
              enctype="multipart/form-data"
            >
              <div class="flex items-center justify-center text-start">
                <div class="container max-w-screen-lg mx-auto">
                  <div>
                    <div class="bg-white rounded md:px-4 p-4">
                      <div
                        class="grid gap-4 gap-y-2 text-sm grid-cols-1 lg:grid-cols-3"
                      >
                        <div class="mb-4 image-preview">
                          <label> Preview: </label>
                          <div class="bg-white border w-80 h-80">
                            <img
                              class="preview w-full h-full"
                              v-if="state.preview"
                              :src="state.preview"
                              alt=""
                            />
                          </div>
                          <input
                            type="file"
                            name="file"
                            id="file"
                            @change="onChange"
                            required
                          />
                        </div>

                        <div class="lg:col-span-2">
                          <div
                            class="grid gap-4 gap-y-2 text-sm grid-cols-1 md:grid-cols-5"
                          >
                            <div class="md:col-span-5">
                              <label for="title">Title</label>
                              <input
                                type="text"
                                name="title"
                                id="title"
                                class="h-10 border mt-1 rounded px-4 w-full bg-gray-50"
                                v-model="state.formData.title"
                                required
                              />
                            </div>
                            <div class="md:col-span-2">
                              <label for="price">Price</label>
                              <input
                                class="h-10 border mt-1 rounded px-4 w-full bg-gray-50"
                                id="price"
                                type="number"
                                step="0.01"
                                placeholder="$"
                                v-model="state.formData.price"
                                required
                              />
                            </div>
                            <div class="md:col-span-3">
                              <label for="category">Category</label>
                              <select
                                v-model="state.formData.category"
                                class="h-10 bg-gray-50 flex border border-gray-200 rounded items-center mt-1 w-full"
                                name="category"
                                id="categories"
                                required
                              >
                                <option selected disabled>
                                  Select a category
                                </option>
                                <option
                                  v-for="(category, index) in state.categories"
                                  :key="index"
                                  :value="category.toLowerCase()"
                                >
                                  {{ category }}
                                </option>
                              </select>
                            </div>

                            <div class="md:col-span-5">
                              <label
                                class="block text-gray-700 text-sm font-bold mb-2"
                                for="description"
                              >
                                Description (optional)
                              </label>
                              <textarea
                                class="bg-gray-50 flex border border-gray-200 rounded items-center mt-1 w-full h-40"
                                id="description"
                                placeholder="Maximum length of 500 characters"
                                maxlength="120"
                                v-model="state.formData.description"
                              ></textarea>
                            </div>

                            <div class="md:col-span-5 text-right">
                              <div class="submit-btn inline-flex items-end">
                                <button
                                  type="submit"
                                  class="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                                >
                                  Submit
                                </button>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { reactive, inject } from "vue";
const axios = inject("axios");
const emit = defineEmits(["toggleModal"]);

const state = reactive({
  showModal: false,
  preview: "",
  categories: [
    "Electronics",
    "Apparel & Accessories",
    "Furniture",
    "Health & Personal care",
    "Food & Beverage",
    "Toys & Hobbies",
    "Books/Music/Video",
    "Office Equipment",
    "Other",
  ],
  form: new FormData(),
  formData: {
    title: null,
    price: null,
    category: null,
    description: null,
  },
});

function upload() {
  if (
    state.formData.title !== null &&
    state.formData.price !== null &&
    state.formData.category !== null
  ) {
    state.form.append("title", state.formData.title);
    state.form.append("price", state.formData.price);
    state.form.append("category", state.formData.category);
    state.form.append("description", state.formData.description);
    axios
      .post("/add-product", state.form)
      .then((response) => {
        location.reload();
      })
      .catch((error) => {
        console.log(error);
      });
  } else {
    return;
  }
}

function onChange(e) {
  let files = e.target.files || e.dataTransfer.files;

  if (!files.length) return;

  state.file = new FormData();
  state.preview = URL.createObjectURL(files[0]);

  state.form.append("file", files[0]);
}
function toggleModal() {
  emit("toggleModal");
  state.showModal = !state.showModal;
}
</script>
<style scoped>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.2);
  display: table;
  transition: opacity 0.3s ease;
}
.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}
@keyframes animatetop {
  from {
    top: -300px;
    opacity: 0;
  }
  to {
    top: 0;
    opacity: 1;
  }
}
.animate-top {
  opacity: 1;
  animation-name: animatetop;
  animation-iteration-count: 1;
  animation-timing-function: ease-in;
  animation-duration: 0.3s;
}
.modal-container {
  width: 90%;
  margin: 0px auto;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
  font-family: Helvetica, Arial, sans-serif;
}
.modal-header h3 {
  margin-top: 0;
  color: #42b983;
}
.modal-body {
  margin: 20px 0;
}
.modal-default-button {
  float: right;
}
.modal-enter {
  opacity: 0;
}
.modal-leave-active {
  opacity: 0;
}
.modal-enter .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}

@media only screen and (max-width: 1023px) {
  .modal-container {
    height: 90%;
    overflow: scroll;
  }
  .image-preview {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  .submit-btn {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .close-btn {
    right: 3.5rem;
    position: fixed;
  }
}

@media only screen and (max-width: 700px) {
  .close-btn {
    right: 2rem;
    position: fixed;
  }
}
</style>
