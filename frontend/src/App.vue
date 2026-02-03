<script setup>
import { RouterView } from 'vue-router'

import Sidebar from './components/Sidebar.vue'
import Navbar from './components/Navbar.vue'


</script>

<template>
  <div class="bg-background-light dark:bg-background-dark text-slate-800 dark:text-slate-100 h-screen w-full flex overflow-hidden">
    
     <!-- Componente de Diseño para la Sidebar -->
    <Sidebar />
    
    <div class="flex-1 flex flex-col h-full relative overflow-hidden">
        
      <!-- Componente de Diseño para la Navbar -->
      <Navbar />

      <main class="flex-1 overflow-y-auto p-6 md:p-10">
        
        <div class="max-w-7xl mx-auto w-full">
          <RouterView />
        </div>
        
      </main>
    
    </div>

  </div>
</template>
