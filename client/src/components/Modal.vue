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
            <slot></slot>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { reactive } from "vue";
const emit = defineEmits(["toggle"]);
const state = reactive({
  showModal: true,
  error: null,
});
function toggleModal() {
  emit("toggle");
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
  height: fit-content;
  width: 50%;
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
}

@media only screen and (max-width: 1023px) {
  .modal-container {
    width: 30%;
    height: fit-content;
    overflow: hidden;
  }
}
@media only screen and (max-width: 800px) {
  .modal-container {
    width: 80%;
    height: fit-content;
    overflow: hidden;
  }
}
</style>
