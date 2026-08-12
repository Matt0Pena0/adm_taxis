<script setup>
const emit = defineEmits(['toggle-sidebar']);
</script>

<template>
  <header class="h-16 bg-white/80 dark:bg-surface-dark/80 backdrop-blur-md border-b border-gray-200 dark:border-border-dark px-3 flex justify-between sticky top-0 z-20">
    
    <!-- Botón de "Hamburguesa" (solo en mobile) -->
    <div class="flex items-center ">
      <button @click="$emit('toggle-sidebar')" class="text-slate-500 dark:text-slate-400 focus:outline-none">
        <div class="size-10 m-1 me-4 dark:text-primary-dark  bg-surface-dark rounded-lg flex items-center justify-center shadow-lg shadow-primary/30">
          <span class="material-symbols-outlined">local_taxi</span> 
        </div>  
      </button>
        
        <div>
          <h1 class="text-xl font-bold tracking-tight text-slate-900 dark:text-primary-dark leading-none">Adm Taxi </h1>
          <span class="text-xs text-slate-500 dark:text-slate-400 font-medium">Aministrador de Taxis</span>
        </div>
    </div>


    <button class="rounded-full flex flex-1 items-center justify-end gap-4 text-slate-500 hover:text-primary hover:bg-primary/5 transition-colors relative">
      <span class="material-symbols-outlined">notifications</span>
      <span class=" bg-red-500 rounded-full border-2 border-white dark:border-surface-dark"></span>
    </button>

    <!-- Contenido del header para desktop puedes agregar un buscador y filtros -->
    <div class="flex flex-1 items-center justify-end gap-4">
      <input class="bg-white/80 dark:bg-surface-dark/80" type="search" placeholder="Buscar..." />
    </div>
  </header>
</template>