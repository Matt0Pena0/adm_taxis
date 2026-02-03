<script setup>
</script>

<template>
  <header class="h-16 bg-white/80 dark:bg-surface-dark/80 backdrop-blur-md border-b border-gray-200 dark:border-border-dark px-6 flex items-center justify-between sticky top-0 z-20">

    <div class="flex items-center gap-4">
      <h2 class="text-lg font-bold text-slate-700 dark:text-white hidden md:block">Dashboard</h2>
    </div>

    <div class="flex items-center gap-3">

      <button class="w-10 h-10 rounded-full flex items-center justify-center text-slate-500 hover:text-primary hover:bg-primary/5 transition-colors relative">
        <span class="material-symbols-outlined">notifications</span>
        <span class="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full border-2 border-white dark:border-surface-dark"></span>
      </button>

    </div>

  </header>
</template>