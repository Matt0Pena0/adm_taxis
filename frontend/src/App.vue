<script setup>
import { ref } from 'vue'
import { RouterView } from 'vue-router'

import Sidebar from './components/Sidebar.vue'
import Navbar from './components/Navbar.vue'

// Estado para controlar la visibilidad de la sidebar en móviles
const isSidebarOpen = ref(false);

// Función para abrir/cerrar la sidebar
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};
</script>

<template>
  <div class="bg-background-light dark:bg-background-dark text-slate-800 dark:text-slate-100 h-screen w-full flex overflow-hidden">
    <div class="flex-1 flex flex-col h-full relative overflow-hidden">
      <!-- Pasamos el evento para que el Navbar pueda abrir la Sidebar -->
      <Navbar @toggle-sidebar="toggleSidebar" />

      <div class="flex flex-1 overflow-hidden">
        <!-- Componente de Diseño para la Sidebar -->
        <Sidebar :is-open="isSidebarOpen" @close="isSidebarOpen = false" />

        <main class="flex-1 overflow-y-auto p-6 md:p-10">
          <div class="max-w-7xl mx-auto w-full">
            <RouterView />
          </div>
        </main>
      </div>
    </div>
  </div>
</template>
