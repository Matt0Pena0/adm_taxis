// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

import CochesView from '@/views/CochesView.vue'
import ChoferesView from '@/views/ChoferesView.vue'
import RecaudacionesView from '@/views/RecaudacionesView.vue'


const router = createRouter({
  // createWebHistory permite URLs limpias, usando la API del navegador
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/coches' // Redirige la raíz a coches por defecto
        },
        {
            path: '/coches',
            name: 'coches',
            component: CochesView
        },
        {
            path: '/choferes',
            name: 'choferes',
            component: ChoferesView
        },
        {
            path: '/recaudaciones',
            name: 'recaudaciones',
            component: RecaudacionesView
        },
    ]
})

export default router
