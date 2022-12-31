import { createRouter, createWebHistory } from 'vue-router'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Profile from '../views/Profile.vue'
import Cart from '../views/Cart.vue'
import axios from 'axios'
const routes = [
    {
        path: '/',
        name: 'home',
        component: Home
    },
    {
        path: '/register',
        name: 'register',
        component: Register,
    },
    {
        path: '/login',
        name: 'login',
        component: Login,
    },
    {
        path: '/profile',
        name: 'profile',
        component: Profile,
        meta: { requiresAuth: true }
    },
    {
        path: '/cart',
        name: 'cart',
        component: Cart,
        meta: { requiresAuth: true }
    },
]

const router = createRouter({
    history: createWebHistory(), routes
})

router.beforeEach((to, from, next) => {
    if(to.matched.some(rec => rec.meta.requiresAuth)){
        axios.get("/user").then(response => {
                if(response.data.id){
                    next()
                } 
        }).catch((error) => {
            next({ name: 'login' })
        })
    } else {
        next()
    }
})

export default router