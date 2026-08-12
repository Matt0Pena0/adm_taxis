<script setup>
defineProps({
  isOpen: {
    type: Boolean,
    required: true,
  },
});

const emit = defineEmits(['close']);
</script>

<template>
  <!-- Fondo oscuro para el overlay en mobile -->
  <div
    :class="isOpen ? 'block' : 'hidden'"
    @click="$emit('close')"
    class="fixed inset-0 z-20 bg-black opacity-50 transition-opacity lg:hidden"
  ></div>

  <!-- Contenedor de la Sidebar -->
  <aside :class="[
    'w-64 bg-surface-light dark:bg-surface-dark border-r border-border-light dark:border-border-dark flex flex-col justify-between shrink-0 transition-transform duration-300 h-full',
    'fixed inset-y-0 left-0 z-30 lg:sticky lg:translate-x-0',
    isOpen ? 'translate-x-0' : '-translate-x-full'
  ]">
    <div class="p-6">
      <div class="flex items-center gap-3">

        <!-- <div class="size-10 dark:text-primary-dark  bg-surface-dark rounded-lg flex items-center justify-center shadow-lg shadow-primary/30">
          <span class="material-symbols-outlined">local_taxi</span> 
        </div>  

        <div>
          <h1 class="text-xl font-bold tracking-tight text-slate-900 dark:text-primary-dark leading-none">Adm Taxi </h1>
          <span class="text-xs text-slate-500 dark:text-slate-400 font-medium">Aministrador de Taxis</span>
        </div> -->

      </div>
    </div>

    <div class="p-6">
      <nav class="flex flex-col gap-2 ">

        <RouterLink 
          to="/coches" 
          @click="$emit('close')"
          active-class="bg-primary/10 border-primary text-primary-light dark:text-primary-dark"
          class="flex items-center gap-3 px-4 py-3 rounded-lg border-l-4 border-transparent transition-all 
                  text-slate-600 dark:text-slate-400 
                  hover:bg-slate-100 dark:hover:bg-white/5"
        >
          <span class="material-symbols-outlined">local_taxi</span>
          <span class="font-bold text-md ">Coches</span>
        </RouterLink>

        <RouterLink 
          to="/choferes" 
          @click="$emit('close')"
          active-class="bg-primary/10 border-primary text-primary-light dark:text-primary-dark"
          class="flex items-center gap-3 px-4 py-3 rounded-lg border-l-4 border-transparent transition-all 
                  text-slate-600 dark:text-slate-400 
                  hover:bg-slate-100 dark:hover:bg-white/5"
        >
          <span class="material-symbols-outlined">person</span>
          <span class="font-bold text-md">Choferes</span>
        </RouterLink>

        <RouterLink 
          to="/recaudaciones" 
          @click="$emit('close')"
          active-class="bg-primary/10 border-primary text-primary-light dark:text-primary-dark"
          class="flex items-center gap-3 px-4 py-3 rounded-lg border-l-4 border-transparent transition-all 
                  text-slate-600 dark:text-slate-400 
                  hover:bg-slate-100 dark:hover:bg-white/5"
        >
          <span class="material-symbols-outlined">list_alt_add</span>
          <span class="font-bold text-md">Recaudaciones</span>
        </RouterLink>
        
      </nav>
    </div>
  </aside>
</template>