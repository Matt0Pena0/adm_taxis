<script setup>
</script>

<template>
  <aside class="w-64 bg-surface-light dark:bg-surface-dark border-r border-border-light dark:border-border-dark flex-col justify-between hidden md:flex shrink-0 transition-colors duration-300 h-screen sticky top-0">

    <div class="p-6">
      <div class="flex items-center gap-3 mb-10">

        <div class="size-10 dark:text-primary-dark  bg-surface-dark rounded-lg flex items-center justify-center shadow-lg shadow-primary/30">
          <span class="material-symbols-outlined">local_taxi</span> 
        </div>  

        <div>
          <h1 class="text-xl font-bold tracking-tight text-slate-900 dark:text-primary-dark leading-none">Adm Taxi </h1>
          <span class="text-xs text-slate-500 dark:text-slate-400 font-medium">Aministrador de Taxis</span>
        </div>

      </div>
    </div>

    <nav class="flex flex-col gap-2">

      <RouterLink 
        to="/coches" 
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
        active-class="bg-primary/10 border-primary text-primary-light dark:text-primary-dark"
        class="flex items-center gap-3 px-4 py-3 rounded-lg border-l-4 border-transparent transition-all 
                text-slate-600 dark:text-slate-400 
                hover:bg-slate-100 dark:hover:bg-white/5"
      >
        <span class="material-symbols-outlined">list_alt_add</span>
        <span class="font-bold text-md">Recaudaciones</span>
      </RouterLink>
      
    </nav>

  </aside>
</template>