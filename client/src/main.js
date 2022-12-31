import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import router from './router/index'

axios.defaults.withCredentials = true
axios.defaults.baseURL = "http://localhost:5000"


const app = createApp(App).use(router)
app.use(VueAxios, axios)
app.provide('axios', app.config.globalProperties.axios)
app.mount("#app")


