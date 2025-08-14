// Vue 2 router config in src/nav/index.js
import Vue from 'vue'
import VueRouter from 'vue-router'

// Pages
import Landing from '@/views/Landing.vue'
import RouteView from '@/views/RouteView.vue'
import DataInsight from "@/views/DataInsight.vue";

Vue.use(VueRouter)

const routes = [
    { path: '/', meta: { title: 'ParkAgile' },  component: Landing },
    { path: '/route', meta: { title: 'Park & Ride options' }, component: RouteView },
    { path: '/data-insight', meta: { title: 'Data Insights' }, component: DataInsight },
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes,
    scrollBehavior() {
        return { x: 0, y: 0 }
    }
})

export default router
